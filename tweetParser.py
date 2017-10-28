import tweepy
from twitterAuth import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

for status in tweepy.Cursor(api.search, q='test', geocode='40.7128, 74.0060, 200mi').items(100):
    print(status)