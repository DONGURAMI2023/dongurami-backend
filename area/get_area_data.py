import requests
import os
import json
from .models import Area

def get_data_from_open_api(year, month, law_code):
    url = 'http://apis.data.go.kr/1611000/nsdi/FluctuationRateofLandPriceService/attr/getByRegion'
    params ={'serviceKey' : os.environ['AREA_OPEN_API_KEY'], 'pageNo' : '1', 'numOfRows' : '10', 'stdrYear' : str(year), 'stdrMt' : str(month), 'reqLdCode' : str(law_code), 'scopeDiv' : 'B', 'format' : 'json' }
    response = json.loads(requests.get(url, params=params).content)
    return response['byRegions']['field'][0]['pclndIndex']

def insert_demo_data():
    with open('areafile.json', 'r') as f:
        area = json.load(f)
        for i in area['area']:
            price = float(get_data_from_open_api(2023, 7, i['law_code']))
            # exprimental value
            price_scale = int(pow(1.02, (price-99)*1000)//500000)
            Area.objects.get_or_create(id=i['id'], price=price_scale)
    return Area.objects.all()
