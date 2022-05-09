import requests
import json
import time
import os
 
   
'''
This file appends or adds the newest stick data to our csv files in the Data folder. 
Run this file at the beginning of every day before you run the trading simulation.

'''

# create a function to append new date on to each ticker   
def append():
    tickers = ["ADBE", "AMZN", "AAPL", "COST", "DELL", "FB", "MSFT", "NKE", "TSLA", "WMT"]

    for ticker in tickers: 
        url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8'
        req = requests.get(url)
        time.sleep(12)
        req_dict = json.loads(req.text)
        print(req_dict.keys())
    
        key1 = "Time Series (Daily)" # dictionary with all prices by date
        key2 = '4. close'
            
        # opening file and getting the last date
        # this will be used to know what dates, to add data to the file
        csv_file = open("/home/ubuntu/environment/Final_Project/Data/" + ticker + ".csv", "r")
        lines = csv_file.readlines()
        last_date = lines[-1].split(",")[0]
        
        new_lines = []
        for date in req_dict[key1]:
            if date == last_date:
                break
            print(date + "," + req_dict[key1][date][key2]) #print key, value
            new_lines.append(date + "," + req_dict[key1][date][key2]+"\n")
            
        new_lines = new_lines[::-1]
        csv_file = open("/home/ubuntu/environment/Final_Project/Data/" + ticker + ".csv", "a") # opening the file to append data
        csv_file.writelines(new_lines) # appending new data
        csv_file.close()

# append()