import argparse
import abc
from collections import defaultdict
import math
import sys
import numpy as np

from pyspark.ml.feature import \
    Tokenizer, \
    RegexTokenizer, \
    StopWordsRemover, \
    HashingTF, \
    IDF
from pyspark.ml.clustering import KMeans, BisectingKMeans, GaussianMixture
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
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


def train(alg, data, k, seed=0):
  alg = alg.setK(k).setSeed(1)
  model = alg.fit(data)
  return model


def evaluate(data, model, alg, k, gt_file, cls_file):
  if alg != 'gmm':
    print_centers(model)
    wssse = model.computeCost(data)
    print('Within Set Sum of Squared Errors = {}'.format(wssse))

  predictions = model.transform(data)
  feat_pred_label = [(row.features.toArray().tolist(), row.prediction, row.category)
                     for row in predictions.collect()]
  # confusion = defaultdict(int)
  # categories = list(set(list(zip(*pred_and_label))[1]))
  # for r in pred_and_label:
  #   confusion[r] += 1

  # print('Confusion Matrix:')
  # for i in range(k):
  #   s = str(i)
  #   for c in categories:
  #     s += '\t{}: {}'.format(c, confusion[(i, c)])
  #   s += '\n'
  #   print(s)
  gt_out = open(gt_file, 'w')
  cls_out = open(cls_file, 'w')

  header = ','.join(['ID'] +
                    ['feature_{}'.format(i) for i in range(20)] +
                    ['label'])
  gt_out.write(header + '\n')
  cls_out.write(header + '\n')

  for i, r in enumerate(feat_pred_label):
    gt_out.write(','.join(map(str, [i] + r[0] + [r[2]])) + '\n')
    cls_out.write(','.join(map(str, [i] + r[0] + [r[1]])) + '\n')


def print_centers(model):
  print('Cluster centers:\n')
  for c in model.clusterCenters():
    print(c)


def main():
  parser = argparse.ArgumentParser(description='Clustering with pyspark.')

  parser.add_argument('--data-file', type=str,
                      default='enwiki.json')
  parser.add_argument('--num-clusters', type=int, default=4)
  parser.add_argument('--seed', type=int, default=23)
  parser.add_argument('--algorithm', default='kmeans',
                      choices=['kmeans', 'hier', 'gmm'])
  parser.add_argument('--output-groundtruth', type=str,
                      default='groundtruth.csv')
  parser.add_argument('--output-cluster', type=str,
                      default='cluster.csv')

  args = parser.parse_args()

  spark_session = SparkSession.builder.appName('clustering').getOrCreate()

  data = preprocess(spark_session, args.data_file)

  if args.algorithm == 'kmeans':
    alg = KMeans()
  elif args.algorithm == 'hier':
    alg = BisectingKMeans()
  elif args.algorithm == 'gmm':
    alg = GaussianMixture()

  model = train(alg, data, args.num_clusters, seed=args.seed)
  evaluate(data, model, args.algorithm, args.num_clusters,
           args.output_groundtruth, args.output_cluster)


if __name__ == '__main__':
  main()
