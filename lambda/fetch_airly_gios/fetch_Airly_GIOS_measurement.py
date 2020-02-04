import json
import boto3
import botocore
from datetime import datetime, timedelta
import urllib3
import os

AIRLY_KEY = os.environ['AIRLY_KEY']
AIRLY_DEVICES_URL = "https://airapi.airly.eu/v2/installations/nearest?lat=50.062006&lng=19.940984&maxDistanceKM=20" \
                    "&maxResults=1000 "
AIRLY_MEASUREMENT_URL = 'https://airapi.airly.eu/v2/measurements/installation?installationId='
AIRLY = "AIRLY"

GIOS = "GIOS"
GIOS_DEVICES_URL = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
GIOS_SENSOR_URL = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/"
GIOS_MEASUREMENT_URL = "http://api.gios.gov.pl/pjp-api/rest/data/getData/"


# returns gios stations from Krakow
def get_gios_devices():
    http = urllib3.PoolManager()
    r = http.request('GET', GIOS_DEVICES_URL)
    data = json.loads(r.data.decode('utf-8'))
    return [d for d in data if d["city"] is not None and d["city"]["name"] == "Kraków"]


# returns airly stations from the distance of 20km from Krakow center
def get_airly_devices():
    http = urllib3.PoolManager()
    r = http.request('GET', AIRLY_DEVICES_URL, headers={'apikey': AIRLY_KEY})

    stations = json.loads(r.data.decode('utf-8'))
    return stations


# get current measurement for station id
def get_measurement_airly(device_id):
    http = urllib3.PoolManager()
    r = http.request('GET', AIRLY_MEASUREMENT_URL + str(device_id), headers={'apikey': AIRLY_KEY})
    measurement = json.loads(r.data.decode('utf-8'))
    if not measurement.get("current"):
        return None, None
    return measurement["current"]["values"], measurement["current"]["fromDateTime"]


# save only new appeared station to database
def save_stations_to_db(device_type, ids, names, latitudes, longitudes):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Devices')
    for i in range(len(ids)):
        try:
            table.put_item(Item={
                'StationID': ids[i],
                'StationType': device_type,
                'StationName': names[i],
                'Latitude': str(latitudes[i]),
                'Longitude': str(longitudes[i]),
                'LastPushDate': prepare_date_to_save_in_db(datetime.utcnow() - timedelta(days=365))
            }, ConditionExpression="attribute_not_exists(StationID) AND attribute_not_exists(StationType)")
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
                raise


# save new sensors id for GIOS stations
def save_gios_sensor_to_db(sensors):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('SensorsGIOS')
    with table.batch_writer() as batch:
        for sensor in sensors:
            batch.put_item(
                Item={
                    'StationID': sensor["stationId"],
                    'SensorType': sensor["param"]["paramFormula"],
                    'SensorID': sensor["id"],
                }
            )


# get all stations from database
def read_stations_from_db():
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Devices')
    devices = table.scan()
    return devices["Items"]


#  read sensors id for GIOS stations
def read_sensors_form_db(stationID):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('SensorsGIOS')
    pm10id = table.get_item(
        Key={
            'StationID': stationID,
            'SensorType': "PM10"
        }
    )
    pm2_5id = table.get_item(
        Key={
            'StationID': stationID,
            'SensorType': "PM2.5"
        }
    )
    return {"pm10": pm10id['Item'] if "Item" in pm10id else None,
            "pm2_5": pm2_5id['Item'] if "Item" in pm2_5id else None}


#  check whether new stations/sensors appear
def update_devices():
    stations_GIOS = get_gios_devices()
    save_stations_to_db(GIOS,
                        list(map(lambda x: x["id"], stations_GIOS)),
                        list(map(lambda x: x["stationName"], stations_GIOS)),
                        list(map(lambda x: x["gegrLat"], stations_GIOS)),
                        list(map(lambda x: x["gegrLon"], stations_GIOS)))

    sensorID = get_sensorsid(stations_GIOS)
    save_gios_sensor_to_db(sensorID)

    stations_AIRLY = get_airly_devices()
    if "message" in stations_AIRLY:
        return {
            'statusCode': 404,
            'body': json.dumps(stations_AIRLY["message"])
        }
    save_stations_to_db(AIRLY,
                        list(map(lambda x: x["id"], stations_AIRLY)),
                        list(map(lambda x: x["address"]["street"], stations_AIRLY)),
                        list(map(lambda x: x["location"]["latitude"], stations_AIRLY)),
                        list(map(lambda x: x["location"]["longitude"], stations_AIRLY)))


def persist_measurement_airly(device_id):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Measurements')

    measurement, datetime = get_measurement_airly(device_id)
    if not measurement:
        return -1
    pm10 = next((x["value"] if (x["value"]) else -1 for x in measurement if x["name"] == "PM10"), None)
    pm25 = next((x["value"] if (x["value"]) else -1 for x in measurement if x["name"] == "PM25"), None)

    table.put_item(Item={
        'StationID': device_id,
        'StationType': AIRLY,
        'PM10': str(pm10),
        'PM2_5': str(pm25),
        'Datetime': datetime,
    })


#  get id for pm10 and pm2_5 for GIOS station
def get_sensorsid(stations):
    http = urllib3.PoolManager()
    sensors = []
    for station in stations:
        r = http.request('GET', GIOS_SENSOR_URL + str(station['id']))
        data = json.loads(r.data.decode('utf-8'))
        sensors.extend(
            [d for d in data if d["param"]["paramFormula"] == "PM10" or d["param"]["paramFormula"] == "PM2.5"])
    return sensors


def prepare_date_to_save_in_db(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def persist_measurement_gios(device):
    http = urllib3.PoolManager()
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('Measurements')

    ids = read_sensors_form_db(device["StationID"])
    last_push_date = datetime.strptime(device["LastPushDate"], "%Y-%m-%dT%H:%M:%S.%fZ")
    new_push_date = datetime.now()
    measurements = {}

    for sensor_id in ids:
        if ids[sensor_id] is not None:
            r = http.request('GET', GIOS_MEASUREMENT_URL + str(ids[sensor_id]["SensorID"]))
            response_measurements = json.loads(r.data.decode('utf-8'))["values"]
            for measurement in response_measurements:
                date_to_db = datetime.strptime(measurement["date"], "%Y-%m-%d %H:%M:%S") - timedelta(hours=1)
                if date_to_db >= last_push_date:
                    if measurement["value"] is not None:
                        if date_to_db not in measurements:
                            measurements[date_to_db] = {}
                        measurements[date_to_db][sensor_id] = measurement["value"]
                    else:
                        new_push_date = date_to_db
    with table.batch_writer() as batch:
        for key in measurements:
            batch.put_item(
                Item={
                    'StationID': device["StationID"],
                    'StationType': GIOS,
                    'PM10': str(measurements[key]["pm10"]) if "pm10" in measurements[key] else None,
                    'PM2_5': str(measurements[key]["pm2_5"]) if "pm2_5" in measurements[key] else None,
                    'Datetime': prepare_date_to_save_in_db(key),
                }
            )
    if new_push_date != last_push_date:
        table = dynamodb.Table('Devices')

        table.update_item(Key={
            'StationID': device["StationID"],
            'StationType': GIOS
        },
            UpdateExpression="set LastPushDate = :date",
            ExpressionAttributeValues={
                ':date': prepare_date_to_save_in_db(new_push_date)
            },
            ReturnValues="UPDATED_NEW"
        )


def get_measurements():
    stations = read_stations_from_db()
    for s in stations:
        if s["StationType"] == AIRLY:
            persist_measurement_airly(s["StationID"])
        if s["StationType"] == GIOS:
            persist_measurement_gios(s)


def lambda_handler(event, context):
    print("event")
    if event['event_type'] == "DEVICE_UPDATE":
        update_devices()
    if event['event_type'] == "GET_CURRENT_MEASUREMENTS":
        get_measurements()

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
