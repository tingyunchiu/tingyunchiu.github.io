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
# data players gender birthday year rating 
# link example: https://www.goratings.org/en/history/1980-01-01.html
result =[]  
for yr in range(1980, 2022):
    print(yr) 
    if yr % 10 ==0:
        time.sleep(10)
    year = yr
    url = 'https://www.goratings.org/en/history/'+ str(year) + '-01-01.html'
    # 取得table each row
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    data = soup.find('table')

    # data clean 抓 姓名、性別、年分、ranking、積分
    # data clean 抓 1000強的排名、姓名、性別、目前積分
    
    for tr in data:
        if len(tr.findAll('td'))>2:
        
            result.append( {# 只儲存 Date 跟 Rating
            'Year': year,
            'Rank': tr.findAll('td')[0].text,
            'Name': tr.findAll('td')[1].text,
            'Gender':  tr.findAll('td')[2].text,
            'Country': tr.find('img', alt= True).get('alt'),
            'Rating':  tr.findAll('td')[4].text,            
            }
            )
    time.sleep(5)        
        
# 轉換成 Data Frame
df1 = pd.DataFrame(result)  
# record gender
df1.Gender = df1.Gender.map({"â\x99\x80": "female", 
       "â\x99\x82": "male"})
# save
#f = '1980to2021.csv'
#df1.to_csv(f, index=False)


# 抓選手生日
bd =[]
for pl in range(1,3000): 
    print (pl)
    if pl % 200 ==0:
        time.sleep(120)
    
    link = 'https://www.goratings.org/en/players/' + str(pl) + '.html'
    
    req = requests.get(link)
    soupB = BeautifulSoup(req.text, "html.parser")
    
    nm = soupB.find('title').text
    dta = soupB.find('table').findAll('td')[-1].text 
    bd.append({
           'Name': nm,
           'Birthday': dta
           })
    

 
# 轉換成 Data Frame
df2 = pd.DataFrame(bd)        
#df2.to_csv('birthday.csv', index=False)  







        