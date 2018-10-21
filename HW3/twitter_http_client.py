import json
import requests
import requests_oauthlib
import socket
import sys

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

TCP_IP = 'localhost'
TCP_PORT = 9999


def get_tweets():
  my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY,
                                     CONSUMER_SECRET,
                                     ACCESS_TOKEN,
                                     ACCESS_TOKEN_SECRET)
  url = 'https://stream.twitter.com/1.1/statuses/filter.json'
  query_data = [('language', 'en'),
                ('track', 'food,photography,pets,funny,happybirthday,'
                          'movies,foodporn,friends,bitcoin,ico')]
  query_url = url + '?' + '&'.join(['{}={}'.format(q[0], q[1])
                                    for q in query_data])
  response = requests.get(query_url, auth=my_auth, stream=True)
  print(response)
  return response


def send_tweets_to_spark(http_resp, tcp_conn):
  for line in http_resp.iter_lines():
    try:
      full_tweet = json.loads(line)
      tweet_text = full_tweet['text']
      tcp_conn.send((tweet_text + '\n').encode())
    except:
      e = sys.exc_info()[0]
      print(e)


def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)
  print('Waiting for TCP connection ...')
  conn, addr = s.accept()
  print('Connected ... Starting to get tweets.')
  resp = get_tweets()
  send_tweets_to_spark(resp, conn)


if __name__ == '__main__':
  main()
