#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: HJTraut
"""

from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import pandas

#############################################################
def approx(query, choices, limit = 3):
    results = process.extract(query, choices, limit = limit,
                              scorer = fuzz.token_sort_ratio)
    return results                                               #list of tuples


df = pandas.read_csv('your_search_results_input_here.csv')       #readin csv

uniqueID = df['uniqueID'].tolist()                               #convert col to list
[str(i) for i in uniqueID]

titles = df['title'].tolist()                                    #convert col to list
[str(i) for i in titles]

#titles = ['abcdefg', 'hijklmna', 'qrshijk']                     #values
#uniqueID = [1, 2, 3]                                            #keys
lnk = dict(zip(uniqueID,titles))                                 #dict of uniqueID : titles

output = []                                                      #create empty output list

for i in range(0,len(titles)):
    match = approx(titles[i], lnk, limit = 3)
    catch = False
    print(i)
    
    while catch == False:                                        #con't searching thru list until none removed
        ol = len(match)
        
        for i in match:
            if i[1] < 95:
                match.remove(i)
        nl = len(match)
        
        if ol == nl:
            catch = True
    
    output.append(match)                                         #list of 3 element tuples: word, match%, and key

df_output = pandas.DataFrame(output)
df_output.to_csv("your_output_here.csv")
