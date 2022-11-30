import requests

#Haetaan Digitraficin rajapinnasta kaikki juna-asemat

data = requests.get('https://rata.digitraffic.fi/api/v1/metadata/stations')
data_dict = data.json()
for row in data_dict:
    print(f"{row['stationName']}. {row['stationShortCode']}")

station_sort = []
for row in data_dict:
    station_sort.append([row['stationName'], row['stationShortCode']])
station_sorted = sorted(station_sort, key=lambda tup: tup[0])
for row in station_sorted:
    print(f"{row[0]}. {row[1]}")