import urllib.request
import json
import csv
import time
import datetime
import sys

token = "091d2352892783ce2d50e3827c1f898aa5761be5"

def get_station_json(uid):
    url = "http://api.waqi.info/feed/@" + str(uid) + "/?token=" + token
    # print(url)
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        print(data)
        return data

def download_and_save_stations(number=1, uid=None):
    # Add header and open csv
    filename = 'stations' + str(number) + '_' + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + '.csv'
    csvfile = open(filename, 'w')
    keys = ['UID', 'Lat', 'Lon', 'CO', 'PM10', 'PM25', 'AQI']
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()

    if (uid):
        start = uid
        number = uid + number
    else:
        start = 0

    for uid in range(start, number):
        print("--- UID: %d --- %s seconds ---" % (uid, time.time() - start_time))
        station = {}
        station_json = get_station_json(uid)
        if station_json["data"].get("status") == 'error':
            continue
        if station_json["data"]["idx"] < 0:
            continue
        station["UID"] = station_json["data"]["idx"]
        if station_json["data"].get("city") is not None:
            if station_json["data"]["city"].get("geo") is not None:
                station["Lat"] = station_json["data"]["city"]["geo"][0]
                station["Lon"] = station_json["data"]["city"]["geo"][1]
        else:
            continue
        if station_json["data"].get("iaqi") is not None:
            if type(station_json["data"]["iaqi"]) is dict:
                for pollution in station_json["data"]["iaqi"].keys():
                    if pollution == "co":
                        station["CO"] = station_json["data"]["iaqi"]["co"]["v"]

                    if pollution == "pm25":
                        station["PM25"] = station_json["data"]["iaqi"]["pm25"]["v"]

                    if pollution == "pm10":
                        station["PM10"] = station_json["data"]["iaqi"]["pm10"]["v"]

        if station_json["data"]["aqi"] != '-':
            station["AQI"] = station_json["data"]["aqi"]

        writer.writerow(station)

    csvfile.close()


print(len(sys.argv))
start_time = time.time()
num = 9000
uid = 0
if (len(sys.argv) > 1):
    num = int(sys.argv[1])

print("Downloading {} stations.".format(str(num)))
download_and_save_stations(num, uid=uid)