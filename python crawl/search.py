# -*- coding: utf-8 -*-
"""
Spyder Editor: tingyunchiu

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
import openpyxl
import country_converter as coco


path = "D:\\NHRI\\google trend\\"
# read excel file that contains the search keywords
df = pd.read_excel(path + "49countries.xlsx", index_col=None,header=None)



# google trends
pytrend = TrendReq()
# country code convert
cc = coco.CountryConverter()
# where to put results
result_1 = pd.DataFrame()
result_2 = pd.DataFrame()
result_3 = pd.DataFrame()
result_4 = pd.DataFrame()
result_5 = pd.DataFrame()

for y in range(0,len(df)):
    target = df.iloc[y]
    co = cc.convert(names = target[0], to = 'ISO2') 
    for x in range (1,6):
          kw = list(target[x].split(','))  
          pytrend.build_payload(
            kw_list=kw,
            cat=0,
            timeframe='2019-01-01 2020-11-25',
            geo= co)
          data = pytrend.interest_over_time()
          if len(data)!=0:
            data = data.drop(labels=['isPartial'],axis='columns')
            cou = cc.convert(names = target[0], to = 'name_short') 
            for k in range(0,len(data.columns)):
                data.rename(columns={list(data)[k]:cou}, inplace=True)
            
            if x==1:
                result_1 = pd.concat([result_1, data], axis=1)
                
            elif x==2:
                result_2 = pd.concat([result_2, data], axis=1)
                
            elif x==3:
                result_3 = pd.concat([result_3, data], axis=1)
                
            elif x==4:
                result_4 = pd.concat([result_4, data], axis=1)
                
            elif x==5:
                result_5 = pd.concat([result_5, data], axis=1)
                  

result_1.to_excel(path + '49 countries\\' + 'handwash' + '.xlsx', index = True)
result_2.to_excel(path + '49 countries\\' + 'mask' + '.xlsx', index = True)
result_3.to_excel(path + '49 countries\\' + 'insonmia' + '.xlsx', index = True)
result_4.to_excel(path + '49 countries\\' + 'depression' + '.xlsx', index = True)
result_5.to_excel(path + '49 countries\\' + 'suicide' + '.xlsx', index = True)

                
