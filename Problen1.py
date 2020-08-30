#96197f921ac1bab99e6873e90463e917
import requests as r
from pprint import pprint

url = 'https://api.openweathermap.org/data/2.5/weather'
params =  {'q': 'Moscow',
           'appid': '96197f921ac1bab99e6873e90463e917'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

resp = r.get(url=url,params=params, headers=headers, verify=False)
j_data = resp.json()
pprint(j_data)