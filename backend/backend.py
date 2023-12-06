from flask import Flask, request
from flask_cors import CORS 
import flask
import json
import requests
from datetime import datetime, timedelta 
from RealtimeDB import RealtimeDB 
import key_variables

theDB = RealtimeDB()
API_KEY = key_variables.API_KEY
yesterday = (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d')
today = datetime.today().strftime('%Y-%m-%d')

StocksFirst = Flask(__name__)
CORS(StocksFirst)

@StocksFirst.route("/", methods=["GET", "POST"])

def data():
    print("Data endpoint reached.")
    print(request.method)

    if request.method == "GET":
        url = 'https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey='+API_KEY

        #Check DB if top performer data is there
        #   Send data back to landing page
        if theDB.get_top_performer_data():
            print("There is data")
        else:
            api_call = requests.get(url)
            data = api_call.json()
            
            last_updated = data["last_updated"][0:10]
            tmp = list(data["top_gainers"])
            top_gainers = []
            for el in range(0, 4):
                top_gainers.append(tmp[el])
                
            
            tmp_dic = dict()
            tmp_dic[last_updated] = top_gainers
            
            theDB.write_top_performer_data(tmp_dic)

        
        return flask.Response(response = tmp_dic, status=200)
    
    if request.method == "POST":
        ticker = request.get_json()["data"].upper()
        print(ticker)
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey='+API_KEY
        api_call = requests.get(url)
        data = api_call.json()

        #Data is not recorded for the weekends so careful not to break the site

        days = list(data["Time Series (Daily)"])
        current_data = data["Time Series (Daily)"][days[0]]

        #if today in data["Time Series (Daily)"]:
            #current_data = data["Time Series (Daily)"][today]
        #else:
            #current_data = data["Time Series (Daily)"][yesterday]

        title = theDB.get_co_name(ticker)
        last_search = {ticker: {title: {"Open": current_data["1. open"], 
                                        "High": current_data["2. high"],
                                        "Low": current_data["3. low"],
                                        "Close": current_data["4. close"],
                                        "Volume": current_data["5. volume"]}}}
        
        theDB.write_search_history(last_search)
        return flask.Response(response= title + " (" + ticker + ")" + ": " + json.dumps(current_data, indent = 4),status=200)


if __name__ == "__main__":
    StocksFirst.run("localhost", 6969) 