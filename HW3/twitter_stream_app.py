from pyspark import SparkConf, SparkContext
from pyspark.sql import Row, SQLContext
from pyspark.streaming import StreamingContext
import sys
import requests

TCP_IP = 'localhost'
TCP_PORT = 9999

HASHTAGS = set(['#food', '#photography', '#pets', '#funny', '#happybirthday',
                '#movies', '#foodporn', '#friends', '#bitcoin', '#ico'])


def sum_tags_count(new_values, total_sum):
  return sum(new_values) + (total_sum or 0)


def get_sql_context_instance(spark_context):
  if ('sqlContextSingletonInstance' not in globals()):
    globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
  return globals()['sqlContextSingletonInstance']


def process_rdd(time, rdd):
  print('\n----------- {} -----------'.format(time))
  hashtag_counts_df = None
  try:
    sql_context = get_sql_context_instance(rdd.context)
    row_rdd = rdd.map(lambda w: Row(hashtag=w[0], hashtag_count=w[1]))
    hashtags_df = sql_context.createDataFrame(row_rdd)
    hashtags_df.registerTempTable('hashtags')
    hashtag_counts_df = sql_context.sql('select hashtag, hashtag_count '
                                        'from hashtags '
                                        'order by hashtag_count desc '
                                        'limit 10')
  except:
    e = sys.exc_info()[0]
    print(e)
  finally:
    if hashtag_counts_df is not None:
      hashtag_counts_df.show()


def main():
  conf = SparkConf()
  # conf.setMaster('local[2]')
  conf.setAppName('TwitterStreamApp')
  sc = SparkContext(conf=conf)
  sc.setLogLevel('ERROR')
  ssc = StreamingContext(sc, 60)
  ssc.checkpoint('checkpoint_TwitterApp')

  dataStream = ssc.socketTextStream(TCP_IP, TCP_PORT)
  words = dataStream.flatMap(lambda line: line.split())
  hashtags = words.filter(lambda w: w in HASHTAGS).map(lambda x: (x, 1))
  tags_totals = hashtags.updateStateByKey(sum_tags_count)
  tags_totals.foreachRDD(process_rdd)
  ssc.start()
  ssc.awaitTermination()


if __name__ == '__main__':
  main()
