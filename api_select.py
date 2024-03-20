import akshare as ak

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
import akshare as ak

stock_us_hist_df = ak.stock_us_hist(symbol='105.SOXX', period="daily", start_date="20200101", end_date="20240314", adjust="qfq")
stock_name = ak.stock_us_spot_em()
stock_name.to_csv("stock_data/stock_name.csv")
#print(stock_us_hist_df)
stock_us_hist_df.to_csv("stock_data/SOXX_EAST.csv")
stock_us_daily_df = ak.stock_us_daily(symbol="SOXX", adjust="qfq")
print(stock_us_daily_df)
stock_us_daily_df.to_csv("stock_data/SOXX_SINA.csv")
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

# 获取 SOXX 的历史数据
#soxx = yf.Ticker("AAPL")
#date = "2024-03-10"
# 获取复权的历史数据，period='max' 表示获取所有可用的历史数据
#soxx_history = soxx.history(start=date, end=date)

#print(soxx_history)


