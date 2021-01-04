# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 00:02:04 2020

@author: donia
"""

import pandas as pd
import json
with open('./all_coins.json','r') as fp:
    json_fp = json.load(fp)
data = json_fp['data']
coin_list = []
coin_df = pd.DataFrame.from_dict(data)
coin_df.drop(columns = ['platform','is_active', 'id', 'rank'], inplace = True)
#这里是在处理时间
#要不这个时间就不用了，主要是有个币缺失了
#而且意义不大
#for index, row in coin_df.iterrows():
#    row['first_historical_data'] = row['first_historical_data'][0:10]
#    row['last_historical_data'] = row['last_historical_data'][0:10]
coin_df['history_has_been_saved'] = 0
coin_df.to_csv('coin_df.csv', index = False)