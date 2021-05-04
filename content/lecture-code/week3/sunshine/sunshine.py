import csv

with open('./weatherAUS.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    locationInfo = {}
    for row in csv_reader:

        line_count += 1
        if line_count > 1:

            location = row[1]
            try:
                rainfall = float(row[4])
            except ValueError:
                rainfall = 0

            if location not in locationInfo:
                locationInfo[location] = 0

            locationInfo[location] += rainfall

    locationSummary = []
    for locationTuple in locationInfo.items():
        locationSummary.append(locationTuple)

    locationSummary.sort(key = lambda x: x[1], reverse=True)

    for location, rainfall in locationSummary[:5]:
        print(f"{location}: {round(rainfall)}")