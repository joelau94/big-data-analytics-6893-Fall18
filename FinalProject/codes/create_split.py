import math
import random
import sys


def main():
  in_file, out_file_prefix, test_ratio, seed = sys.argv[1:5]
  test_ratio = float(test_ratio)
  seed = int(seed)

  random.seed(seed)
  records = open(in_file, 'r').readlines()
  random.shuffle(records)

  num_test_samples = int(math.ceil(test_ratio * len(records)))

  open(out_file_prefix + '_train.csv', 'w').write(
      ''.join(records[:- num_test_samples]))
  open(out_file_prefix + '_test.csv', 'w').write(
      ''.join(records[- num_test_samples:]))


if __name__ == '__main__':
  main()