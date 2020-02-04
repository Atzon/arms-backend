import requests
import json


url = "http://localhost:3000/api/points"


with open('points.json') as json_file:
    data = json.load(json_file)

    for measurement in data:
        requests.post(url, json=measurement)
