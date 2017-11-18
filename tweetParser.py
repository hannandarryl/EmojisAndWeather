import tweepy
from twitterAuth import *
import sqlite3
import time
import pyowm

# List of GeoCodes
newYork = [-74, 40, -73, 41]
sanFran = [-122.75, 36.8, -121.75, 37.8]
LA = [-118.65, 33.64, -117.58, 34.4]
chicago = [-88.21, 41.45, -87.01, 42.49]
houston = [-95.80, 29.53, -95.01, 30.09]
philly = [-75.38, 39.82, -74.91, 40.07]
phoenix = [-112.30, 33.22, -111.65, 33.78]
sanAntonio = [-98.74, 29.21, -98.20, 29.67]
sanDiego = [-117.38, 32.52, -116.88, 32.90]
dallas = [-97.08, 32.59, -96.47, 33.07]
sanJose = [-122.09, 37.23, -121.69, 37.47]
austin = [-97.95, 30.10, -97.48, 30.56]
jacksonville = [-81.82, 30.17, -81.48, 30.48]
indianapolis = [-86.32, 39.67, -85.97, 39.96]
columbus = [-83.16, 39.85, -82.77, 40.14]
seattle = [-122.75, 47.24, -121.87, 48.04]
denver = [-105.25, 39.51, -104.60, 40.06]
detroit = [-83.45, 41.97, -82.64, 42.59]
DC = [-77.28, 38.76, -76.80, 39.05]
boston = [-71.29, 42.17, -70.84, 42.54]
nashville = [-86.89, 36.08, -86.63, 36.28]

# Connect to database
c = sqlite3.connect('data/emojiDatabase.db')

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


def inRectangle(point, rectangleCoords):
    if (point[0] > rectangleCoords[0] and point[0] < rectangleCoords[2]) or (
                    point[0] < rectangleCoords[0] and point[0] > rectangleCoords[2]):
        if (point[1] > rectangleCoords[1] and point[1] < rectangleCoords[3]) or (
                        point[1] < rectangleCoords[1] and point[1] > rectangleCoords[3]):
            return True

    return False


# Check if two bounding boxes are intersected
def areIntersected(statusCoords, cityCoords):
    return inRectangle(statusCoords[0], cityCoords) or inRectangle(statusCoords[1], cityCoords) or inRectangle(
        statusCoords[2], cityCoords) or inRectangle(statusCoords[3], cityCoords)


# Gets the city given a set of coordinates
def getCity(coordinates):
    if areIntersected(coordinates, newYork):
        return 'NewYork'
    elif areIntersected(coordinates, sanFran):
        return 'SanFrancisco'
    elif areIntersected(coordinates, LA):
        return 'LosAngeles'
    elif areIntersected(coordinates, chicago):
        return 'Chicago'
    elif areIntersected(coordinates, houston):
        return 'Houston'
    elif areIntersected(coordinates, philly):
        return 'Philadelphia'
    elif areIntersected(coordinates, phoenix):
        return 'Phoenix'
    elif areIntersected(coordinates, sanAntonio):
        return 'SanAntonio'
    elif areIntersected(coordinates, sanDiego):
        return 'SanDiego'
    elif areIntersected(coordinates, dallas):
        return 'Dallas'
    elif areIntersected(coordinates, sanJose):
        return 'SanJose'
    elif areIntersected(coordinates, austin):
        return 'Austin'
    elif areIntersected(coordinates, jacksonville):
        return 'Jacksonville'
    elif areIntersected(coordinates, indianapolis):
        return 'Indianapolis'
    elif areIntersected(coordinates, columbus):
        return 'Columbus'
    elif areIntersected(coordinates, seattle):
        return 'Seattle'
    elif areIntersected(coordinates, denver):
        return 'Denver'
    elif areIntersected(coordinates, detroit):
        return 'Detroit'
    elif areIntersected(coordinates, DC):
        return 'WashingtonDC'
    elif areIntersected(coordinates, boston):
        return 'Boston'
    elif areIntersected(coordinates, nashville):
        return 'Nashville'


def getCityID(cityName):
    if cityName == 'NewYork':
        return 5128638
    elif cityName == 'SanFrancisco':
        return 5391959
    elif cityName == 'LosAngeles':
        return 5368361
    elif cityName == 'Chicago':
        return 4887398
    elif cityName == 'Houston':
        return 4699066
    elif cityName == 'Philadelphia':
        return 5131095
    elif cityName == 'Phoenix':
        return 5308655
    elif cityName == 'SanAntonio':
        return 4726206
    elif cityName == 'SanDiego':
        return 5391811
    elif cityName == 'Dallas':
        return 4684888
    elif cityName == 'SanJose':
        return 5392171
    elif cityName == 'Austin':
        return 4099974
    elif cityName == 'Jacksonville':
        return 4160021
    elif cityName == 'Indianapolis':
        return 4259418
    elif cityName == 'Columbus':
        return 4509177
    elif cityName == 'Seattle':
        return 5809844
    elif cityName == 'Denver':
        return 5419384
    elif cityName == 'Detroit':
        return 4990729
    elif cityName == 'WashingtonDC':
        return 4497666
    elif cityName == 'Boston':
        return 4930956
    elif cityName == 'Nashville':
        return 4644585


# Class that defines the functionality of our listener
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.theTime = time.time()
        self.vectorDict = {}

    # This is executed each time a status is received
    def on_status(self, status):
        # Get the vector of emojis from the tweet
        tmpvector = extractEmojis(status.text)

        # Below code collects emojis for an hour and then adds them to the database
        if (time.time() < self.theTime + 7200):

            # All should have geographic location, but just in case, skip if they don't
            if status.place == None:
                return

            # Get city
            city = getCity(status.place.bounding_box.coordinates[0])

            # Skip if not in one of our cities
            if city == None:
                return

            # If the city doesn't already have an entry in the dictionary, initialize it to zero
            if not city in self.vectorDict:
                self.vectorDict[city] = [0 for i in range(75)]

            # Add (element-wise) the vector of emojis from the current tweet to the preexisting vector
            self.vectorDict[city] = [sum(x) for x in
                                     zip(self.vectorDict[city], tmpvector)]
        else:

            # All should have geographic location, but just in case, skip if they don't
            if status.place == None:
                return

            # Get city
            city = getCity(status.place.bounding_box.coordinates[0])

            # Skip if not in one of our cities
            if city == None:
                return

            # If the city doesn't already have an entry in the dictionary, initialize it to zero
            if not city in self.vectorDict:
                self.vectorDict[city] = [0 for i in range(75)]

            # Add (element-wise) the vector of emojis from the current tweet to the preexisting vector
            self.vectorDict[city] = [sum(x) for x in
                                     zip(self.vectorDict[city], tmpvector)]

            for key, vector in self.vectorDict.items():
                # Create the list of data that will be inserted
                rowList = []
                rowList.append(str(time.ctime(self.theTime)))
                rowList.append(str(time.ctime(time.time())))
                rowList.append(key)
                for value in vector:
                    rowList.append(str(value))

                # Use pyowm to read in weather for each location
                weatherAPI = pyowm.OWM('7b2e89e5e4e4a8494dc1a2a6e9e19d3f')
                observation = weatherAPI.weather_at_id(getCityID(key))
                w = observation.get_weather()
                rowList.append(w.get_temperature('fahrenheit')['temp'])
                rowList.append(w.get_status())

                print('Inserting... ' + str(rowList))
                # Perform the insert
                c.execute(
                    'INSERT INTO emojiWeather VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                    rowList)

                # Commit after each insert to avoid data loss
                c.commit()

            # Reset our time and clear emoji vectors
            self.theTime = time.time()
            self.vectorDict = {}


# Set authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Initialize the Stream
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

# Build list of all places
places = newYork + sanFran + LA + chicago + houston + philly + phoenix + sanAntonio + sanDiego + dallas + sanJose + austin + jacksonville + indianapolis + columbus + seattle + denver + detroit + DC + boston + nashville

# Begin streaming, will capture all tweets that came from one of our geographic locations
myStream.filter(locations=places)
