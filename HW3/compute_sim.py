import argparse
import abc
import math
import os
import sys
import _pickle as pkl

from pyspark.ml.feature import \
    Tokenizer, \
    RegexTokenizer, \
    StopWordsRemover, \
    HashingTF, \
    IDF, \
    Normalizer
from pyspark.mllib.linalg.distributed import IndexedRow, IndexedRowMatrix
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType, DoubleType
from pyspark.ml import Pipeline


def preprocess(spark_session, data_file):
  raw_data = spark_session.read.format('json').load(data_file)

  regexTokenizer = RegexTokenizer(inputCol='text',
                                  outputCol='words',
                                  pattern='\\w+',
                                  gaps=False,
                                  toLowercase=True)

  stopWordsRemover = StopWordsRemover(inputCol='words',
                                      outputCol='filtered_words')

  hashingTF = HashingTF(inputCol='filtered_words',
                        outputCol='tf_features',
                        numFeatures=20)

  idf = IDF(inputCol='tf_features', outputCol='features')

  pipeline = Pipeline(stages=[regexTokenizer, stopWordsRemover, hashingTF, idf])
  pipeline_model = pipeline.fit(raw_data)
  data = pipeline_model.transform(raw_data)

  return data


def get_sim(tfidf, threshold, save_dir):
  normalizer = Normalizer(inputCol='features', outputCol='norm')
  data = normalizer.transform(tfidf)
  dot_udf = udf(lambda x, y: float(x.dot(y)), DoubleType())
  sim_df = (data.alias('i')
            .join(data.alias('j'), col('i.id') < col('j.id'))
            .select(col('i.id').alias('i'),
                    col('j.id').alias('j'),
                    dot_udf('i.norm', 'j.norm').alias('similarity'))
            # .sort('i', 'j')
            )
  sim_df_filtered = sim_df.filter(col('similarity').between(threshold, 1.0))

  edges = [(row.i, row.j, row.similarity)
           for row in sim_df_filtered.collect()]
  print('Edges: {}'.format(len(edges)))
  vertices = set()
  for e in edges:
    vertices.add(e[0])
    vertices.add(e[1])
  vertices = [(v,) for v in list(vertices)]
  doc_sim = {'edges': edges, 'vertices': vertices}

  pkl.dump(doc_sim, open(os.path.join(save_dir, 'doc_sim.pkl'), 'wb'))


def main():
  parser = argparse.ArgumentParser(description='Clustering with pyspark.')

  parser.add_argument('--data-file', type=str,
                      default='../data/enwiki.json')
  parser.add_argument('--threshold', type=float, default=0.9)

  args = parser.parse_args()

  spark_session = SparkSession.builder.appName('similarity').getOrCreate()

  data = preprocess(spark_session, args.data_file)

  get_sim(data, args.threshold, os.path.dirname(args.data_file))


if __name__ == '__main__':
  main()
