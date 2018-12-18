from collections import defaultdict
import re
import sys


def read_log(log_file):
  data = dict()
  features = set()

  flog = open(log_file, 'r')
  subset = ''
  for line in flog:
    if line.startswith('Training'):
      try:
        subset = re.findall(r'Training subset ../rids/(.+).csv:', line)[0]
      except:
        subset = 'Full Data'
      data[subset] = defaultdict(lambda: dict())
    elif line.startswith('Test'):
      acc = float(re.findall(r'Test Accuarcy: (.+)', line)[0])
      data[subset]['acc'] = acc
    elif line[0].isdigit():
      rank, feat, imp, std = re.findall(r'(\d+). feature (.+) \(importance:'
                                        '(.+), std:(.+)\)',
                                        line)[0]
      data[subset][feat] = {'rank': int(rank),
                            'imp': float(imp),
                            'std': float(std)}
      features.add(feat)

  return data, features


def write_csv(data, features, csv_file):
  features = list(features)
  fcsv = open(csv_file, 'w')

  fcsv.write(','.join(['Subset', 'Accuarcy'] + features) + '\n')

  for subset, feat_dict in data.iteritems():
    fields = [subset, '{:.4f}'.format(feat_dict['acc'])]
    for feat in features:
      fields.append('{:2d} ({:.4f}{}{:.4f})'.format(feat_dict[feat]['rank'],
                                                    feat_dict[feat]['imp'],
                                                    u'\u00B1'.encode('utf8'),
                                                    feat_dict[feat]['std']))
    fcsv.write(','.join(fields) + '\n')


def main():
  log_file, csv_file = sys.argv[1:3]
  data, features = read_log(log_file)
  write_csv(data, features, csv_file)


if __name__ == '__main__':
  main()
