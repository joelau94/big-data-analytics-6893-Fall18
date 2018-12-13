import sys

import catchPhrases


class TextFeature(object):
  """TextFeature.
  0: food,
  1: specialNeed,
  2: alcohol,
  3: amount,
  4: service,
  5: efficiency,
  6: return,
  7: recommend,
  8: overall,
  9: location,
  10: place,
  11: price,
  12: sanitation
  """

  def __init__(self, text):
    tokens = text.strip().split()
    ngrams = tokens + \
        ['{} {}'.format(tokens[i], tokens[i + 1])
         for i in range(len(tokens) - 1)] + \
        ['{} {} {}'.format(tokens[i], tokens[i + 1], tokens[i + 2])
         for i in range(len(tokens) - 2)]

    self.feature_list = [0.] * 13
    for ngram in ngrams:
      if ngram in catchPhrases.foodPositive:
        self.feature_list[0] = 1.
      if ngram in catchPhrases.specialNeedPositive:
        self.feature_list[1] = 1.
      if ngram in catchPhrases.alcoholPositive:
        self.feature_list[2] = 1.
      if ngram in catchPhrases.amountPositive:
        self.feature_list[3] = 1.
      if ngram in catchPhrases.servicePositive:
        self.feature_list[4] = 1.
      elif ngram in catchPhrases.serviceNegative:
        self.feature_list[4] = -1.
      if ngram in catchPhrases.efficiencyPositive:
        self.feature_list[5] = 1.
      elif ngram in catchPhrases.efficiencyNegative:
        self.feature_list[5] = -1.
      if ngram in catchPhrases.returnPositive:
        self.feature_list[6] = 1.
      elif ngram in catchPhrases.returnNegative:
        self.feature_list[6] = -1.
      if ngram in catchPhrases.recommendPositive:
        self.feature_list[7] = 1.
      if ngram in catchPhrases.overallPositive:
        self.feature_list[8] = 1.
      elif ngram in catchPhrases.overallNegative:
        self.feature_list[8] = -1.
      if ngram in catchPhrases.locationPositive:
        self.feature_list[9] = 1.
      elif ngram in catchPhrases.locationNegative:
        self.feature_list[9] = -1.
      if ngram in catchPhrases.placePositive:
        self.feature_list[10] = 1.
      if ngram in catchPhrases.pricePositive:
        self.feature_list[11] = 1.
      elif ngram in catchPhrases.priceNegative:
        self.feature_list[11] = -1.
      if ngram in catchPhrases.sanitationPositive:
        self.feature_list[12] = 1.

  def __str__(self):
    return ','.join(map(str, self.feature_list))

  def get_list(self):
    return self.feature_list


def text2csv(text_file, csv_file):
  ftext = open(text_file, 'r')
  fcsv = open(csv_file, 'w')

  for line in ftext:
    try:
      review_id, user_id, business_id, stars, text = \
          line.strip().split(' ||| ')
      feature = TextFeature(text)
      fcsv.write(','.join([review_id,
                           user_id,
                           business_id,
                           stars,
                           str(feature)])
                 + '\n')
    except:
      pass


def main():
  text_file, csv_file = sys.argv[1:3]
  text2csv(text_file, csv_file)


if __name__ == '__main__':
  main()
