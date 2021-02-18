# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:21:52 2020

@author: ting
"""

# " pip install -U requests beautifulsoup4 lxml imageio wordcloud mlxtend ckiptagger[tf,gdown] # tfgpu for GPU support

import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv

# 2021/01/12
# History of Go Ratings from 1980 to 2021
# link example: https://www.goratings.org/en/history/1980-01-01.html
# contains a list of top players of the year as well as
# their ranking, gender, rating(whole-history rating), and country  

# to store the output
result =[]  
for yr in range(1980, 2022):
    # show current year
    print(yr)     
    # to prevent crashes, sleep for 10 secconds for every 10 requests
    if yr % 10 ==0:
        time.sleep(10)    
    # the year of request
    year = yr
    # build the request link
    url = 'https://www.goratings.org/en/history/'+ str(year) + '-01-01.html'
    # request url
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    data = soup.find('table')     
    for tr in data:
        # the first 'tr' is the title of the table and thus does not have any 'td' 
        if len(tr.findAll('td'))>2:        
            # add year, ranking, name, gender, country, rating into result
            result.append( {
            'Year': year,
            'Rank': tr.findAll('td')[0].text,
            'Name': tr.findAll('td')[1].text,
            'Gender':  tr.findAll('td')[2].text,               
            'Country': tr.find('img', alt= True).get('alt'), #Country is an img, so select the alt attribute to indicate country 
            'Rating':  tr.findAll('td')[4].text,            
            }
            )
      
        
# transform result to Data Frame
df1 = pd.DataFrame(result)  
# gender會出現路亂碼，record gender
df1.Gender = df1.Gender.map({"â\x99\x80": "female", 
       "â\x99\x82": "male"})
# save as csv
#f = '1980to2021.csv'
#df1.to_csv(f, index=False)

# note: df1 does not include birthday of the players
# so the second part is to retrieve birthday from each player's profile
# sample link for a player's profile is: 'https://www.goratings.org/en/players/1.html'
# at this point, there are not more than 3000 players in this dataset

# to save birthday of all players 
bd =[]
for pl in range(1,3000): 
    print (pl)
    # take a 2 minute break every 200 requests
    if pl % 200 ==0:
        time.sleep(120)
    link = 'https://www.goratings.org/en/players/' + str(pl) + '.html'
    # request url
    req = requests.get(link)
    soupB = BeautifulSoup(req.text, "html.parser")
    # name of the current player
    nm = soupB.find('title').text
    # birthday is the last column of the first table in the website
    dta = soupB.find('table').findAll('td')[-1].text 
    # add name and birthday into bd 
    bd.append({
           'Name': nm,
           'Birthday': dta
           }) 
# transform bd to Data Frame
df2 = pd.DataFrame(bd)
# save df2 as csv
#df2.to_csv('birthday.csv', index=False)  







        
