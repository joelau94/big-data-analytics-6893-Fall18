import glob
import os
import sys


ORIG_DATA = '../data/yelp_features.csv'
RID_FILE_DIR = '../rids'


def filter_by_review_id(in_file, out_file, rids):
  fin = open(in_file, 'r')
  fout = open(out_file, 'w')
  for line in fin.readlines()[1:]:
    if line.strip() != '':
      rid = line.strip().split(',')[0]
      if rid in rids:
        fout.write(line)


def run_exp(csv_file, rid_file=None):
  if rid_file is not None:
    subset_file = os.path.splitext(csv_file)[0] \
        + '-' \
        + os.path.split(rid_file)[-1]
    rids = set([rid
                for rid in map(lambda l: l.strip(),
                               open(rid_file, 'r').readlines()[1:])
                if rid != ''])
    filter_by_review_id(csv_file, subset_file, rids)
  else:
    subset_file = csv_file
    rid_file = csv_file

  split_out_prefix = os.path.splitext(subset_file)[0]
  split_cmd = 'python create_split.py {} {} 0.1 23'.format(
      subset_file, split_out_prefix)

  subset_name = os.path.split(os.path.splitext(rid_file)[0])[-1]
  train_cmd = ('python main.py '
               '--n-estimators 20 '
               '--criterion gini '
               '--max-depth 50 '
               '--seed 23 '
               '--train-datafile {} '
               '--test-datafile {} '
               '--model-path ../models/{}-model.pkl '
               '--fig-path ../figure/{}.png'
               .format(split_out_prefix + '_train.csv',
                       split_out_prefix + '_test.csv',
                       subset_name,
                       subset_name
                       ))

  print('Training subset {}:'.format(rid_file))
  sys.stdout.flush()
  os.system(split_cmd)
  os.system(train_cmd)


def main():
  for rid_file in glob.glob(os.path.join(RID_FILE_DIR, '*')):
    run_exp(ORIG_DATA, rid_file)
  run_exp(ORIG_DATA)


if __name__ == '__main__':
  main()

