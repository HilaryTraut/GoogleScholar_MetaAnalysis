#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: HJTraut
"""

import requests, time, datetime, pandas as pd
from bs4 import BeautifulSoup as bs
from random import randint


lnk = []; ttl = []; athr = []; pub = []

for j in range(0,10400,10):
    url = "https://scholar.google.com/your/search/here"
    
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    
    
    for entry in soup.find_all("div", {'class': 'gs_ri'}):
        #Title information
        title_obj = entry.find('h3', {'class': 'gs_rt'})
        title_link = title_obj.find('a').get('href'); lnk.append(title_link)
        title_text = title_obj.find('a').get_text(); ttl.append(title_text)
        
        #Author information
        au_obj = entry.find("div", {'class': 'gs_a'})
        au_ls = au_obj.get_text(); athr.append(au_ls)
        yr = [int(s) for s in au_ls.split() if s.isdigit()]; pub.append(yr)
    
    time.sleep(randint(10,120))
    
    print("Result: " + str(j) + " at " + str(datetime.datetime.now()))

#build output
df = pd.DataFrame({'links' : lnk, 'titles' : ttl, 'authors' : athr, 'year' : pub})
df.to_csv("your_output_here.csv")
