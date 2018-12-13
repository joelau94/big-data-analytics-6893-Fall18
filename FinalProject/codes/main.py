import argparse
import os

import data
import models
import visualize


def main():
  parser = argparse.ArgumentParser(description='Yelp Rating Interpretation')

  parser.add_argument('--n-estimators', type=int, default=100)
  parser.add_argument('--criterion', type=str, default='gini',
                      choices=['gini', 'entropy'])
  parser.add_argument('--max-depth', type=int, default=20)
  parser.add_argument('--seed', type=int, default=23)
  parser.add_argument('--top-n-features', type=int)

  parser.add_argument('--train-datafile', type=str,
                      default='data/train.csv')
  parser.add_argument('--test-datafile', type=str,
                      default='data/test.csv')
  parser.add_argument('--model-path', type=str,
                      default='models/model.pkl')
  parser.add_argument('--fig-path', type=str,
                      default='figure/importance.png')

  args = parser.parse_args()

  model = models.RatingInterpreter(n_estimators=args.n_estimators,
                                   criterion=args.criterion,
                                   max_depth=args.max_depth,
                                   seed=args.seed,
                                   top_n_features=args.top_n_features)

  # if os.path.exists(args.model_path):
  #   model.load(args.model_path)
  # else:
  train_dataset = data.Dataset(args.train_datafile)
  test_dataset = data.Dataset(args.test_datafile)

  # acc, rmse = model.train(train_dataset, test_dataset)
  acc = model.train(train_dataset, test_dataset)
  model.save(args.model_path)

  importances, std = model.get_importance()
  # visualize.display(importances, std, acc, rmse, args.fig_path,
  #                   top_n_features=args.top_n_features)
  visualize.display(importances, std, acc, args.fig_path,
                    top_n_features=args.top_n_features)


if __name__ == '__main__':
  main()
