from bs4 import BeautifulSoup
import requests, lxml
import unicodedata
import time
from datetime import datetime as dt
import csv

work = "advanced photon source, IL"
#half1 = "distance between nashville, tn, and "
locations = [
        "wicker park, chicago",
        "roscoe village, chicago",
        "ukrainian village, chicago",
        "logan square, chicago",
        "lincoln park, chicago",
        "gold coast, chicago"
        ]

def get_routes():
    routes_list = [[] for i in range(len(locations))]
    fastest_times = [[] for i in range(len(locations))]
    
    j=0
    for location in locations:
        if dt.now().hour < 12:
            search_str = "distance between " + location + " and " + work
        else:
            search_str = "distance between " + work + " and " + location 

        params = {
            "q": search_str,
            "hl": "en",
        }
    
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4758.87 Safari/537.36",
            }
        
        html = requests.get("https://www.google.com/search", params=params, 
                headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, "lxml")
    
        # first index = location
        routes_list[j].append(location) 
        fastest_times[j].append(location) 
    
        #print(location)
        
        # add full results string to routes_list for each location
        for result in soup.select(".uE1RRc"):
            routes_list[j].append(unicodedata.normalize("NFKD", result.text)) 
             
        # for fastest_times, we just want format: location, route minutes, date
        # routes_list[j][1] has the full results string
        # possible format examples: "1 hr", "1 hr 4 min", "40 min"
        if "min" in routes_list[j][1]:
            fast = routes_list[j][1].split(" min")[0]
            if "hr" in routes_list[j][1]:
                fast_split = fast.split(" hr ")
                fastest_times[j].append(int(fast_split[0])*60 + int(fast_split[1]))
            else:
                fastest_times[j].append(int(fast))
        elif "hr" in routes_list[j][1]:
            fast = routes_list[j][1].split(" hr")[0]
            fastest_times[j].append(int(fast)*60)
        
        # add date to last index per location of both lists
        routes_list[j].append(dt.now()) 
        fastest_times[j].append(dt.now()) 
    
        j += 1

    return routes_list, fastest_times


#interval_sec = 5*60
interval_sec = 30 

if __name__ == '__main__':
    temp_hr = 0
    while True:
        if dt.now().hour != temp_hr:
            temp_hr = dt.now().hour
            print(dt.now())

        # choose hours to grab data
        if dt.now().hour in range(8,11) or dt.now().hour in range(13,24):
            routes_list, fastest_times = get_routes()
            #for route in routes_list:
            #    print(route)
            #for route in fastest_times:
            #    print(route)

            with open("fast_routes.csv", "a", encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                for route in fastest_times:
                    writer.writerow(route)
            
            with open("fast_routes_full.csv", "a", encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                for route in routes_list:
                    writer.writerow(route)
            
            time.sleep(interval_sec)
        else:
            time.sleep(10)




