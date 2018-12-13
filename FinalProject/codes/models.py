import pickle as pkl
import sys

import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import mean_squared_error

import visualize


class RatingInterpreter(object):
  '''RatingInterpreter'''

  def __init__(self,
               n_estimators=100,
               criterion='gini',
               max_depth=None,
               seed=0,
               top_n_features=3):

    self.forest = ExtraTreesClassifier(
        n_estimators=n_estimators,
        criterion=criterion,
        max_depth=max_depth,
        random_state=seed)

    self.top_n_features = top_n_features

  def train(self, train_dataset, test_dataset):
    self.forest.fit(train_dataset.features, train_dataset.labels)
    acc = self.forest.score(test_dataset.features, test_dataset.labels)
    # rmse = np.sqrt(mean_squared_error(
    #     test_dataset.labels, self.forest.predict(test_dataset.features)))
    print('Test Accuarcy: {}'.format(acc))
    # print('RMSE: {}'.format(rmse))
    sys.stdout.flush()
    # return acc, rmse
    return acc

  def get_importance(self):
    importances = self.forest.feature_importances_
    std = np.std([tree.feature_importances_
                  for tree in self.forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    if self.top_n_features is None:
      self.top_n_features = indices.shape[0]

    print('Feature ranking:')
    for f in range(self.top_n_features):
      print('{}. feature {} (importance:{}, std:{})'
            .format(f + 1,
                    visualize.FMAP[indices[f]],
                    importances[indices[f]],
                    std[indices[f]]))
    sys.stdout.flush()

    return importances, std

  def save(self, path):
    pkl.dump(self.forest, open(path, 'wb'))

  def load(self, path):
    self.forest = pkl.load(open(path, 'rb'))
