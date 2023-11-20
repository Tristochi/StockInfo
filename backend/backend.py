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
    print(API_KEY)
    print(request.method)

    if request.method == "GET":
        some_data = theDB.get_search_history()
        return flask.Response(response = some_data, status=200)
    if request.method == "POST":
        ticker = request.get_json()["data"].upper()
        print(ticker)
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&apikey='+API_KEY
        api_call = requests.get(url)
        data = api_call.json()

        #Data is not recorded for the weekends so careful not to break the site
        if today in data["Time Series (Daily)"]:
            current_data = data["Time Series (Daily)"][today]
        else:
            current_data = data["Time Series (Daily)"][yesterday]

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