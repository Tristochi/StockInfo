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
content = x.get_top_performer_data()

if content:
    print(json.dumps(content, indent=4))
    print(type(content))
    print(content[0])
else:
    print("Nope")
