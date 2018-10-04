import argparse
import abc
import math

from pyspark.mllib.recommendation import ALS
from pyspark import SparkContext, SparkConf


class CollaborativeFilter(object):
  """CollaborativeFilter"""
  __metaclass__ = abc.ABCMeta

  def __init__(self,
               spark_context,
               data_file,
               sample_rate,
               rank,
               num_iters,
               reg_lambda,
               seed):
    self.spark_context = spark_context
    self.data_file = data_file
    self.sample_rate = sample_rate
    self.rank = rank
    self.num_iters = num_iters
    self.reg_lambda = reg_lambda
    self.seed = seed

  @abc.abstractmethod
  def preprocess(self):
    pass

  def train(self):
    self.model = ALS.train(self.trainRDD,
                           self.rank,
                           seed=self.seed,
                           iterations=self.num_iters,
                           lambda_=self.reg_lambda)

  def validate(self):

    predictions = self.model.predictAll(
        self.validRDD.map(lambda x: (x[0], x[1]))
    ).map(lambda r: ((r[0], r[1]), r[2]))

    labels_predictions = self.validRDD.map(
        lambda r: ((int(r[0]), int(r[1])), float(r[2]))
    ).join(predictions)

    error = math.sqrt(labels_predictions.map(
        lambda r: (r[1][0] - r[1][1])**2
    ).mean())

    return error


class MovieLensRec(CollaborativeFilter):
  """MovieLens Recommender."""

  def preprocess(self):
    raw_data = self.spark_context.textFile(self.data_file)
    raw_data_header = raw_data.take(1)[0]
    records = (raw_data.sample(False, self.sample_rate)
               .filter(lambda line: line != raw_data_header)
               .map(lambda line: line.split(','))
               .map(lambda e: (int(e[0]), int(e[1]), float(e[2])))
               .cache())
    self.trainRDD, self.validRDD = \
        records.randomSplit([8, 2], seed=self.seed)


class RestaurantRec(CollaborativeFilter):
  """Restaurant Recommender."""

  def preprocess(self):
    raw_data = self.spark_context.textFile(self.data_file)
    raw_data_header = raw_data.take(1)[0]
    records = (raw_data.sample(False, self.sample_rate)
               .filter(lambda line: line != raw_data_header)
               .map(lambda line: line.split(','))
               .map(lambda e: (int(e[0][1:]), int(e[1]), float(e[2])))
               .cache())
    self.trainRDD, self.validRDD = \
        records.randomSplit([8, 2], seed=self.seed)


class SongsRec(CollaborativeFilter):
  """Songs Recommender."""

  def preprocess(self):
    raw_data = self.spark_context.textFile(self.data_file)
    raw_data_header = raw_data.take(1)[0]
    records = (raw_data.sample(False, self.sample_rate)
               .filter(lambda line: line != raw_data_header)
               .map(lambda line: line.split(','))
               .map(lambda e: (int(e[0]), int(e[1]), float(e[2])))
               .cache())
    self.trainRDD, self.validRDD = \
        records.randomSplit([8, 2], seed=self.seed)


def main():
  parser = argparse.ArgumentParser(description='Recommendation with pyspark.')

  parser.add_argument('--data-file', type=str,
                      default='../data/movielens-20m-dataset/rating.csv')
  parser.add_argument('--sample-rate', type=float, default=.1)
  parser.add_argument('--rank', type=int, default=10)
  parser.add_argument('--num-iters', type=int, default=10)
  parser.add_argument('--reg-lambda', type=float, default=.1)
  parser.add_argument('--seed', type=int, default=23)
  parser.add_argument('--task', default='MovieLens',
                      choices=['MovieLens', 'Restaurant', 'Songs'])

  args = parser.parse_args()

  conf = (SparkConf()
          .setAppName("CollaborativeFilter")
          .set("spark.executor.memory", "2g"))
  sc = SparkContext(conf=conf)

  if args.task == 'MovieLens':
    rec_class = MovieLensRec
  elif args.task == 'Restaurant':
    rec_class = RestaurantRec
  elif args.task == 'Songs':
    rec_class = SongsRec

  recommender = rec_class(spark_context=sc,
                          data_file=args.data_file,
                          sample_rate=args.sample_rate,
                          rank=args.rank,
                          num_iters=args.num_iters,
                          reg_lambda=args.reg_lambda,
                          seed=args.seed)

  recommender.preprocess()
  recommender.train()
  rmse = recommender.validate()
  print('Task dataset: {}\n'
        'Sample Rate: {}\n'
        'Rank: {}\n'
        'RMSE = {}\n'
        .format(args.task, args.sample_rate, args.rank, rmse))


if __name__ == '__main__':
  main()
