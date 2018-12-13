import json
import sys


def get_bid_by_city(json_file, business_id_file, city):
  fjson = open(json_file, 'r')
  fbid = open(business_id_file, 'w')

  for line in fjson:
    try:
      business = json.loads(line)
      if business['city'] == city and 'Restaurants' in business['categories']:
        fbid.write(business['business_id'] + '\n')
    except:
      pass


def main():
  get_bid_by_city(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
  main()
