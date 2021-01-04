# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 21:22:41 2020

@author: donia
"""
"""
用来获取所有币的列表
"""
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
parameters = {
  'start':'1',
  'limit':'5000',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '喵喵喵',#写API密钥的地方,请自行替换
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)

with open('all_coins.json','w',encoding='utf-8') as file:
    file.write(json.dumps(data,indent=2,ensure_ascii=False))