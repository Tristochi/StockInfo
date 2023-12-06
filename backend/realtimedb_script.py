import requests 
import json 
from RealtimeDB import RealtimeDB
import asyncio
#url = "https://stocksfirst-3f87d-default-rtdb.firebaseio.com/ticker_list.json"
#json_file = open("ticker_list.json")
#data = json.load(json_file)
#header = {"content-type": "application/json; charset=UTF-8"}
#r = requests.put(url, data = json.dumps(data,indent=4).encode("UTF-8"), headers=header)
#print((r.content))

x = RealtimeDB()
async def get_result():
    result = await x.get_top_performer_data()
    print(result)