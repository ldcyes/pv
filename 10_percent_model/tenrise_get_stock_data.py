import pandas as pd
import efinance as ef
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import csv
from datetime import datetime
import stock_api
from tenrise_global_var import *

def data_norm(a,b):
    if(b==0):
        return np.inf
    else:
        return a/b

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
    if(len(dw['收盘'])==0):
        return dw
    else:
        dw.loc[:,'upper'],dw.loc[:,'middle'],dw.loc[:,'lower'] = ta.BBANDS(
        dw['收盘'],
        timeperiod=20,
        nbdevup=2,
        nbdevdn=2,
        matype=0
    )
    return dw

def col_rename(df):
    df.rename(columns={'date':'日期','open':'开盘','high':'最高','low':'最低','close':'收盘','volume':'成交量'}, inplace=True)
    return df

def xueqiu_data(key,start_date,count=1000):

    begin = start_date+" 00:00:00"
    
    stock_us_daily_df=stock_api.get_xueqiu_stock(symbol=key,begin=begin,period='day',count=count,indicator='kline')
    
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
    
    stock_us_daily_df=col_rename(stock_us_daily_df)
    weekly_data=col_rename(weekly_data)
    monthly_data=col_rename(monthly_data)

    stock_us_daily_df.to_csv("./stock_data/"+key+"_day.csv")
    weekly_data.to_csv("./stock_data/"+key+"_week.csv")
    monthly_data.to_csv("./stock_data/"+key+"_month.csv")

    return stock_us_daily_df,weekly_data,monthly_data

def build_frame(stock_keys,start_date,end_date):

    df = {}
    table = pd.DataFrame()
    table_row_index = 0

    for key in stock_keys:
            print(str(key))

            if(is_xueqiu==1):
                df[key,'day'],df[key,'week'],df[key,'month'] = xueqiu_data(key,end_date,count=365*12)
            else:
                df[key,'day']   = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=101) # day
                df[key,'week']  = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=102) # week
                df[key,'month'] = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=103) # month

            # data is empty
            if(df[key,'day'].empty or df[key,'week'].empty or df[key,'month'].empty):
                continue

            #print(key)
            df[key,'day']   = get_bolls(df[key,'day'])
            df[key,'week']  = get_bolls(df[key,'week'])
            df[key,'month'] = get_bolls(df[key,'month'])

            week_index  = 0
            month_index = 0

            for day in range(len(df[key,'day'])):
                if(is_xueqiu):
                    if(df[key,'week']['日期'][week_index]<df[key,'day']['日期'][day]):
                        # 2-25,3-3,3-10
                        # 3/1, 3/4-8,3/11
                        if((week_index+1)<len(df[key,'week'])):
                            week_index +=1# next_week_index
                    if(df[key,'month']['日期'][month_index]<df[key,'day']['日期'][day]):
                        if((month_index+1)<len(df[key,'month'])):
                            month_index +=1# next_month_index
                # note this should >10 percent rise
                record_condition = (df[key,'day']['涨跌幅'][day] >= 6.8) and (week_index-1>=0) and \
                                   (month_index-1>=0) and \
                                   (df[key,'day']['涨跌幅'][day] <= 10.2)
                if(record_condition):
                    table.loc[table_row_index,'date']   = df[key,'day']['日期'][day]
                    # the currentable_row_i
                    table.loc[table_row_index,'week_date']   = df[key,'week']['日期'][week_index-1]
                    table.loc[table_row_index,'month_date']  = df[key,'month']['日期'][month_index-1]
                    table.loc[table_row_index,'close']       = df[key,'day']['收盘'][day]
                    table.loc[table_row_index,'open']        = df[key,'day']['开盘'][day]
                    table.loc[table_row_index,'volume']      = df[key,'day']['成交量'][day]
                    table.loc[table_row_index,'key']         = key
                    #table.loc[df[key,'day']['日期'][day],str(key)+'volume'] = df[key,'day']['成交量'][day]
                    if(month_index-back_times>=0):
                        for i in range(1,back_times+1):
                    # near 5 week price and data
                            table.loc[table_row_index,'near1d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-1])
                            table.loc[table_row_index,'near1d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-1])
                            table.loc[table_row_index,'near1d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-1])
                            table.loc[table_row_index,'near1d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-1])
                            table.loc[table_row_index,'near1d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-1])
                            table.loc[table_row_index,'near1w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-1])
                            table.loc[table_row_index,'near1w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-1])
                            table.loc[table_row_index,'near1w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-1])
                            table.loc[table_row_index,'near1w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-1])
                            table.loc[table_row_index,'near1w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-1])           
                            table.loc[table_row_index,'near1m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-1])
                            table.loc[table_row_index,'near1m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-1])
                            table.loc[table_row_index,'near1m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-1])
                            table.loc[table_row_index,'near1m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-1])
                            table.loc[table_row_index,'near1m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-1])
                        
                        table.loc[table_row_index,'price_vs_up_day']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['upper'][day])
                        table.loc[table_row_index,'price_vs_mid_day']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['middle'][day])
                        table.loc[table_row_index,'price_vs_low_day']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['lower'][day])
                        table.loc[table_row_index,'price_vs_up_week']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['upper'][week_index-1])
                        table.loc[table_row_index,'price_vs_mid_week']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['middle'][week_index-1])
                        table.loc[table_row_index,'price_vs_low_week']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['lower'][week_index-1])
                        table.loc[table_row_index,'price_vs_up_month']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['upper'][month_index-1])
                        table.loc[table_row_index,'price_vs_mid_month'] = data_norm(df[key,'day']['收盘'][day],df[key,'month']['middle'][month_index-1])
                        table.loc[table_row_index,'price_vs_low_month'] = data_norm(df[key,'day']['收盘'][day],df[key,'month']['lower'][month_index-1])
                        table.loc[table_row_index,'price_vs_20high']    = data_norm(df[key,'day']['收盘'][day],get_near_high(df,key,day,20))
                        table.loc[table_row_index,'price_vs_20low']     = data_norm(df[key,'day']['收盘'][day],get_near_low(df,key,day,20))

                        if(day-7>=0):
                            table.loc[table_row_index,'7dayup']   =  int((df[key,'day']['收盘'][day]>df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]>df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]>df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]>df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]>df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]>df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]>df[key,'day']['开盘'][day-6]))
                            table.loc[table_row_index,'7daydown']   =  int((df[key,'day']['收盘'][day]<df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]<df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]<df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]<df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]<df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]<df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]<df[key,'day']['开盘'][day-6]))
                        if(day+train_targets[0]<len(df[key,'day'])):
                            table.loc[table_row_index,'gain'+str(train_targets[0])] = data_norm(df[key,'day']['收盘'][day+train_targets[0]],df[key,'day']['收盘'][day])
                            #table.loc[table_row_index,'day20gain'] =df[key,'day']['收盘'][day+20]
                        if(day+train_targets[1]<len(df[key,'day'])):
                            table.loc[table_row_index,'gain'+str(train_targets[1])] = data_norm(df[key,'day']['收盘'][day+train_targets[1]],df[key,'day']['收盘'][day])
                            #table.loc[table_row_index,'day10gain'] =df[key,'day']['收盘'][day+10]
                        #if(day+train_targets[2]<len(df[key,'day'])):
                        #    table.loc[table_row_index,'gain'+str(train_targets[2])] = data_norm(df[key,'day']['收盘'][day+train_targets[2]],df[key,'day']['收盘'][day])
                            #table.loc[table_row_index,'day5gain'] =df[key,'day']['收盘'][day+5]
                        #if(day+train_targets[3]<len(df[key,'day'])):
                        #    table.loc[table_row_index,'gain'+str(train_targets[3])] = data_norm(df[key,'day']['收盘'][day+train_targets[3]],df[key,'day']['收盘'][day])
                        #if(day+train_targets[4]<len(df[key,'day'])):
                        #    table.loc[table_row_index,'gain'+str(train_targets[4])] = data_norm(df[key,'day']['收盘'][day+train_targets[4]],df[key,'day']['收盘'][day])
                  
                            #table.loc[table_row_index,'day1gain'] =df[key,'day']['收盘'][day+1]
                table_row_index = table_row_index+1
                if(is_xueqiu):
                    pass
                else:
                # example week = 2012-7-12 day = 2012-7-11 week
                    if(df[key,'week']['日期'][week_index]==df[key,'day']['日期'][day]):
                        if((week_index+1)<len(df[key,'week'])):
                            week_index +=1# next_week_index

                    #print(df[key,'month']['日期'][month_index])
                    if(df[key,'month']['日期'][month_index]==df[key,'day']['日期'][day]):
                        if((month_index+1)<len(df[key,'month'])):
                            month_index +=1# next_month_index
    
    # 按A列日期由先到后排序
    if(len(stock_keys)>1):
        table['date'] = table[stock_keys[1]+'date'].combine_first(table[stock_keys[0]+'date'])
    else:
        table['date'] = table[stock_keys[0]+'date']
    
    table.sort_values('date',inplace=True) 

    return table
                                                   
#color=[]
'''
key = 'SOXX'
for i in range(len(df[key,'day']['收盘'])):
    if(table.loc[df[key,'day']['日期'][i],str(key)+'gain']<0.9):
        color.append('green')
    elif(table.loc[df[key,'day']['日期'][i],str(key)+'gain']>1.1):
        color.append('red')
    else:
        color.append('blue')

print(color)
x = np.arange(len(df[key,'day']['收盘']))

#plt.scatter(x,df[key,'day']['收盘'],color=color)
#plt.show()
'''
if __name__ == "__main__":
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')
    if(train):
        start_date = train_start_date
        end_date   = train_end_date
        file_name = "10rise_TRAIN_DATA.csv"
    else:
        start_date = test_start_date
        end_date   = str(formatted_date)
        file_name = "10rise_TEST_DATA.csv"
    eft_id_list = [
        #'399006',
        #'399001',
        '399006',
        '399001',
        '399005',
        '000905',
        '000905']
    stock_keys=pd.DataFrame()

    for id in eft_id_list:
        stocks=ef.stock.get_members(id)# CYB300
        stock_keys=pd.concat([stock_keys,stocks['股票名称']])
    stock_keys=stock_keys.drop_duplicates(inplace=False)
    print("the stock total numbers ",stock_keys.shape)
    print(stock_keys)
    print(type(stock_keys))
    table=build_frame(list(stock_keys[0]),start_date,end_date)
    csv_df = pd.DataFrame(data=table,index=None)
    csv_df.to_csv("./stock_data/"+file_name)
