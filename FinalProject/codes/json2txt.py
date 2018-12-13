import json
import re
import sys

import nltk


STOP_WORDS = set(nltk.corpus.stopwords.words('english'))


# def extract(json_file, text_file, business_id_file):
#   """
#   Output text format:
#   review_id ||| user_id ||| business_id ||| stars ||| text
#   """
#   fjson = open(json_file, 'r')
#   ftext = open(text_file, 'w')
#   fbid = open(business_id_file, 'r')
#   bids = set(fbid.read().strip().split('\n'))

#   for i, line in enumerate(fjson):
#     try:
#       if i % 1000 == 0:
#         print('Processing {} ...'.format(i))
#       review = json.loads(line)
#       if review['business_id'] in bids:
#         tokens = nltk.tokenize.word_tokenize(review['text'].lower())
#         # tokens = [t for t in tokens if not t in STOP_WORDS]
#         tokens = [tok for tok in tokens
#                   if re.match(r'^\w+$', tok) and tok not in STOP_WORDS]

#         clean_text = ' '.join(tokens)

#         ftext.write('{} ||| {} ||| {} ||| {} ||| {}\n'
#                     .format(review['review_id'],
#                             review['user_id'],
#                             review['business_id'],
#                             review['stars'],
#                             clean_text))
#     except:
#       pass


def extract(json_file, text_file):
  """
  Output text format:
  review_id ||| user_id ||| business_id ||| stars ||| text
  """
  fjson = open(json_file, 'r')
  ftext = open(text_file, 'w')

  for i, line in enumerate(fjson):
    try:
      if i % 1000 == 0:
        print('Processing {} ...'.format(i))
      review = json.loads(line)
      tokens = nltk.tokenize.word_tokenize(review['text'].lower())
      # tokens = [t for t in tokens if not t in STOP_WORDS]
      tokens = [tok for tok in tokens
                if re.match(r'^\w+$', tok) and tok not in STOP_WORDS]

      clean_text = ' '.join(tokens)

      ftext.write('{} ||| {} ||| {} ||| {} ||| {}\n'
                  .format(review['review_id'],
                          review['user_id'],
                          review['business_id'],
                          review['stars'],
                          clean_text))
    except:
      pass


def main():
  json_file = sys.argv[1]
  text_file = sys.argv[2]
  extract(json_file, text_file)


if __name__ == '__main__':
  main()
