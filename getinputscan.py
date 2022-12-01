import requests
import json
import logging
import boto3
import uuid

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Käytetään Digitraficin rajapintaa, josta haetaan Tampereen juna-aseman reaaliaikaista aikataulu tietoa
# Lisäksi OpenAPIWeather rajapinnasta haetaan Tampereen reaaliaikainen säätietoa.

def lambda_handler(event, context):
    logger.info(requests.__version__)
    data = requests.get('https://rata.digitraffic.fi/api/v1/live-trains/station/TPE')
    data2 = requests.get('https://api.weatherapi.com/v1/current.json?key=b1de5ace880e458ba11220248223011&q=Tampere&aqi=no')
    
    dynamodb = boto3.resource('dynamodb')
    
    data_dict = data.json()
    data2_dict = data2.json()
    
    station_sort = []
    late = []
    early = []
    for train in data_dict:
        for row in train['timeTableRows']:
            
            if "differenceInMinutes" in row and row['stationShortCode'] == 'TPE':
    
                difference = row['differenceInMinutes']
                if difference < 0: 
                    early.append(difference)
                elif difference > 0: 
                    late.append(difference) 
    
    late_all = sum(late)
    early_all = sum(early)
    
    late_hours = late_all  
    early_hours = (early_all) * -1
    round_late = str(round(late_all, ndigits= 1))
    round_early = str(round(early_all, ndigits= 1))
    
    value_saa2 = str(data2_dict['location']['name'])
    value_saa = str(data2_dict['current']['temp_c'])
    value_time = str(data2_dict['current']['last_updated'])
   
    # Rajapinnoista haetut Tampereen juna-aseman aikataulutiedot ja säätiedot lisätään DynamoDB:hen
    table = dynamodb.Table('Information')
    id = str(uuid.uuid4())
    data = table.put_item(
       Item={
            'Id': id,
            'Early(min)': round_early,
            'Late(min)': round_late,
            'Location' : value_saa2,
            'Temperature(C)': value_saa,
            'Date' : value_time,
        }
    )
    
    response = {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }
    
    return response