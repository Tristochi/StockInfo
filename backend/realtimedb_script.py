import requests 
import json 
from RealtimeDB import RealtimeDB
import asyncio
import key_variables
#url = "https://stocksfirst-3f87d-default-rtdb.firebaseio.com/ticker_list.json"
#json_file = open("ticker_list.json")
#data = json.load(json_file)
#header = {"content-type": "application/json; charset=UTF-8"}
#r = requests.put(url, data = json.dumps(data,indent=4).encode("UTF-8"), headers=header)
#print((r.content))

x = RealtimeDB()
content = x.get_search_history('AAP')
API_KEY = key_variables.API_KEY

url = 'https://alphavantageapi.co/timeseries/analytics?SYMBOLS=IBM&RANGE=full&INTERVAL=DAILY&OHLC=close&CALCULATIONS=MIN,MAX,MEDIAN,MEAN&apikey='+API_KEY

r = requests.get(url)
print(json.dumps(r.text, indent=4))