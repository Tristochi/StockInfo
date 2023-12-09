import requests
import json 
from datetime import datetime, timedelta
import asyncio

class RealtimeDB:
    """A class for handling interactions with the Realtime DB"""
    url = "https://stocksfirst-3f87d-default-rtdb.firebaseio.com/"

    def get_co_name(self, ticker):
        """
            Returns title (string) of provided ticker.
        """
        link = self.url + "ticker_list/"+ ticker + ".json"
        r = requests.get(link)
        title = r.text.strip('\"')
        
        return title 
    
    def write_search_history(self, last_search):
        """
            Keep track of most recent search history. 
            Will not write history if recently searched.
            Takes a dictionary, converts to JSON, writes it to db.
        """
        #TODO: Query db to see if last_search is already in last 10.

        #TODO: If not present, write to search history.
            #TODO: If there are already 10 recent searches, remove oldest first
        link = self.url+ "search_history.json"
        json_data = json.dumps(last_search, indent=4).encode("UTF-8")
        header = {"content-type": "application/json; charset=UTF-8"}
        r = requests.patch(link, data = json_data, headers = header)
        print(r.content)

    def get_search_history(self, ticker):
        #link = self.url + "search_history.json"
        #last_close_date = (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
        

        #check if ticker exists
        link = self.url + "search_history/" + ticker + ".json"
        r = requests.get(link)
        content = r.text 
        if content == "null":
            return None 
        
        return content 

    def get_graph_data(self, some_data):
        data = json.loads(some_data)
        co_name = list(data.keys())[0]
        date_list = list(data[co_name])
        close_list = []

        for val in range(len(date_list)):
            close_list.append(data[co_name][date_list[val]]["Close"])
        
        #Combine two lists into new dic using dict comprehension
        response = {date_list[i] : close_list[i] for i in range(len(date_list))}
        return response


    def get_top_performer_data(self):
        #Data is never for current data, but previous close date which is yesterday COB
        last_close_date = (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
        link = self.url + "top_performers/"+ last_close_date + ".json" 
        header = { 'User-Agent': '(Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0)',
                   'referer': self.url}
        
        r = requests.get(link)
        content = r.text
        print(content)
        
        if content == "null":
            #for i in range(1,5):
                #date = (datetime.today() - timedelta(days = i)).strftime('%Y-%m-%d')
                #link = self.url + "top_performers/"+ date + ".json" 
                #r = requests.get(link, headers=header)
                #if r.text != "null":
                    #return r.text
            return None 
        
        return content

    



    
    def write_top_performer_data(self, top_performers):
        #Check if we have data in the database already for today, or last few days
        # up to 4 to account for weekend use of app.
        print("Data for put request: ")
        print(json.dumps(top_performers, indent=4))
        link = self.url + "top_performers.json"
        json_data = json.dumps(top_performers, indent=4)
        header = {"content-type": "application/json; charset=UTF-8"}

        #r = requests.put(link, data=json_data, headers = header)
        r = requests.patch(link, data=json_data,headers=header)
        print("Response: ")
        print(r.content)


        
