import requests
import json


api_key = "eXWGyo10E1lZpwJND5XlmC4dmHVLHAjW"
headers = { 'apikey': api_key }

measurements_url = 'https://airapi.airly.eu/v2/measurements/installation?installationId='
installation_url = "https://airapi.airly.eu/v2/installations/nearest?lat=50.062006&lng=19.940984&maxDistanceKM=20&maxResults=1000"


def call_request(url):
    response = requests.get(url, headers=headers) 

    if(response.ok):
        return json.loads(response.content)
    else:
        response.raise_for_status()


def create_point(measurement, installation):

    pm10_index = next((i for i, item in enumerate(measurement['values']) if item["name"] == 'PM10'), -1)
    if pm10_index > 0: 
        pm10 = measurement['values'][pm10_index]["value"]
    else:
        pm10 = -1 

    pm25_index = next((i for i, item in enumerate(measurement['values']) if item["name"] == 'PM25'), -1)
    if pm25_index > 0: 
        pm25 = measurement['values'][pm25_index]["value"]
    else:
        pm25 = -1 

    return {
        'location':{
            'latitude': installation["location"]["latitude"], 
            'longitude': installation["location"]["longitude"]
        }, 
        'PM10': pm10, 
        'PM2_5': pm25, 
        'datetime': measurement['fromDateTime']
    }
def get_measurements_for_installations(installations):
    points = []
    for installation in installations:
        measurements = call_request(measurements_url + str(installation["id"]))["history"]
        for measurement in measurements:
            points.append(create_point(measurement, installation))
    
    return points 


points = get_measurements_for_installations(call_request(installation_url))


file = open('airly_points.json', 'w+')
file.write(json.dumps(points))
file.close()


