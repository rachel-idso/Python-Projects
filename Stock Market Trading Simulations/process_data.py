import requests
import json
import time
import os

'''
This file will be used to create csv files for the 10 tickers we will be trading.
We will save the csv files in the folder data. We only need to use this .py file once to 
create the csv files. After that, we can use append_data to add the new data to the csv
each day. 

'''

# get the data on 10 tickers from the internet and load it as a json file. 
tickers = ["ADBE", "AMZN", "AAPL", "COST", "DELL", "FB", "MSFT", "NKE", "TSLA", "WMT"]
#tickers = ["AAPL"]
for ticker in tickers:
    url = 'http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8'
    req = requests.get(url)
    time.sleep(12)
    #create a dictionary from the json file. 
    req_dict = json.loads(req.text)

    #print(req_dict.keys())

    key1 = "Time Series (Daily)" # dictionary with all prices by date
    key2 = '4. close'
# create a cvs file for each ticker
    csv_file = open("/home/ubuntu/environment/Final_Project/Data/" + ticker + ".csv", "w")
    csv_file.write("Date," + ticker + "\n")
    write_lines = []
    for date in req_dict[key1]:
        #print(date + "," + req_dict[key1][date][key2]) #print key, value
        write_lines.append(date + "," + req_dict[key1][date][key2]+"\n")
# reverse the order of the dates, so that we can easily append to the end of the file each day       
    write_lines = write_lines[::-1]
    csv_file.writelines(write_lines)
    csv_file.close()


