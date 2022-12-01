import requests

# Hae JSON-dataa osoitteesta https://api.github.com/search/repositories?q=language:python (voit ensin kurkata vaikka
# selaimella millaista dataa osoitteesta löytyy)

data = requests.get('https://rata.digitraffic.fi/api/v1/metadata/stations')
data_dict = data.json()
#Tulosta data rivi kerrallaan, seuraavassa muodossa:
# {forks}. {name}: {description}
for row in data_dict:
    print(f"{row['stationName']}. {row['stationShortCode']}")


# ⭐Järjestä tuloksena saadut vastaukset ”forks” –arvon mukaan laskevassa järjestyksessä
forks_sort = []
for row in data_dict:
    forks_sort.append([row['stationName'], row['stationShortCode']])
forks_sorted = sorted(forks_sort, key=lambda tup: tup[0])
for row in forks_sorted:
    print(f"{row[0]}. {row[1]}")
