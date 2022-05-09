import numpy
import json
import time
from datetime import datetime, timedelta
import alpaca_trade_api as tradeapi
import append_data
import config as cf

BASE_URL = "https://paper-api.alpaca.markets"

api = tradeapi.REST(key_id=cf.ALPACA_API_KEY,
                    secret_key=cf.ALPACA_SECRET_KEY, base_url=BASE_URL, api_version='v2')

current_date = str(datetime.now()).split(" ")[0]

append_data.append()

# define function meanReversionStrategy
def meanReversionStrategy(prices, last_date_str, ticker):
#    run strategy and output buys/sells, final profit, and final percentage returns
    i = 0
    avg = 0
    buy = 0
    first_buy = 0
    total_profit = 0
    
    # this calculates the 5 day moving average
    for price in prices: 
        if i >= 5:
            avg = (prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5]) / 5

            # this checks to see if the price that day is below the moving average
            # if it is, we buy the stock
            if price < (avg * 0.95) and buy == 0: 
                #print("buying at: ", price)
                buy = price
                
                #tells you to buy today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='buy', type='market', time_in_force='day')
                    print("You bought", ticker, "today.")
                    
                # else: 
                    # print("You don't have the most updated price for", ticker, "today. ")
                    
                #this tell us what the price of the first buy is
                if first_buy == 0:
                    #print("The price of your first buy is: ", price)
                    first_buy = price
                    
            # this checks to see if the price is above the moving average
            # if it is, we sell the stock
            elif price > (avg * 1.05) and buy != 0:

                #tells you to sell today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='sell', type='market', time_in_force='day')
                    print("You sold", ticker, "today.")
                    
                # else: 
                #     print("You don't have the most updated price for", ticker, "today. ")
                    
               # print("selling at: ", price)
                total_profit += price - buy
               # print("trade profit: ", (price - buy))
               # print("total profit:", total_profit)
                buy = 0
        
        i += 1

    # calculate the final profit procentage
    returns = (total_profit/first_buy) * 100

  #  print("total profit: ", total_profit) 
  #  print("returns: ", returns)
#    return profit and returns
    return total_profit, returns
    

# define function simpleMovingAverageStrategy
def simpleMovingAverageStrategy(prices, last_date_str, ticker):
#    run strategy and output buys/sells, final profit, and final percentage returns
    i = 0
    buy = 0
    tot_profit = 0
    first_buy = 0
    for price in prices:
        
        if i >= 5: # 5 day moving average
            avg = ( prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5] ) / 5
            # print("avg: ", avg)
            if price > avg and buy == 0:
                #print("buying at: ", price)
                buy = price
                
                #tells you to buy today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='buy', type='market', time_in_force='day')
                    print("You bought", ticker, "today.")
                    
                # else: 
                #     print("You don't have the most updated price for", ticker, "today. ")
                
                if first_buy == 0:
                    first_buy = price
                
            elif price < avg and buy != 0:
                
                #tells you to sell today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='sell', type='market', time_in_force='day')
                    print("You sold", ticker, "today.")
                    
                # else: 
                #     print("You don't have the most updated price for", ticker, "today. ")
                    
                #print("selling at: ", price)
                tot_profit += price - buy
                #print("trade profit: ", price - buy)
                buy = 0
            else:
                pass #do nothing
            
        i += 1
    #print("tot_profit: ", tot_profit)
    
    returns = (tot_profit/first_buy)

#    return profit and returns
    return tot_profit, returns
    
# define function bollinger bands
def BollingerBands(prices, last_date_str, ticker):
    i = 0
    buy = 0
    tot_profit = 0
    first_buy = 0
    for price in prices:
        if i >= 5: # 5 day moving average
            avg = ( prices[i-1] + prices[i-2] + prices[i-3] + prices[i-4] + prices[i-5] ) / 5
            # print("avg: ", avg)
            if price > avg * 1.05 and buy == 0:
                #print("buying at: ", price)
                buy = price
                
                #tells you to buy today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='buy', type='market', time_in_force='day')
                    print("You bought", ticker, "today.")
                    
                # else: 
                #     print("You don't have the most updated price for", ticker, "today. ")
                
                if first_buy == 0:
                    first_buy = price
                
            elif price < avg * 0.95 and buy != 0:
                
                #tells you to sell today
                if i == (len(prices)-1) and current_date == last_date_str:
                    api.submit_order(symbol=ticker, qty=1, side='sell', type='market', time_in_force='day')
                    print("You sold", ticker, "today.")
                    
                # else: 
                #     print("You don't have the most updated price for", ticker, "today. ")
                
                #print("selling at: ", price)
                tot_profit += price - buy
               # print("trade profit: ", price - buy)
                buy = 0
            else:
                pass #do nothing
            
        i += 1
  #  print("tot_profit: ", tot_profit)
    
    returns = (tot_profit/first_buy)

#    return profit and returns
    return tot_profit, returns
    
# define function saveResults
def saveResults(results):
  #  print(results)
    json.dump(results, open("/home/ubuntu/environment/Final_Project/results.json", "w"))
    

# list to store 10 tickers
tickers = ["ADBE", "AMZN", "AAPL", "COST", "DELL", "FB", "MSFT", "NKE", "TSLA", "WMT"]
# tickers = ["AAPL"]
# dictionary called results to store prices, profits, return percentages and highest returns
results = {}
# loop through the list of tickers
#   - load prices from a file <ticker>.txt, and store them in the results dictionary 
#     with the key “<ticker>_prices”

#variables to find the highest returns
highest_returns = 0
highest_returns_ticker = ()
highest_returns_stragtey = ()

for ticker in tickers:
    cvs_file = open("/home/ubuntu/environment/Final_Project/Data/" + ticker + ".csv")
    lines = cvs_file.readlines()[1:]
    
    csv_file = open("/home/ubuntu/environment/Final_Project/Data/" + ticker + ".csv", "r")
    last_date_str = csv_file.readlines()[-1].split(",")[0]
    
    prices = [] 
    for line in lines:
        price = line.split(",")[1]
        prices.append(float(price))
        
#running mean reversion strategy
    profit, returns = meanReversionStrategy(prices, last_date_str, ticker)
    results[ticker + "_mr_profit"] = profit
    results[ticker + "_mr_returns"] = returns
    strategy = "Mean Reversion Strategy"
    
    #sets the highest return for all tickers as highest_returns
    #save which ticker, and which strategy earns highest return.
    if returns > highest_returns: 
        highest_returns = returns
        highest_returns_ticker = ticker
        highest_returns_stragtey = strategy
    
#running simple moving average strategy
    #results[ticker + "_prices"] = prices
    profit, returns = simpleMovingAverageStrategy(prices, last_date_str, ticker)
    results[ticker + "_sma_profit"] = profit
    results[ticker + "_sma_returns"] = returns
    strategy = "Simple Moving Average"
    
    #sets the highest return for all tickers as highest_returns
    #save which ticker, and which strategy earns highest return.
    if returns > highest_returns: 
        highest_returns = returns
        highest_returns_ticker = ticker
        highest_returns_stragtey = strategy

#running bolliger bands strategy
    profit, returns = BollingerBands(prices, last_date_str, ticker)
    results[ticker + "_bb_profit"] = profit
    results[ticker + "_bb_returns"] = returns
    strategy = "Bollinger Bands"
    
    #sets the highest return for all tickers as highest_returns
    #save which ticker, and which strategy earns highest return.
    if returns > highest_returns: 
        highest_returns = returns
        highest_returns_ticker = ticker
        highest_returns_stragtey = strategy

    #add the highest return to the results dictionary
    results["Highest Returns"] = highest_returns
    results["Highest Returns Ticker"] = highest_returns_ticker
    results["Highest Returns Strategy"] = highest_returns_stragtey
    
#save results    
saveResults(results)
