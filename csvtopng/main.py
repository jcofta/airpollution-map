import csv
from skimage.draw import circle
import numpy as np
from PIL import Image

MAP_WIDTH = 4000
MAP_HEIGHT = 2000


def coordinates_to_xy(lat, lon):
    x = (MAP_WIDTH / 360.0) * (180 + lon)
    y = (MAP_HEIGHT / 180.0) * (90 - lat)
    return int(x), int(y)


def read_from_csv(filename):
    stations = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        # rownum = 0

        for rownum,row in enumerate(reader):
            if rownum == 0:
                header = row
            else:
                station = row
                stations.append(station)

    return stations


def gradient(value, max):
    if value > max:
        value = 1
    else:
        value = value / max
    red = 0
    green = 0
    blue = 0
    if 0 <= value < 0.5:
        blue = 1 - 2 * value
        green = 2 * value
        red = 0
    elif 0.5 <= value <= 1:
        blue = 0
        green = 1 - 2*(value - 0.5)
        red = (value - 0.5) * 2
    return [red*255, green*255, blue*255]

pollutions = {
    'co' : [3, 300],
    'pm10' : [4, 300],
    'pm25' : [5, 300],
    'aqi': [6, 300]
}

def generate_point_map(stations, selected_poll='aqi'):
    pollution_map = np.zeros((MAP_HEIGHT, MAP_WIDTH, 4), dtype=np.uint8)
    pollution_index = pollutions[selected_poll][0]
    for station in stations:
        print(station)
        if station[1] == '':
            continue
        else:
            lat = float(station[1])

        if station[2] == '':
            continue
        else:
            lon = float(station[2])

        if station[pollution_index] == '':
            continue
        value = float(station[pollution_index])

        # Reject failed data
        if -90 > lat or lat > 90:
            continue
        if -180 > lon or lon > 180:
            continue

        x, y = coordinates_to_xy(lat, lon)
        rr, cc = circle(y,x,5)
        color = gradient(value, pollutions[selected_poll][1])
        color.append(200)
        pollution_map[rr, cc] = color

    return pollution_map



def main():
    filename = 'stations9000'
    all_stations = read_from_csv('../data_downloader/'+filename+'.csv')

    for pollution in pollutions.keys():
        worldmap = generate_point_map(all_stations, pollution)
        img = Image.fromarray(worldmap, 'RGBA')
        img.save(filename + '_' + pollution + '.png')

main()
