import csv


def read_from_csv(filename):
    stations = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)

        for rownum, row in enumerate(reader):
            if rownum == 0:
                header = row
            else:
                station = row
                stations.append(station)

    return stations


def create_prediction(filename1, filename2, filename3):
    stations1 = read_from_csv(filename1)
    stations2 = read_from_csv(filename2)
    stations3 = read_from_csv(filename3)

    print(len(stations3))
    print(len(stations2))
    print(len(stations1))

    csvfile = open('prediction.csv', 'w')
    keys = ['UID', 'Lat', 'Lon', 'CO', 'PM10', 'PM25', 'AQI']
    writer = csv.DictWriter(csvfile, fieldnames=keys)
    writer.writeheader()

    for i in range(0, len(stations1)):
        # print(stations1[0][1])
        tmp_station = {}

        if stations1[i][0] == '':
            tmp_station['UID'] = ''
        else:
            tmp_station['UID'] = stations1[i][0]

        if stations1[i][1] == '':
            tmp_station['Lat'] = ''
        else:
            tmp_station['Lat'] = stations1[i][1]

        if stations1[i][2] == '':
            tmp_station['Lon'] = ''
        else:
            tmp_station['Lon'] = stations1[i][2]

        if ((stations1[i][3] == '') or (stations2[i][3] == '') or (stations3[i][3] == '')):
            tmp_station['CO'] = ''
        else:
            value = (float(stations1[i][3]) + float(stations2[i][3]) + float(stations3[i][3])) / 3
            tmp_station['CO'] = value

        if ((stations1[i][4] == '') or (stations2[i][4] == '') or (stations3[i][4] == '')):
            tmp_station['PM10'] = ''
        else:
            value = (float(stations1[i][4]) + float(stations2[i][4]) + float(stations3[i][4])) / 3
            tmp_station['PM10'] = value

        if ((stations1[i][5] == '') or (stations2[i][5] == '') or (stations3[i][5] == '')):
            tmp_station['PM25'] = ''
        else:
            value = (float(stations1[i][5]) + float(stations2[i][5]) + float(stations3[i][5])) / 3
            tmp_station['PM25'] = value

        if ((stations1[i][6] == '') or (stations2[i][6] == '') or (stations3[i][6] == '')):
            tmp_station['AQI'] = ''
        else:
            value = (float(stations1[i][6]) + float(stations2[i][6]) + float(stations3[i][6])) / 3
            tmp_station['AQI'] = value

        writer.writerow(tmp_station)

    csvfile.close()


def main():
    filename1 = 'stations9000_2017-06-01_23:49.csv'
    filename2 = 'stations9000_2017-06-01_23:49.csv'
    filename3 = 'stations9000_2017-06-02_04:02.csv'

    create_prediction(filename1, filename2, filename3)


main()
