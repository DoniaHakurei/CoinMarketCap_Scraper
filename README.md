# CoinMarketCap_Scraper
##背景
完成作业时发现GitHub上的CMC爬虫都失效了，发现是CMC的CSS结构有所变化。所以写了个粗糙的爬虫。
学期结束了，分享给大家。

##文件说明
get_list_from_API.py: 采用CMC提供的API将所有币的URL友好名称下载下来
from_API_get_key_and_value.py: 进一步提取URL友好名称
scraper.py: 爬虫主体
coin_df.csv: 辅助文件，实现简单的断点续传功能
