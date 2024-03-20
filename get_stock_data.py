import pandas as pd
import efinance as ef
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import csv
from datetime import datetime
from global_var import *
import akshare as ak

def get_near_high(df,key,day,day_range):
    cur_high=df[key,'day']['收盘'][day]
    for i in range(day_range):
        if(day-i>=0):
            if((df[key,'day']['收盘'][day-i]>cur_high) and (day-i>=0)):
                cur_high = df[key,'day']['收盘'][day-i]
    return cur_high

def get_near_low(df,key,day,day_range):
    cur_low=df[key,'day']['收盘'][day]
    for i in range(day_range):
        if(day-i>=0):
            if((df[key,'day']['收盘'][day-i]<cur_low)):
                cur_low = df[key,'day']['收盘'][day-i]
    return cur_low

def get_bolls(dw):
    dw.loc[:,'upper'],dw.loc[:,'middle'],dw.loc[:,'lower'] = ta.BBANDS(
        dw['收盘'],
        timeperiod=20,
        nbdevup=2,
        nbdevdn=2,
        matype=0
    )
    return dw

def ak_rename(df):
    df.rename(columns={'date':'日期','open':'开盘','high':'最高','low':'最低','close':'收盘','volume':'成交量'}, inplace=True)
    return df

# data from sina only have daily data
def akshare_data(key):

    stock_us_daily_df = ak.stock_us_daily(symbol=key, adjust="qfq")
    stock_us_daily_df['date'] = pd.to_datetime(stock_us_daily_df['date'])
    stock_us_daily_df.set_index('date', inplace=True)

    # 计算月线数据
    monthly_data = stock_us_daily_df.resample('M').agg({
        'open': 'first',  # 每月第一天的开盘价
        'high': 'max',    # 每月的最高价
        'low': 'min',     # 每月的最低价
        'close': 'last',  # 每月最后一天的收盘价
        'volume': 'sum'   # 每月的成交量总和
    })

    # 计算周线数据
    weekly_data = stock_us_daily_df.resample('W').agg({
        'open': 'first',  # 每周第一天的开盘价
        'high': 'max',    # 每周的最高价
        'low': 'min',     # 每周的最低价
        'close': 'last',  # 每周最后一天的收盘价
        'volume': 'sum'   # 每周的成交量总和
    })

    # 重置索引，使日期变回普通列
    monthly_data.reset_index(inplace=True)
    weekly_data.reset_index(inplace=True)
    stock_us_daily_df.reset_index(inplace=True)
    
    stock_us_daily_df=ak_rename(stock_us_daily_df)
    weekly_data=ak_rename(weekly_data)
    monthly_data=ak_rename(monthly_data)

    stock_us_daily_df.to_csv("./stock_data/"+key+"_day.csv")
    weekly_data.to_csv("./stock_data/"+key+"_week.csv")
    monthly_data.to_csv("./stock_data/"+key+"_month.csv")

    return stock_us_daily_df,weekly_data,monthly_data

def build_frame(stock_keys,start_date,end_date):
    df = {}
    table = pd.DataFrame()
    for key in stock_keys:
            
            if(is_akshare):
                df[key,'day'],df[key,'week'],df[key,'month'] = akshare_data(key)
            else:
                df[key,'day']   = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=101)# day
                df[key,'week']  = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=102)# week
                df[key,'month'] = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=103)# month

            df[key,'day']   = get_bolls(df[key,'day'])
            df[key,'week']  = get_bolls(df[key,'week'])
            df[key,'month'] = get_bolls(df[key,'month'])

            week_index  = 0
            month_index = 0
            for day in range(len(df[key,'day'])):

                if(week_index-1>=0 and month_index-1>=0):
                    table.loc[df[key,'day']['日期'][day],str(key)+'date']   = df[key,'day']['日期'][day]
                    # the current week contain no futrue data
                    table.loc[df[key,'day']['日期'][day],str(key)+'week_date']   = df[key,'week']['日期'][week_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'month_date']  = df[key,'month']['日期'][month_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'close']       = df[key,'day']['收盘'][day]
                    #table.loc[df[key,'day']['日期'][day],str(key)+'volume'] = df[key,'day']['成交量'][day]
                    if(month_index-5>=0):
                    # near 5 week price and data
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1d_open']   = df[key,'day']['收盘'][day]/df[key,'day']['开盘'][day-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1d_close']  = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1d_high']   = df[key,'day']['收盘'][day]/df[key,'day']['最高'][day-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1d_low']    = df[key,'day']['收盘'][day]/df[key,'day']['最低'][day-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1d_volume'] = df[key,'day']['成交量'][day]/df[key,'day']['成交量'][day-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2d_open']   = df[key,'day']['收盘'][day]/df[key,'day']['开盘'][day-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2d_close']  = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2d_high']   = df[key,'day']['收盘'][day]/df[key,'day']['最高'][day-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2d_low']    = df[key,'day']['收盘'][day]/df[key,'day']['最低'][day-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2d_volume'] = df[key,'day']['成交量'][day]/df[key,'day']['成交量'][day-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3d_open']   = df[key,'day']['收盘'][day]/df[key,'day']['开盘'][day-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3d_close']  = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3d_high']   = df[key,'day']['收盘'][day]/df[key,'day']['最高'][day-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3d_low']    = df[key,'day']['收盘'][day]/df[key,'day']['最低'][day-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3d_volume'] = df[key,'day']['成交量'][day]/df[key,'day']['成交量'][day-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4d_open']   = df[key,'day']['收盘'][day]/df[key,'day']['开盘'][day-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4d_close']  = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4d_high']   = df[key,'day']['收盘'][day]/df[key,'day']['最高'][day-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4d_low']    = df[key,'day']['收盘'][day]/df[key,'day']['最低'][day-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4d_volume'] = df[key,'day']['成交量'][day]/df[key,'day']['成交量'][day-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5d_open']   = df[key,'day']['收盘'][day]/df[key,'day']['开盘'][day-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5d_close']  = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5d_high']   = df[key,'day']['收盘'][day]/df[key,'day']['最高'][day-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5d_low']    = df[key,'day']['收盘'][day]/df[key,'day']['最低'][day-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5d_volume'] = df[key,'day']['成交量'][day]/df[key,'day']['成交量'][day-5]

                        table.loc[df[key,'day']['日期'][day],str(key)+'near1w_open']   = df[key,'day']['收盘'][day]/df[key,'week']['开盘'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1w_close']  = df[key,'day']['收盘'][day]/df[key,'week']['收盘'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1w_high']   = df[key,'day']['收盘'][day]/df[key,'week']['最高'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1w_low']    = df[key,'day']['收盘'][day]/df[key,'week']['最低'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1w_volume'] = df[key,'day']['成交量'][day]/df[key,'week']['成交量'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2w_open']   = df[key,'day']['收盘'][day]/df[key,'week']['开盘'][week_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2w_close']  = df[key,'day']['收盘'][day]/df[key,'week']['收盘'][week_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2w_high']   = df[key,'day']['收盘'][day]/df[key,'week']['最高'][week_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2w_low']    = df[key,'day']['收盘'][day]/df[key,'week']['最低'][week_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2w_volume'] = df[key,'day']['成交量'][day]/df[key,'week']['成交量'][week_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3w_open']   = df[key,'day']['收盘'][day]/df[key,'week']['开盘'][week_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3w_close']  = df[key,'day']['收盘'][day]/df[key,'week']['收盘'][week_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3w_high']   = df[key,'day']['收盘'][day]/df[key,'week']['最高'][week_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3w_low']    = df[key,'day']['收盘'][day]/df[key,'week']['最低'][week_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3w_volume'] = df[key,'day']['成交量'][day]/df[key,'week']['成交量'][week_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4w_open']   = df[key,'day']['收盘'][day]/df[key,'week']['开盘'][week_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4w_close']  = df[key,'day']['收盘'][day]/df[key,'week']['收盘'][week_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4w_high']   = df[key,'day']['收盘'][day]/df[key,'week']['最高'][week_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4w_low']    = df[key,'day']['收盘'][day]/df[key,'week']['最低'][week_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4w_volume'] = df[key,'day']['成交量'][day]/df[key,'week']['成交量'][week_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5w_open']   = df[key,'day']['收盘'][day]/df[key,'week']['开盘'][week_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5w_close']  = df[key,'day']['收盘'][day]/df[key,'week']['收盘'][week_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5w_high']   = df[key,'day']['收盘'][day]/df[key,'week']['最高'][week_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5w_low']    = df[key,'day']['收盘'][day]/df[key,'week']['最低'][week_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5w_volume'] = df[key,'day']['成交量'][day]/df[key,'week']['成交量'][week_index-5]
                        # near 5 month price 
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1m_open']   = df[key,'day']['收盘'][day]/df[key,'month']['开盘'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1m_close']  = df[key,'day']['收盘'][day]/df[key,'month']['收盘'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1m_high']   = df[key,'day']['收盘'][day]/df[key,'month']['最高'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1m_low']    = df[key,'day']['收盘'][day]/df[key,'month']['最低'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near1m_volume'] = df[key,'day']['成交量'][day]/df[key,'month']['成交量'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2m_open']   = df[key,'day']['收盘'][day]/df[key,'month']['开盘'][month_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2m_close']  = df[key,'day']['收盘'][day]/df[key,'month']['收盘'][month_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2m_high']   = df[key,'day']['收盘'][day]/df[key,'month']['最高'][month_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2m_low']    = df[key,'day']['收盘'][day]/df[key,'month']['最低'][month_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near2m_volume'] = df[key,'day']['成交量'][day]/df[key,'month']['成交量'][month_index-2]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3m_open']   = df[key,'day']['收盘'][day]/df[key,'month']['开盘'][month_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3m_close']  = df[key,'day']['收盘'][day]/df[key,'month']['收盘'][month_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3m_high']   = df[key,'day']['收盘'][day]/df[key,'month']['最高'][month_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3m_low']    = df[key,'day']['收盘'][day]/df[key,'month']['最低'][month_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near3m_volume'] = df[key,'day']['成交量'][day]/df[key,'month']['成交量'][month_index-3]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4m_open']   = df[key,'day']['收盘'][day]/df[key,'month']['开盘'][month_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4m_close']  = df[key,'day']['收盘'][day]/df[key,'month']['收盘'][month_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4m_high']   = df[key,'day']['收盘'][day]/df[key,'month']['最高'][month_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4m_low']    = df[key,'day']['收盘'][day]/df[key,'month']['最低'][month_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near4m_volume'] = df[key,'day']['成交量'][day]/df[key,'month']['成交量'][month_index-4]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5m_open']   = df[key,'day']['收盘'][day]/df[key,'month']['开盘'][month_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5m_close']  = df[key,'day']['收盘'][day]/df[key,'month']['收盘'][month_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5m_high']   = df[key,'day']['收盘'][day]/df[key,'month']['最高'][month_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5m_low']    = df[key,'day']['收盘'][day]/df[key,'month']['最低'][month_index-5]
                        table.loc[df[key,'day']['日期'][day],str(key)+'near5m_volume'] = df[key,'day']['成交量'][day]/df[key,'month']['成交量'][month_index-5]

                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_up_day']    = df[key,'day']['收盘'][day]/df[key,'day']['upper'][day]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_mid_day']   = df[key,'day']['收盘'][day]/df[key,'day']['middle'][day]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_low_day']   = df[key,'day']['收盘'][day]/df[key,'day']['lower'][day]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_up_week']   = df[key,'day']['收盘'][day]/df[key,'week']['upper'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_mid_week']  = df[key,'day']['收盘'][day]/df[key,'week']['middle'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_low_week']  = df[key,'day']['收盘'][day]/df[key,'week']['lower'][week_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_up_month']  = df[key,'day']['收盘'][day]/df[key,'month']['upper'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_mid_month'] = df[key,'day']['收盘'][day]/df[key,'month']['middle'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_low_month'] = df[key,'day']['收盘'][day]/df[key,'month']['lower'][month_index-1]
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_20high']    = df[key,'day']['收盘'][day]/get_near_high(df,key,day,20)
                        table.loc[df[key,'day']['日期'][day],str(key)+'price_vs_20low']     = df[key,'day']['收盘'][day]/get_near_low(df,key,day,20)

                        if(day-7>=0):
                            table.loc[df[key,'day']['日期'][day],str(key)+'7dayup']   =  int((df[key,'day']['收盘'][day]>df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]>df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]>df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]>df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]>df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]>df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]>df[key,'day']['开盘'][day-6]))
                            table.loc[df[key,'day']['日期'][day],str(key)+'7daydown']   =  int((df[key,'day']['收盘'][day]<df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]<df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]<df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]<df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]<df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]<df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]<df[key,'day']['开盘'][day-6]))
                        if(day+train_targets[0]<len(df[key,'day'])):
                            table.loc[df[key,'day']['日期'][day],str(key)+'gain'+str(train_targets[0])] = df[key,'day']['收盘'][day+train_targets[0]]/df[key,'day']['收盘'][day]
                        if(day+train_targets[1]<len(df[key,'day'])):
                            table.loc[df[key,'day']['日期'][day],str(key)+'gain'+str(train_targets[1])] = df[key,'day']['收盘'][day+train_targets[1]]/df[key,'day']['收盘'][day]
                        if(day+train_targets[2]<len(df[key,'day'])):
                            table.loc[df[key,'day']['日期'][day],str(key)+'gain'+str(train_targets[2])] = df[key,'day']['收盘'][day+train_targets[2]]/df[key,'day']['收盘'][day]
                        if(day+train_targets[3]<len(df[key,'day'])):
                            table.loc[df[key,'day']['日期'][day],str(key)+'gain'+str(train_targets[3])] = df[key,'day']['收盘'][day+train_targets[3]]/df[key,'day']['收盘'][day]
                if(is_akshare):
                    if(df[key,'week']['日期'][week_index]<=df[key,'day']['日期'][day]):
                        if((week_index+1)<len(df[key,'week'])):
                            week_index +=1# next_week_index
                    if(df[key,'month']['日期'][month_index]<=df[key,'day']['日期'][day]):
                        if((month_index+1)<len(df[key,'month'])):
                            month_index +=1# next_month_index
                else:
                    if(df[key,'week']['日期'][week_index]==df[key,'day']['日期'][day]):
                        if((week_index+1)<len(df[key,'week'])):
                            week_index +=1# next_week_index
                    if(df[key,'month']['日期'][month_index]==df[key,'day']['日期'][day]):
                        if((month_index+1)<len(df[key,'month'])):
                            month_index +=1# next_month_index

    return table

if __name__ == "__main__":
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')

    if(train):
        start_date = train_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TRAIN_DATA.csv"
    else:
        start_date = test_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TEST_DATA.csv"
    table= build_frame(x_stocks,start_date,end_date)
    csv_df = pd.DataFrame(data=table,index=None)
    csv_df.to_csv("./stock_data/"+file_name)