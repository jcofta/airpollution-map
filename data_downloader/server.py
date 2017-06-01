import urllib.request
import json
import csv
import time

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
    filename = 'stations' + str(number) + '.csv'
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
        station = {}
        station_json = get_station_json(uid)
        station["UID"] = uid
        if station_json["data"]["city"]["geo"] != None:
            station["Lat"] = station_json["data"]["city"]["geo"][0]
            station["Lon"] = station_json["data"]["city"]["geo"][1]
        else:
            continue

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


start_time = time.time()
download_and_save_stations(9000)
# download_and_save_stations(1, uid=17)
print("--- %s seconds ---" % (time.time() - start_time))
