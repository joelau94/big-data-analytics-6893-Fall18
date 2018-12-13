import os

import numpy as np
import matplotlib.pyplot as plt


FMAP = [
    # text features
    'food', 'specialNeed', 'alcohol', 'amount', 'service', 'efficiency',
    'return', 'recommend', 'overall', 'location', 'place', 'price',
    'sanitation',
    # review features
    'kolreview', 'social1rating', 'social2rating',
    # user features
    'community', 'elite', 'closeness', 'betweenness', 'pagerank',
    'user_avgstar',
    # business features
    'zip_code', 'restaurant_avgstar', 'c0fav', 'c3fav', 'c2fav', 'c9fav', 'c13fav',
    'c42fav', 'c5fav', 'c19fav', 'c21fav', 'c54fav', 'c27fav', 'c34fav',
    'c70fav', 'c10fav', 'c12fav', 'c33fav', 'c167fav'
]


def display(importances, std, acc, fig_path, top_n_features=None):
  indices = np.argsort(importances)
  feature_names = [FMAP[i] for i in indices]

  name = os.path.splitext(os.path.split(fig_path)[-1])[0]
  title = '{} (Acc={:.4f})'.format(name, acc)
  # title = '{} (Acc={:.4f}, RMSE={:.4f})'.format(name, acc, rmse)

  if top_n_features is None:
    top_n_features = indices.shape[0]

  plt.switch_backend('agg')

  plt.figure()
  plt.title(title)
  plt.barh(range(top_n_features), importances[indices],
           color='r', xerr=std[indices], align='center')
  plt.gcf().subplots_adjust(left=0.25)
  plt.yticks(range(top_n_features), feature_names, fontsize=8)
  plt.ylim([-1, top_n_features])
  plt.savefig(fig_path)
