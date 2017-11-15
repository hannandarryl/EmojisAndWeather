import json
import requests
import sqlite3

api_token = "OzwtahbcTEexzzBFnosmWhbJsMBVQZLk"
url_base = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&locationid=ZIP:10023&startdate=2017-10-01&enddate=2017-10-31"


headers = {'token': api_token}
response = requests.get(url_base, headers=headers)
response = response.json()

print(response)
conn = sqlite3.connect('emojiDatabase.db')
c = conn.cursor()
# insert relevant data
conn.commit()
conn.close()