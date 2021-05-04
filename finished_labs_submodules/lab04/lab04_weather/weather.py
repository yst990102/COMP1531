import datetime
import csv


def weather(date, location):
    # A date in the format "DD-MM-YYYY"
    # need to reverse date
    date_cmp = "-".join(date.split("-")[::-1])

    infos = []
    with open('weatherAUS.csv', 'r') as myFile:
        lines = csv.reader(myFile)
        infos = [line[0:4] for line in lines]

    dates = []
    min_s = []
    max_s = []
    for info in infos:
        if info[1] == location and (info[2] != 'NA') and (info[3] != 'NA'):
            dates.append(info[0])
            min_s.append(float(info[2]))
            max_s.append(float(info[3]))
            
    min_sum = sum(min_s)
    max_sum = sum(max_s)

    average_min = round(min_sum / len(min_s), 1)
    average_max = round(max_sum / len(max_s), 1)

    min_temp = min_s[dates.index(date_cmp)]
    max_temp = max_s[dates.index(date_cmp)]

    diff_min = round(average_min - min_temp, 1)
    diff_max = round(average_max - max_temp, 1)

    return (diff_min, diff_max)


class LocationMissing(Exception):
    pass
