from datetime import datetime, timedelta, date
import requests
import time
import json
import objectpath
import datetime
import random

def generatePM():
        randomPM = random.uniform(1, 15)
        return randomPM, randomPM*2

oneLineData = []
def sniffOneLine(lineNumber):
        url = "https://krakowpodreka.pl/pl/vehicles/positions/"

        #querystring = {"newer_than":"1569662464","lines[]":"%s" % lineNumber,"lines%5B%5D":"%s" % lineNumber}
        querystring = {"newer_than":"1570440328","lines[]":["114","125","208","269","501"]}

        payload = ""
        headers = {
    'Host': "krakowpodreka.pl",
    'User-Agent': "PostmanRuntime/7.17.1",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "3d5ddc8a-d744-4a25-a7e3-0047ebdacfaf,6a0e1374-9f43-420b-a4e9-2fe6a2d8f349",
    'Accept-Encoding': "gzip, deflate",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
        }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        jsonnn_tree = objectpath.Tree(response.json())
        vehicles = tuple(jsonnn_tree.execute('$.positions'))
        for vehicle in vehicles:

                item = {"_id": vehicle["id"]}
                pm5, pm10 = generatePM()
                item["line_number"] = vehicle["line_number"]
                item["datetime"] = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                item["PM2_5"] = pm5
                item["PM10"] = pm10
                item["location"] = { "latitude" : vehicle["latitude"], "longitude" : vehicle["longitude"]}
                item["__v"] = 0
                oneLineData.append(item)

        jsonData=json.dumps(oneLineData,indent=4)
        print(jsonData)


def procedeSniffing(sniffTime):
        timeout = int(sniffTime)   # [seconds]

        timeout_start = time.time()

        while time.time() < timeout_start + timeout:
                test = 0
                if test == 5:
                        break

                sniffOneLine("173")
                time.sleep(10)
                test -= 1



        with open('oneLienData_%ss.json' % sniffTime, 'w') as outfile:
                json.dump(oneLineData, outfile, indent=4)


procedeSniffing("3600")