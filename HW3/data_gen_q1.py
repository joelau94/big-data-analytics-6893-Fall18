import json
import re
import os
import random

PATH_PREFIX = '../data/'
CATEGORIES = ['enwikibooks',
              'enwikinews',
              'enwikiversity',
              'enwikivoyage']
OUTPUT = 'enwiki.json'
NUM_SAMPLES = 1000
SEED = 23


def clean_text(json_str, cat):
  json_obj = json.loads(json_str)
  json_obj['text'] = json_obj['text'].replace('\\n', ' ').replace('\\', '')
  json_obj['text'] = ' '.join(re.findall(r'\w+', json_obj['text']))
  json_obj['category'] = cat
  json_str = json.dumps(json_obj)
  return json_str

def sample(path, category, n):
  fin = open(os.path.join(path, category + '.json'), 'r')
  lines = [clean_text(line, category)
           for line in fin.readlines() if 'text' in json.loads(line)]
  records = random.sample(lines, n)
  # records = map(lambda r: (r['text'].replace('\n', ' ').strip(), category),
  #               map(json.loads,
  #                   records)
  #               )
  # return list(records)
  return records


def data_gen(categories,
             output_file,
             n_samples,
             data_path,
             seed=None):

  random.seed(seed)
  records = []
  for cat in categories:
    records.extend(sample(data_path, cat, n_samples))
  random.shuffle(records)

  fout = open(os.path.join(data_path, output_file), 'w')
  fout.write('\n'.join(records))


def main():
  data_gen(CATEGORIES,
           OUTPUT,
           NUM_SAMPLES,
           PATH_PREFIX,
           seed=SEED)


if __name__ == '__main__':
  main()
