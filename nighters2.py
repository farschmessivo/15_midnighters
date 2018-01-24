import datetime
import requests
import pytz
import json


url = 'https://devman.org/api/challenges/solution_attempts/?page=1'
user_objects = requests.get(url)

users = []

for u_object in user_objects:
    json.dump(u_object, users)

print(users)


#json.dumps(users)

print(type(users))