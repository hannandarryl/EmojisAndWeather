import tweepy
from twitterAuth import *

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

def buildQuery():
    with open('emojiList.txt', 'r') as file:
        queryList = []
        for line in file:
            queryList.append(line.strip())

    return queryList

# Set authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# List of GeoCodes
newYork = [-74,40,-73,41]

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

emojiQuery = buildQuery()

myStream.filter(locations=newYork, track=emojiQuery)