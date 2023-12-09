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
content = x.get_search_history('AAP')

if not content:
    print("TIcker doesn't exist")
else:
    print(json.dumps(json.loads(content), indent=4))

data = json.loads(content)
co_name = list(data.keys())[0]
date_list = list(data[co_name])
close_list = []
for val in range(len(date_list)):
    close_list.append(data[co_name][date_list[val]]["Close"])

#print(date_list)
#print(close_list)

#create new dictionary through list comprehension that would be sent back to the frontend
response = {date_list[i]: close_list[i] for i in range(len(date_list))}
print(response)

