from collections import Counter
import sys


def extract_ngram(data_file):
  unigrams, bigrams, trigrams = [], [], []
  for i, line in enumerate(open(data_file, 'r')):
    if i % 1000 == 0:
      print('Sentence {}'.format(i))
    if line.strip() != '':
      tokens = line.strip().split('|||')[-1].strip().split()
      unigrams.extend(tokens)
      bigrams.extend(['{} {}'.format(tokens[i], tokens[i+1])
                      for i in range(len(tokens)-1)])
      trigrams.extend(['{} {} {}'.format(tokens[i], tokens[i+1], tokens[i+2])
                       for i in range(len(tokens)-2)])
  return unigrams, bigrams, trigrams


def print_sorted_ngrams(output_file, ngrams):
  ngrams = Counter(ngrams)
  fout = open(output_file, 'w')
  for k, v in sorted(ngrams.iteritems(),
                     key=lambda (k, v): (v, k),
                     reverse=True):
    fout.write('{}\t{}\n'.format(k, v))


def main():
  data_file = sys.argv[1]
  output_prefix = sys.argv[2]
  unigrams, bigrams, trigrams = extract_ngram(data_file)
  print_sorted_ngrams(output_prefix + '.unigram.txt', unigrams)
  print_sorted_ngrams(output_prefix + '.bigram.txt', bigrams)
  print_sorted_ngrams(output_prefix + '.trigram.txt', trigrams)


if __name__ == '__main__':
  main()
