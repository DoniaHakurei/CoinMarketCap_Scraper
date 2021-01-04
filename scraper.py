# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 16:55:24 2020

@author: donia
"""
import json
import urllib.request as urllib
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import numpy as np
ua = UserAgent()

def make_a_url(curr = 'bitcoin', start = '20130429', end = '20201202'):
    url = 'https://coinmarketcap.com/currencies/' + curr + '/historical-data/?start=' + start + '&end=' + end
    return url
def get_a_page(curr = 'bitcoin', start = '20130429', end = '20201202'):
    url = make_a_url(curr, start, end)
    req = urllib.Request(url)
    #每次拉网页都要弄个新的虚假报头，感觉有点诡异
    req.add_header("User-Agent", ua.random)
    try:
        page = urllib.urlopen(req,timeout = 10)
    except:
        return -1
    else:    
        status = page.status
        if status == 200:
            return page
        else:
            return -1
#html = page.read()
#content = html.decode('utf-8')
def extract_data(curr = 'bitcoin', start = '20130429', end = '20201202'):
    page = get_a_page(curr, start, end)
    if page == -1:
        print(curr + '有点问题，可能是没请求到网页')
        return -2#页面没抓到
    try:
        bs = BeautifulSoup(page, 'html.parser')
    except:
        print(curr + '有点问题，可能是bs对象没建起来')
        return -3#bs没建起来
    else:
        result = bs.select('script[id="__NEXT_DATA__"]')
        result = result[0]
        result_con = result.contents
        dicts = json.loads(result_con[0])
        tabel = list((dicts['props']['initialState']['cryptocurrency']['ohlcvHistorical']).values())
        if len(tabel) == 0:
            print(curr + '的list有问题')
            return -5
        else:
            tabel = tabel[0]
        quotes = tabel['quotes'].copy()
        for index in range(0, len(quotes)):
            to_be_append = quotes[index]['quote']['USD']
            to_be_append['time_high'] = quotes[index]['time_high']
            to_be_append['time_low'] = quotes[index]['time_low']
            to_be_append['time_close'] = quotes[index]['time_close']
            quotes[index] = to_be_append.copy()
            quotes[index]['timestamp'] = quotes[index]['timestamp'][0:10]
        if len(quotes) > 0:    
            return quotes
        else:
            print(curr + '的quote没拉到')
            return -1
def the_roll():
    #每次开始迭代之前都读取一下coin_df.csv
    #直到最后才把csv更新保存
    while True:    
        coin_df = pd.read_csv('./coin_df.csv')
        coins_to_down = list(coin_df[coin_df.history_has_been_saved != 1]['slug'])
        if len(coins_to_down) == 0:
            return 1
        slug = coins_to_down[0]
        tag = 0#准备保存到coin_df的标记
        pull_data = extract_data(curr = slug)
        try:
            if (pull_data not in [-1, -2, -5]):
                pull_to_csv = pd.DataFrame.from_dict(pull_data)
        except:
            tag = -4
            print(slug + "有点问题，可能是df没建起来") 
        else:
            if (pull_data in [-1, -2, -3, -5]):
                tag = pull_data
            else:
                tag = 1
                string = './data/' + slug + '.csv'
                pull_to_csv.to_csv(path_or_buf = string, index = False)
                print(slug + '成功保存了，喵喵喵')
        finally:
            coin_df.loc[coin_df['slug'] == slug, 'history_has_been_saved'] = tag
            coin_df.to_csv('./coin_df.csv', index = False)
            time.sleep(6 * np.random.random() + 3)
the_roll()
        