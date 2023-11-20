import requests 
import json 

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
        r = requests.put(link, data = json_data, headers = header)
        print(r.content)


        
