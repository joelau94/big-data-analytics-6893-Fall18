import numpy as np


def write_cluster_data(n_feature, n_datapoint, mean_values, filename):
  datapoints = []
  for i, mean in enumerate(mean_values):
    dp = np.random.multivariate_normal([mean] * n_feature,
                                       np.identity(n_feature),
                                       n_datapoint)

    datapoints.extend(list(map(lambda d: d + [i], dp.tolist())))

  fout = open(filename, 'w')
  fout.write(','.join(['ID'] +
                      ['feature_{}'.format(i)
                       for i in range(n_feature)] +
                      ['label']) +
             '\n')

  for i, d in enumerate(datapoints):
    fout.write(','.join(map(str, [i] + d)) + '\n')


def main():
  write_cluster_data(20, 100, [0, 100, 200], 'random.csv')


if __name__ == '__main__':
  main()
