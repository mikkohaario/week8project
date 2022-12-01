import requests
import json

data = requests.get('https://rata.digitraffic.fi/api/v1/live-trains/station/TPE')
data2 = requests.get('https://api.weatherapi.com/v1/current.json?key=b1de5ace880e458ba11220248223011&q=Tampere&aqi=no')

data_dict = data.json()
data2_dict = data2.json()

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

late_all = sum(late)
early_all = sum(early)

late_hours = late_all / 60
early_hours = (early_all /60) * -1
round_late = round(late_hours, ndigits= 1)
round_early = round(early_hours, ndigits= 1)


value_saa2 = data2_dict['location']['name']
value_saa = data2_dict['current']['temp_c']


print(f"Today the train has been {round_late} hours late alltogether and {round_early} hours ahead of time and the current weather in Tampere is: {value_saa}")
