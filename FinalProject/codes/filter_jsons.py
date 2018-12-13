import json
import sys


def filter_business(in_file, out_file, city):
  fin = open(in_file, 'r')
  fout = open(out_file, 'w')
  business_ids = set()

  for line in fin:
    try:
      business = json.loads(line)
      if business['city'] == city and 'Restaurants' in business['categories']:
        business_ids.add(business['business_id'])
        fout.write(line)
    except:
      pass

  return business_ids


def filter_review(in_file, out_file, business_ids):
  fin = open(in_file, 'r')
  fout = open(out_file, 'w')
  user_ids = set()

  for line in fin:
    try:
      review = json.loads(line)
      if review['business_id'] in business_ids:
        user_ids.add(review['user_id'])
        fout.write(line)
    except:
      pass

  return user_ids


def filter_user(in_file, out_file, user_ids):
  fin = open(in_file, 'r')
  fout = open(out_file, 'w')

  for line in fin:
    try:
      user = json.loads(line)
      if user['user_id'] in user_ids:
        fout.write(line)
    except:
      pass


def main():
  city = sys.argv[1]
  business_in = sys.argv[2]
  business_out = sys.argv[3]
  review_in = sys.argv[4]
  review_out = sys.argv[5]
  user_in = sys.argv[6]
  user_out = sys.argv[7]

  print('Filtering business ...')
  business_ids = filter_business(business_in, business_out, city)

  print('Filtering review ...')
  user_ids = filter_review(review_in, review_out, business_ids)

  print('Filtering user ...')
  filter_user(user_in, user_out, user_ids)


if __name__ == '__main__':
  main()
