import re
import sys

import nltk


STOP_WORDS = set(nltk.corpus.stopwords.words('english'))


def rm_stopwords(data_file, output_file):
  fout = open(output_file, 'w')
  for i, line in enumerate(open(data_file, 'r')):
    if i % 1000 == 0:
      print('Sentence {}'.format(i))
    if line.strip() != '':
      line = line.strip().split(' ||| ')
      tokens = line[-1].strip().split()
      tokens = [tok for tok in tokens
                if re.match(r'^\w+$', tok) and tok not in STOP_WORDS]
      line[-1] = ' '.join(tokens)
      fout.write(' ||| '.join(line) + '\n')


def main():
  data_file = sys.argv[1]
  output_file = sys.argv[2]
  rm_stopwords(data_file, output_file)


if __name__ == '__main__':
  main()
