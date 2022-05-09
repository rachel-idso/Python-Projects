import matplotlib.pyplot as plt
import networkx as nx
from networkx.classes.function import path_weight
import requests
import json
from itertools import permutations
from itertools import combinations

# We will be using real time data from coingecko.com. This is the URL with the exchange rates we will need. 
url = 'https://api.coingecko.com/api/v3/simple/price?ids=ripple%2Ccardano%2Cbitcoin-cash%2Ceos%2Clitecoin%2Cethereum%2Cbitcoin&vs_currencies=xrp%2Cada%2Cbch%2Ceos%2Cltc%2Ceth%2Cbtc'

# These are the ids and currencies we will loop through: 
ids = ['ethereum', 'ripple', 'bitcoin', 'litecoin', 'eos', 'bitcoin-cash', 'cardano']
vs_currencies = ['eth', 'xrp', 'btc', 'ltc', 'eos', 'bch', 'ada']

# this saves the information from the api in a dictionary
req = requests.get(url)
dct = json.loads(req.text)

edges = []

# For each pair of currencies we will save their names and their rates to a list called edges
i=0
for c1 in ids: 
    j=0
    for c2 in vs_currencies: 
        if i != j: 
            try: # we need a try and except clause here because sometimes there aren't always paths to and from each currency
                edges.append((vs_currencies[i], vs_currencies[j], dct[c1][c2]))
            except: 
                pass
        j +=1
    i+= 1
    
g = nx.DiGraph()

# Now we use the list above to create the nodes and edges of our graph
g.add_weighted_edges_from(edges)

pos=nx.circular_layout(g)
nx.draw_networkx(g,pos)
labels = nx.get_edge_attributes(g,'weight')
nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
plt.savefig("graph.png")

# Now we will loop through the nodes and graphs to find each possible combination of paths

greatest_weight = -99999999
greatest_path = []
lowest_weight = 99999999
lowest_path = []

for n1, n2 in combinations(g.nodes,2):
    print("paths from ", n1, "to", n2, "----------------------------------")
    for path in nx.all_simple_paths(g, source=n1, target=n2):
        # This is the logic to go to the last currency in the path, multiplying each exchange rate/ path weight as we go
        
        path_weight_to = 1
        for i in range(len(path)-1):
            # print("edge from",path[i],"to",path[i+1],": ",g[path[i]][path[i+1]]["weight"])
            path_weight_to *= g[path[i]][path[i+1]]["weight"]
        
        print(path, path_weight_to)
        
        # Now that we've reached the end of the path, we need to go back to the currency we started with.
        # To do that we just reverse the path.
        path.reverse()
        
        # Again we multiply the weights of all the edges as we go along the path.
        path_weight_from = 1
        for i in range(len(path)-1):
            # print("edge from",path[i],"to",path[i+1],": ",g[path[i]][path[i+1]]["weight"])
            path_weight_from *= g[path[i]][path[i+1]]["weight"]
        
        print(path, path_weight_from)
        
        # now we save the product of the path weights we got by going down and back along the path
        # this gives us the path weight factor
        path_weight_factor = path_weight_to * path_weight_from
        # print("path weight factor for path",path,": ",path_weight_factor)
        
        print(path_weight_factor)
        
    # This is how we save the highest and the lowest path so that we know which path had the highest arbitrage opportunity
    if path_weight_factor > greatest_weight:
        greatest_weight = path_weight_factor
        greatest_path = path
        
    if path_weight_factor < lowest_weight: 
        lowest_weight = path_weight_factor
        lowest_path = path

# and now we print the output for the highest and the lowest paths            
print("greatest path",greatest_path, "at weight: ", greatest_weight)
print("lowest path",lowest_path, "at weight: ", lowest_weight)

print(0)