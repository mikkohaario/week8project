import requests
import json

#Haetaan Digitraficin rajapinnasta kaikki myohassa olleet minuutit,juna-asema Tampere

data = requests.get('https://rata.digitraffic.fi/api/v1/live-trains/station/TPE')
data_dict = data.json()

station_sort = []
late = []
early = []
for train in data_dict:
    for row in train['timeTableRows']:
        
        if "differenceInMinutes" in row:

            difference = row['differenceInMinutes']
            if difference < 0: 
                early.append(difference)
            elif difference > 0: 
                late.append(difference) 
# print(late)
# print(early)
late_all = sum(late)
early_all = sum(early)
# print(late_all)
# print(early_all)
late_hours = late_all / 60
early_hours = (early_all /60) * -1
round_late = round(late_hours, ndigits=1)
round_early = round(early_hours, ndigits=1)

print(f"Today the trains has been {round_late} hours late alltogether and {round_early} hours ahead of time")

#print(kokonais)


# for row in data_dict:
#     station_sort.append([row['scheduledTime'], row['actualTime']])
# station_sorted = sorted(station_sort, key=lambda tup: tup[0])
# for row in station_sorted:
#     print(f"{row[0]}. {row[1]}")


# ⭐Järjestä tuloksena saadut vastaukset ”forks” –arvon mukaan laskevassa järjestyksessä
# forks_sort = []
# for row in data_dict:
#     forks_sort.append([row['stationName'], row['stationShortCode']])
# forks_sorted = sorted(forks_sort, key=lambda tup: tup[0])
# for row in forks_sorted:
#     print(f"{row[0]}. {row[1]}")