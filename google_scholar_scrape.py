#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: HJTraut
"""

import requests, time, re, pandas as pd

from bs4 import BeautifulSoup as bs
from selenium import webdriver

#set-up driver
driver_location = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(driver_location)

lnk = []; ttl = []; athr = []; ct = []

for j in range(0,10400,10):
    url = "https://scholar.google.com/your/search/here"
    
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    
    driver.get(url)
    
    #pull cite_button
    cite_buttons = driver.find_elements_by_class_name("gs_or_cit")
    
    for entry in soup.find_all("div", {'class': 'gs_ri'}):
        #Title information
        title_obj = entry.find('h3', {'class': 'gs_rt'})
        title_link = title_obj.find('a').get('href'); lnk.append(title_link)
        title_text = title_obj.find('a').get_text(); ttl.append(title_text)
        
        #Author information
        au_obj = entry.find("div", {'class': 'gs_a'})
        au_ls = au_obj.get_text(); athr.append(au_ls)
    
    for i in range(0,len(cite_buttons)): 
        #click cite_button
        driver.execute_script("arguments[0].click();", cite_buttons[i])
        
        #find citation information
        citation_wrapper = driver.find_element_by_id("gs_cit-bdy")
        time.sleep(4)
        
        #pull the table
        citations = citation_wrapper.find_elements_by_tag_name("tr")
        html = citation_wrapper.get_attribute("innerHTML")
        split_html = html.split("<tr>")
        
        #clean up apa citation
        apa = re.sub('<[^>]+>','',split_html[2]); apa = re.sub('APA','',apa)
        ct.append(apa)
            
        #close popup
        close_buttons = driver.find_elements_by_class_name("gs_btnCLS")
        close_buttons[0].click()

#build output
df = pd.DataFrame({'links' : lnk, 'titles' : ttl, 'authors' : athr, 'citation' : ct})
df.to_csv("your_output_here.csv")

driver.quit()
