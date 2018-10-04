import argparse
import abc
import math

from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.regression import \
    DecisionTreeRegressor, \
    RandomForestRegressor, \
    GBTRegressor
from pyspark.ml.classification import \
    DecisionTreeClassifier, \
    RandomForestClassifier, \
    GBTClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer
from pyspark.ml.evaluation import \
    RegressionEvaluator, MulticlassClassificationEvaluator


class RegressorClassifier(object):
  """Base class for Regressors and Classifiers."""
  __metaclass__ = abc.ABCMeta

  def __init__(self,
               spark_session,
               data_file,
               data_format,
               model_builder,
               model_evaluator,
               metrics,
               max_categories,
               num_trees=None,
               max_iter=None):

    self.spark_session = spark_session
    self.data_file = data_file
    self.data_format = data_format
    self.model_builder = model_builder
    self.model_evaluator = model_evaluator
    self.metrics = metrics
    self.max_categories = max_categories
    self.num_trees = num_trees
    self.max_iter = max_iter

  @abc.abstractmethod
  def prepare(self):
    pass

  def train_validate(self):
    model = self.pipeline.fit(self.train_data)
    predictions = model.transform(self.valid_data)
    if self.metrics == 'rmse':
      labelCol = 'label'
    elif self.metrics == 'accuracy':
      labelCol = 'indexedLabel'
    evaluator = self.model_evaluator(labelCol=labelCol,
                                     predictionCol="prediction",
                                     metricName=self.metrics)
    metric = evaluator.evaluate(predictions)
    print('Model: {}\n'
          'Dataset: {}\n'
          'Performance: {} = {}\n'.format(
              self.model_builder.__name__,
              self.data_file,
              self.metrics,
              metric))


class Regressor(RegressorClassifier):
  """Regressor."""

  def prepare(self):
    data = (self.spark_session.read.format(self.data_format)
            .load(self.data_file))
    featureIndexer = (VectorIndexer(inputCol="features",
                                    outputCol="indexedFeatures",
                                    maxCategories=self.max_categories)
                      .fit(data))
    self.train_data, self.valid_data = data.randomSplit([0.8, 0.2])
    if self.model_builder.__name__ == 'GBTRegressor':
      regressor = self.model_builder(featuresCol="indexedFeatures",
                                     maxIter=self.max_iter)
    else:
      regressor = self.model_builder(featuresCol="indexedFeatures")
    self.pipeline = Pipeline(stages=[featureIndexer, regressor])


class Classifier(RegressorClassifier):
  """Classifier."""

  def prepare(self):
    data = (self.spark_session.read.format(self.data_format)
            .load(self.data_file))
    labelIndexer = StringIndexer(
        inputCol="label", outputCol="indexedLabel").fit(data)
    featureIndexer = (VectorIndexer(inputCol="features",
                                    outputCol="indexedFeatures",
                                    maxCategories=self.max_categories)
                      .fit(data))
    self.train_data, self.valid_data = data.randomSplit([0.8, 0.2])
    if self.model_builder.__name__ == 'DecisionTreeClassifier':
      classifier = self.model_builder(labelCol="indexedLabel",
                                      featuresCol="indexedFeatures")
    elif self.model_builder.__name__ == 'RandomForestClassifier':
      classifier = self.model_builder(labelCol="indexedLabel",
                                      featuresCol="indexedFeatures",
                                      numTrees=self.num_trees)
      labelConverter = IndexToString(inputCol="prediction",
                                     outputCol="predictedLabel",
                                     labels=labelIndexer.labels)
    elif self.model_builder.__name__ == 'GBTClassifier':
      classifier = self.model_builder(labelCol="indexedLabel",
                                      featuresCol="indexedFeatures",
                                      maxIter=self.max_iter)

    if self.model_builder.__name__ == 'RandomForestClassifier':
      self.pipeline = Pipeline(stages=[labelIndexer,
                                       featureIndexer,
                                       classifier,
                                       labelConverter])
    else:
      self.pipeline = Pipeline(stages=[labelIndexer,
                                       featureIndexer,
                                       classifier])


def main():
  parser = argparse.ArgumentParser(
      description='Regression and classification with Pyspark.')

  parser.add_argument('--data-file', type=str,
                      default='../data/movielens-20m-dataset/rating.csv')
  parser.add_argument('--data-format', type=str,
                      default='libsvm')
  parser.add_argument('--model', default='DecisionTreeRegressor',
                      choices=['DecisionTreeRegressor',
                               'RandomForestRegressor',
                               'GBTRegressor',
                               'DecisionTreeClassifier',
                               'RandomForestClassifier',
                               'GBTClassifier'])
  parser.add_argument('--max-categories', type=int, default=4)
  parser.add_argument('--num-trees', type=int, default=10)
  parser.add_argument('--max-iter', type=int, default=10)

  args = parser.parse_args()

  spark_session = SparkSession.builder.appName('reg_cls').getOrCreate()

  if args.model.endswith('Regressor'):
    mdl = Regressor(spark_session=spark_session,
                    data_file=args.data_file,
                    data_format=args.data_format,
                    model_builder=eval(args.model),
                    model_evaluator=RegressionEvaluator,
                    metrics='rmse',
                    max_categories=args.max_categories,
                    num_trees=args.num_trees,
                    max_iter=args.max_iter)
  elif args.model.endswith('Classifier'):
    mdl = Classifier(spark_session=spark_session,
                     data_file=args.data_file,
                     data_format=args.data_format,
                     model_builder=eval(args.model),
                     model_evaluator=MulticlassClassificationEvaluator,
                     metrics='accuracy',
                     max_categories=args.max_categories,
                     num_trees=args.num_trees,
                     max_iter=args.max_iter)
  mdl.prepare()
  mdl.train_validate()


if __name__ == '__main__':
  main()
