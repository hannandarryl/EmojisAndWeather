import tweepy
from twitterAuth import *
import sqlite3
import time

# Connect to database
c = sqlite3.connect('/data/emojiDatabase.db')

# Collect the list of all emojis we will be considering
emojiList = []
with open('emojiList.txt', 'r') as file:
    for line in file:
        emojiList.append(line.strip())


# Get the count of a specific emoji in a given string
def emojiCount(emoji, text):
    index = text.find(emoji)
    if index == -1:
        return 0
    else:
        return 1 + emojiCount(emoji, text[index + 1:])


# Build the vector of emojis given the text from a tweet
def extractEmojis(text):
    emojiVector = [0 for emoji in emojiList]
    for i in range(len(emojiList)):
        emojiVector[i] = emojiCount(emojiList[i], text)

    return emojiVector


# Class that defines the functionality of our listener
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super.__init__(self)
        self.theTime = time.time()
        self.vector = []

    # This is executed each time a status is received
    def on_status(self, status):
        # Get the vector of emojis from the tweet
        tmpvector = extractEmojis(status.text)

        # Below code collects emojis for an hour and then adds them to the database
        if (self.theTime < self.theTime + 3600):
            # Add (element-wise) the vector of emojis from the current tweet to the preexisting vector
            self.vector = [sum(x) for x in zip(self.vector, tmpvector)]
        else:
            # Create the list of data that will be inserted
            rowList = []
            rowList.append(str(self.theTime))
            rowList.append(str(time.time()))
            rowList.append('NewYork')  # TODO: Get the location from the tweet
            for value in self.vector:
                rowList.append(str(value))

            # TODO: Weather code here

            # Perform the insert
            c.execute(
                'INSERT INTO emojiWeather VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)')

            # Commit after each insert to avoid data loss
            c.commit()

            # Reset our time and set all values in emoji vector to 0
            self.theTime = time.time()
            self.vector = [0 for i in range(75)]


# Set authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# List of GeoCodes
newYork = [-74, 40, -73, 41]
sanFran = [-122.75, 36.8, -121.75, 37.8]

# Initialize the Stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Begin streaming, will capture all tweets that contain one of our emojis OR came from one of our geographic locations
myStream.filter(locations=newYork, track=emojiList)
