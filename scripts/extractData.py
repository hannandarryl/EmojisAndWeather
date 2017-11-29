import sqlite3
import pickle

# Connect to database
conn = sqlite3.connect('../data/emojiDatabase.db')
c = conn.cursor()

emojiVectors = []
atmosphericConditions = []

def reclassifyAtmosphere(str):
    if str == 'Clear':
        return 1

    return 0

for row in c.execute('select * from emojiWeather;'):
    emojiVector = [int(value) for value in row[3:-2]]
    if sum(emojiVector) < 40:
        continue

    emojiVectors.append(emojiVector)

    atmosphere = reclassifyAtmosphere(row[-1])
    atmosphericConditions.append(atmosphere)

with open('../data/emojis.pickle', 'wb+') as file:
    pickle.dump(emojiVectors, file)

with open('../data/atmosphere.pickle', 'wb+') as file:
    pickle.dump(atmosphericConditions, file)

print(emojiVectors[0])
print(atmosphericConditions[0])