import sqlite3
import pickle

# Connect to database
conn = sqlite3.connect('../data/emojiDatabase.db')
c = conn.cursor()

emojiVectors = []
atmosphericConditions = []

def reclassifyAtmosphere(str):
    if str == 'Clear':
        return 0
    elif str == 'Rain':
        return 1
    elif str == 'Drizzle':
        return 2
    elif str == 'Mist':
        return 3
    elif str == 'Fog':
        return 4
    elif str == 'Snow':
        return 5
    elif str == 'Haze':
        return 6
    elif str == 'Dust':
        return 7

    return -1

for row in c.execute('select * from emojiWeather;'):
    emojiVector = [int(value) for value in row[3:-2]]
    if sum(emojiVector) < 40:
        continue

    atmosphere = reclassifyAtmosphere(row[-1])

    if atmosphere == -1:
        continue

    emojiVectors.append(emojiVector)
    atmosphericConditions.append(atmosphere)

with open('../data/emojis.pickle', 'wb+') as file:
    pickle.dump(emojiVectors, file)

with open('../data/atmosphere.pickle', 'wb+') as file:
    pickle.dump(atmosphericConditions, file)

print(emojiVectors[0])
print(atmosphericConditions[0])