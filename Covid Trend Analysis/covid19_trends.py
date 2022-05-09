import requests
import json

# build the URL so that we can loop through it with the countries
url1 = "https://covid-api.mmediagroup.fr/v1/history?country="
url2 = "&status=confirmed"

# the countries we will loop through, and the keys we need from the dictionary
countries = ["US", "Russia", "Germany"]
key1 = 'All'
key2 = 'dates'

for country in countries: 

    url = url1 + country + url2
    
    print(url)
    
    # load the json file
    req = requests.get(url)
    dct = json.loads(req.text)
    
    # let's put the total cases and the dates into a list
    total_cases = []
    dates = []
    
    for date in dct[key1][key2]: 
        dates.append(date)
        total_cases.append(dct[key1][key2][date])
        
    dates.pop()
    
    #put the new cases in a list, but subtracting "today" from "yesterday"
    new_cases = []
    
    for i in range(len(total_cases)-1): 
        dif = total_cases[i]-total_cases[i+1]
        new_cases.append(dif)
    
 
    #calculate the average new cases
    average_new_cases = sum(new_cases)/len(new_cases)
    
    
    #find the date with the most high cases
    index = new_cases.index(max(new_cases))
    date_high_new = dates[index]
    
    #find the date when there were no new confirmed cases
    for i in range(len(new_cases)-1):
        no_new_confirmed = new_cases[i]
        if no_new_confirmed == 0: 
            date_no_new_conf = dates[i]
            break
            
    #create a dictionary for the monthly totals and respective dates
    month_dct = {}
    
    for i in range(len(new_cases)):
        if dates[i][:7] in month_dct.keys():
            month_dct[dates[i][:7]]+=new_cases[i]
        else:
            month_dct[dates[i][:7]]=new_cases[i]
            
    
    # separate the month_dct into two lists
    # one for the date, and one for the number of cases
    month_tot = []
    months = []
    
    for month in month_dct.keys(): 
        month_tot.append(month_dct[month])
        months.append(month)
        
    # find the month with the highest and lowest new confirmed cases
    index_max = month_tot.index(max(month_tot))
    index_min = month_tot.index(min(month_tot))
    
    month_max = months[index_max]
    month_min = months[index_min]
    
    # print the statistics
    print("Country name:", country) 
    print("Average number of new daily confirmed cases for the entire dataset:", average_new_cases)
    print("Date with the highest new number of confirmed cases:", date_high_new)
    print("Most recent date with no new confirmed cases: ", date_no_new_conf)
    print("Month with the highest new number of confirmed cases:", month_max)
    print("Month with the lowest new number of confirmed cases:", month_min, "\n")
    
    
    #save the statistics to a dictionary
    country_dct = {}
    
    #key-value pairs for the country dictionary
    country_dct["Country name"] = country
    country_dct["Average number of new daily confirmed cases for the entire dataset"] = average_new_cases
    country_dct["Date with the highest new number of confirmed cases"] = date_high_new
    country_dct["Most recent date with no new confirmed cases"] = date_no_new_conf
    country_dct["Month with the highest new number of confirmed cases"] = month_max
    country_dct["Month with the lowest new number of confirmed cases"] = month_min
        
    
    file = open("/home/ubuntu/environment/HW/HW3/" + country + ".json","w")
    file.write(str(country_dct))
