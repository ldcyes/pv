import akshare as ak
import requests


# 获取复权后A股数据，历史行情数据
# 接口: stock_zh_a_daily
# 目标地址: finance.sina.com.cn/realtime
# 描述: A股数据是从新浪财经获取的数据，历史数据按日频率更新
# 股票代码：000001（以平安银行为例）
# 开始日期：'20230101'
# 结束日期：'20230301'
# 返回数据类型：DataFrame

# 设置日期格式

# 获取数据
#stock_data = ak.stock_zh_a_daily(symbol="SOXX", start_date="20240301", end_date="20240314", adjust="qfq")
#import akshare as ak
#
#stock_us_hist_df = ak.stock_us_hist(symbol='105.SOXX', period="daily", start_date="20200101", end_date="20240314", adjust="qfq")
#stock_name = ak.stock_us_spot_em()
#stock_name.to_csv("stock_data/stock_name.csv")
##print(stock_us_hist_df)
#stock_us_hist_df.to_csv("stock_data/SOXX_EAST.csv")
#stock_us_daily_df = ak.stock_us_daily(symbol="SOXX", adjust="qfq")
#print(stock_us_daily_df)
#stock_us_daily_df.to_csv("stock_data/SOXX_SINA.csv")
# 打印获取的数据
#print(stock_data)

#import tushare as ts
#pro = ts.pro_api("8a582d6c9595f2c88567f2c47774bb00f2e1bb4c37e5c2a5d40b2c80")
#
##获取单一股票行情
#df = pro.us_daily(ts_code='AAPL', start_date='20190101', end_date='20190904')
#
##获取某一日所有股票
#pre_close = df["pre_close"].values[0]
#print("使用tushare API获取SOXX 20240301号的前复权价格：", pre_close)



#import yfinance as yf
#
## 获取 SOXX 的历史数据
#soxx = yf.Ticker("AAPL")
#date = "2024-03-10"
## 获取复权的历史数据，period='max' 表示获取所有可用的历史数据
#soxx_history = soxx.history(start=date, end=date)
#
#print(soxx_history)


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AMD&apikey=1RQWLVEQ10FC5NL0'
#r = requests.get(url)
#data = r.json()

#print(data)

#cnt2utpr01qi1jjgks9gcnt2utpr01qi1jjgksa0

#from googlefinance import getQuotes
#import json
#print (json.dumps(getQuotes('AAPL'), indent=2))

#from googlefinance.client import get_price_data, get_prices_data, get_prices_time_data
#
## Dow Jones
#param = {
#	'q': ".AAPL", # Stock symbol (ex: "AAPL")
#	'i': "86400", # Interval size in seconds ("86400" = 1 day intervals)
#	'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
#	'p': "1Y" # Period (Ex: "1Y" = 1 year)
#}
## get price data (return pandas dataframe)
#df = get_price_data(param)
#print(df)


#from bs4 import BeautifulSoup
#
## 定义headers
#headers = {
#    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
#}
#
## 发送请求，获取响应内容
#response = requests.get('http://stock.finance.sina.com.cn/hkstock/quotesite/api/jsonp.php/StockInfoService.GetQuote?symbol=NVDA&_=1674503286935', headers=headers)
#print(response.content)
## 解析响应内容，获取股票信息
#soup = BeautifulSoup(response.content, 'html.parser')
#stock_info = soup.find('script').text.strip()[16:-1]
#stock_info_dict = eval(stock_info)
#
## 输出NVDA股票信息
#print("NVDA股票信息：")
#print("名称：", stock_info_dict['name'])
#print("代码：", stock_info_dict['symbol'])
#print("最新价格：", stock_info_dict['last'])
#print("涨跌额：", stock_info_dict['change'])
#print("涨跌幅：", stock_info_dict['percent'])

#	symbol：股票代码（前缀SZ表示深圳证券交易所，SH表示上海证券交易所）
#	begin：开始时间戳（一定要13位，不够用0补足）
#	period：周期（day-日，week-周，…）
#	type：类型（before-历史）
#	count：周期数（-8表示获取前8个周期（日）数据）
#	indicator：指示信号（kline-K线，pe-市盈率，pb市净率 等等)

import json
import pandas as pd
import time

def timestamp(timing: str) -> int:
        """
        时间转时间戳
        :param timing:
        :return:
        """
        s_t = time.strptime(timing, "%Y-%m-%d %H:%M:%S")
        mkt = int(time.mktime(s_t)) * 1000
        return (mkt)


def stp_t(timestamp: int) -> str:
        """
        时间戳转时间
        :param timestamp:
        :return:

        """
        # localtime /seconds
        timeArray = time.localtime(timestamp / 1000)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        return otherStyleTime

def get_xueqiu_stock(symbol,begin,period,count,indicator):
        
	
	#:param symbol: SZ300813
	#:param begin: 1669853231808
	#:param period: period=day || week || month || quarter || year || 120m || 60m
	#:param count:  -10 从开始向前的k线数量
	#:param indicator: 指标 kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance
	#:return:

	begin=timestamp(begin)
	#begin='1664553600000'
	type ='before'
	count='-'+str(count)
	# 记得 cookies 要换，网络抓包用chrome右键检查，network，刷新页面，找到对应的请求，找到cookies
	headers = {
		'authority':'stock.xueqiu.com',
		'method':'GET',
		'Cookie':"cookiesu=151695304469557; device_id=e03752a399b2fb0af3b0de7be0f5aecd; s=ck14mgbrj8; bid=cad74acbd943fb9fd7a73051f4451aec_lv9oq4zk; xq_is_login=1; u=1452847370; xq_a_token=84556bd394cf16f377cc4938b09efa10ae3f163b; xqat=84556bd394cf16f377cc4938b09efa10ae3f163b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjE0NTI4NDczNzAsImlzcyI6InVjIiwiZXhwIjoxNzI3NTk4NjAxLCJjdG0iOjE3MjUwMDY2MDExMDQsImNpZCI6ImQ5ZDBuNEFadXAifQ.FfJCnlrrSb3pI9zljxnHqe9eJH-yCUnfqGQ20IVodbcapJYpcDAuTTKeHZsm59Z0yYLntt1V1MZdM8C21DSjeycLKEpwexmpNQDRgb1mrtI2amiALC7quJ6b72zietvxjsTgaSD4P2BzhOEQ7slaqF350Qy_cICQX60s1F2vGPbqN91wNL0T6ulUTxgLGAehLurAWW234Q0UKDkefCHF9saMeevgPMUdCUvSrrOe4tYS3msP_OZMRt50v3EWPc83dyhcz6gb9FSZZJg6HZCr9vLg1OYrdnPmRr5XzJjeRnwu9V-Y0QkovWWNrth2nE8cQvUDLrQ-BmbPbCzpfOiADw; xq_r_token=5a160e4cfa641b936362d56561ef27b897c4c01f; is_overseas=0; Hm_lvt_1db88642e346389874251b5a1eded6e3=1725077287,1725148691,1725239602,1725281761; HMACCOUNT=DB6DE5FE89796214; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1725281793; ssxmod_itna=Yq+xyD0DnDgD9AiQGHqGdYM7zKG8KD0gGO7GoC++DGN4XoDZDiqAPGhDC8fFoeE4+NYlBhp5eDIE+55YCEY4dK3KB8GhFNxb74GLDmKDybUEleDxpq0rD74irDDxD3gD7PGmDieznD7oUM9LXBFqGRD0YDzqDgD7QqwqDEDG3D03UY7DxSiDDliYWhCYePDYpBnqQK=nrDAdoZYGGBD0tDIqGXlYHtxDt1gPxDcd9O=ppcWWrDtqD9+eN2Cn4SemNnQ64P7ODPIDYrI0Y4b+GiAboYBD44Ya+5WooNbYo5eXdUD5DAbhdxD=; ssxmod_itna2=Yq+xyD0DnDgD9AiQGHqGdYM7zKG8KD0gGO7GoC+xA6aPPD/lGDF2nh/P/0wUmK0Qz9rAvwzDqxT2D8e0oeIEC/QYpKGFDSeYi775GYdx4xa4tkTGeFx7Qe0DjKD2iYD=",
		'Origin':'https://xueqiu.com',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
	}
	req_str = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol='+str(symbol)+'&begin='+str(begin)+'&period='+str(period)+'&type='+str(type)+'&count='+str(count)+'&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'
    
	response =requests.get(req_str,headers=headers)
	#response=requests.get('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SOXX&begin=1664553600000&period=day&type=before&count=-8&indicator=kline',headers=headers)
	data = json.loads(response.text)

	# 提取数据
	column_names = data['data']['column']
	item_data = data['data']['item']

	# 创建DataFrame
	df = pd.DataFrame(item_data, columns=column_names)
	df['timestamp']=df['timestamp'].apply(stp_t)
	df.rename(columns={'timestamp':'date'},inplace=True)
	#df.to_csv("stock_data/SOXX_XUEQIU.csv")
	return df
	
#get_xueqiu_stock(symbol='SOXX',begin='2024-03-21 00:00:00',period='day',count='200',indicator='kline')

