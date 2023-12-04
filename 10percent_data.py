import pandas as pd
import efinance as ef
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import csv
from datetime import datetime
from global_var import *

current_date = datetime.now()
formatted_date = current_date.strftime('%Y%m%d')

def data_norm(a,b):
    return (a-b)/b

if(train):
    start_date = train_start_date
    end_date   = train_end_date #str(formatted_date)
    file_name = "10percent_TRAIN_DATA.csv"
else:
    start_date = test_start_date
    end_date   = str(formatted_date)
    file_name = "10percent_TEST_DATA.csv"

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

def build_frame(stock_keys,start_date,end_date):

    df = {}
    table = pd.DataFrame()
    table_row_index = 0
    for key in stock_keys:
            
            df[key,'day']   = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=101) # day
            df[key,'week']  = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=102) # week
            df[key,'month'] = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=103) # month
            #print(key)
            df[key,'day']   = get_bolls(df[key,'day'])
            df[key,'week']  = get_bolls(df[key,'week'])
            df[key,'month'] = get_bolls(df[key,'month'])

            week_index  = 0
            month_index = 0

            for day in range(len(df[key,'day'])):
                
                record_condition = df[key,'day']['涨跌幅'][day] >= 10.0 and week_index-1>=0 and month_index-1>=0

                if(record_condition):
                    table.loc[table_row_index,'date']   = df[key,'day']['日期'][day]
                    # the currentable_row_i
                    table.loc[table_row_index,'week_date']   = df[key,'week']['日期'][week_index-1]
                    table.loc[table_row_index,'month_date']  = df[key,'month']['日期'][month_index-1]
                    table.loc[table_row_index,'close']       = df[key,'day']['收盘'][day]
                    table.loc[table_row_index,'key']         = key
                    #table.loc[df[key,'day']['日期'][day],str(key)+'volume'] = df[key,'day']['成交量'][day]
                    if(month_index-5>=0):
                    # near 5 week price and data
                        table.loc[table_row_index,'near1d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-1])
                        table.loc[table_row_index,'near1d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-1])
                        table.loc[table_row_index,'near1d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-1])
                        table.loc[table_row_index,'near1d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-1])
                        table.loc[table_row_index,'near1d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-1])
                        table.loc[table_row_index,'near2d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-2])
                        table.loc[table_row_index,'near2d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-2])
                        table.loc[table_row_index,'near2d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-2])
                        table.loc[table_row_index,'near2d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-2])
                        table.loc[table_row_index,'near2d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-2])
                        table.loc[table_row_index,'near3d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-3])
                        table.loc[table_row_index,'near3d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-3])
                        table.loc[table_row_index,'near3d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-3])
                        table.loc[table_row_index,'near3d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-3])
                        table.loc[table_row_index,'near3d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-3])
                        table.loc[table_row_index,'near4d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-4])
                        table.loc[table_row_index,'near4d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-4])
                        table.loc[table_row_index,'near4d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-4])
                        table.loc[table_row_index,'near4d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-4])
                        table.loc[table_row_index,'near4d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-4])
                        table.loc[table_row_index,'near5d_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['开盘'][day-5])
                        table.loc[table_row_index,'near5d_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'day']['收盘'][day-5])
                        table.loc[table_row_index,'near5d_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最高'][day-5])
                        table.loc[table_row_index,'near5d_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['最低'][day-5])
                        table.loc[table_row_index,'near5d_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'day']['成交量'][day-5])
                        table.loc[table_row_index,'near1w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-1])
                        table.loc[table_row_index,'near1w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-1])
                        table.loc[table_row_index,'near1w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-1])
                        table.loc[table_row_index,'near1w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-1])
                        table.loc[table_row_index,'near1w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-1])
                        table.loc[table_row_index,'near2w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-2])
                        table.loc[table_row_index,'near2w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-2])
                        table.loc[table_row_index,'near2w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-2])
                        table.loc[table_row_index,'near2w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-2])
                        table.loc[table_row_index,'near2w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-2])
                        table.loc[table_row_index,'near3w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-3])
                        table.loc[table_row_index,'near3w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-3])
                        table.loc[table_row_index,'near3w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-3])
                        table.loc[table_row_index,'near3w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-3])
                        table.loc[table_row_index,'near3w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-3])
                        table.loc[table_row_index,'near4w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-4])
                        table.loc[table_row_index,'near4w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-4])
                        table.loc[table_row_index,'near4w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-4])
                        table.loc[table_row_index,'near4w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-4])
                        table.loc[table_row_index,'near4w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-4])
                        table.loc[table_row_index,'near5w_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['开盘'][week_index-5])
                        table.loc[table_row_index,'near5w_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['收盘'][week_index-5])
                        table.loc[table_row_index,'near5w_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最高'][week_index-5])
                        table.loc[table_row_index,'near5w_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'week']['最低'][week_index-5])
                        table.loc[table_row_index,'near5w_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'week']['成交量'][week_index-5])
            
                        table.loc[table_row_index,'near1m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-1])
                        table.loc[table_row_index,'near1m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-1])
                        table.loc[table_row_index,'near1m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-1])
                        table.loc[table_row_index,'near1m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-1])
                        table.loc[table_row_index,'near1m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-1])
                        table.loc[table_row_index,'near2m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-2])
                        table.loc[table_row_index,'near2m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-2])
                        table.loc[table_row_index,'near2m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-2])
                        table.loc[table_row_index,'near2m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-2])
                        table.loc[table_row_index,'near2m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-2])
                        table.loc[table_row_index,'near3m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-3])
                        table.loc[table_row_index,'near3m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-3])
                        table.loc[table_row_index,'near3m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-3])
                        table.loc[table_row_index,'near3m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-3])
                        table.loc[table_row_index,'near3m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-3])
                        table.loc[table_row_index,'near4m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-4])
                        table.loc[table_row_index,'near4m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-4])
                        table.loc[table_row_index,'near4m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-4])
                        table.loc[table_row_index,'near4m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-4])
                        table.loc[table_row_index,'near4m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-4])
                        table.loc[table_row_index,'near5m_open']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['开盘'][month_index-5])
                        table.loc[table_row_index,'near5m_close']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['收盘'][month_index-5])
                        table.loc[table_row_index,'near5m_high']   = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最高'][month_index-5])
                        table.loc[table_row_index,'near5m_low']    = data_norm(df[key,'day']['收盘'][day],df[key,'month']['最低'][month_index-5])
                        table.loc[table_row_index,'near5m_volume'] = data_norm(df[key,'day']['成交量'][day],df[key,'month']['成交量'][month_index-5])
                        table.loc[table_row_index,'price/up day']    = data_norm(df[key,'day']['收盘'][day],df[key,'day']['upper'][day])
                        table.loc[table_row_index,'price/mid day']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['middle'][day])
                        table.loc[table_row_index,'price/low day']   = data_norm(df[key,'day']['收盘'][day],df[key,'day']['lower'][day])
                        table.loc[table_row_index,'price/up week']   = data_norm(df[key,'day']['收盘'][day],df[key,'week']['upper'][week_index-1])
                        table.loc[table_row_index,'price/mid week']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['middle'][week_index-1])
                        table.loc[table_row_index,'price/low week']  = data_norm(df[key,'day']['收盘'][day],df[key,'week']['lower'][week_index-1])
                        table.loc[table_row_index,'price/up month']  = data_norm(df[key,'day']['收盘'][day],df[key,'month']['upper'][month_index-1])
                        table.loc[table_row_index,'price/mid month'] = data_norm(df[key,'day']['收盘'][day],df[key,'month']['middle'][month_index-1])
                        table.loc[table_row_index,'price/low month'] = data_norm(df[key,'day']['收盘'][day],df[key,'month']['lower'][month_index-1])
                        table.loc[table_row_index,'price/20high']    = data_norm(df[key,'day']['收盘'][day],get_near_high(df,key,day,20))
                        table.loc[table_row_index,'price/20low']     = data_norm(df[key,'day']['收盘'][day],get_near_low(df,key,day,20))

                        if(day-7>=0):
                            table.loc[table_row_index,'7 day up']   =  int((df[key,'day']['收盘'][day]>df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]>df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]>df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]>df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]>df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]>df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]>df[key,'day']['开盘'][day-6]))
                            table.loc[table_row_index,'7 day down']   =  int((df[key,'day']['收盘'][day]<df[key,'day']['开盘'][day]) and
                                                                        (df[key,'day']['收盘'][day-1]<df[key,'day']['开盘'][day-1]) and
                                                                        (df[key,'day']['收盘'][day-2]<df[key,'day']['开盘'][day-2]) and
                                                                        (df[key,'day']['收盘'][day-3]<df[key,'day']['开盘'][day-3]) and
                                                                        (df[key,'day']['收盘'][day-4]<df[key,'day']['开盘'][day-4]) and
                                                                        (df[key,'day']['收盘'][day-5]<df[key,'day']['开盘'][day-5]) and
                                                                        (df[key,'day']['收盘'][day-6]<df[key,'day']['开盘'][day-6]))
                        if(day+20<len(df[key,'day'])):
                            table.loc[table_row_index,'gain20'] = df[key,'day']['收盘'][day+20]/df[key,'day']['收盘'][day]
                            table.loc[table_row_index,'day20gain'] =df[key,'day']['收盘'][day+20]
                        if(day+10<len(df[key,'day'])):
                            table.loc[table_row_index,'gain10'] = df[key,'day']['收盘'][day+10]/df[key,'day']['收盘'][day]
                            table.loc[table_row_index,'day10gain'] =df[key,'day']['收盘'][day+10]
                        if(day+5<len(df[key,'day'])):
                            table.loc[table_row_index,'gain5'] = df[key,'day']['收盘'][day+5]/df[key,'day']['收盘'][day]
                            table.loc[table_row_index,'day5gain'] =df[key,'day']['收盘'][day+5]
                        if(day+1<len(df[key,'day'])):
                            table.loc[table_row_index,'gain1'] = df[key,'day']['收盘'][day+1]/df[key,'day']['收盘'][day]
                            table.loc[table_row_index,'day1gain'] =df[key,'day']['收盘'][day+1]
                table_row_index = table_row_index+1
                # example week = 2012-7-12 day = 2012-7-11 week
                if(df[key,'week']['日期'][week_index]==df[key,'day']['日期'][day]):
                    if((week_index+1)<len(df[key,'week'])):
                        week_index +=1# next_week_index

                #print(df[key,'month']['日期'][month_index])
                if(df[key,'month']['日期'][month_index]==df[key,'day']['日期'][day]):
                    if((month_index+1)<len(df[key,'month'])):
                        month_index +=1# next_month_index
    return table
                                                   


color=[]
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
stocks0=ef.stock.get_members('399006')
stocks1=ef.stock.get_members('399001')#000852 #000905
#stocks2=ef.stock.get_members('000852')
stocks3=ef.stock.get_members('000905')
list0=stocks0['股票名称']
list1=stocks1['股票名称']
#list2=stocks2['股票名称']
list3=stocks3['股票名称']
stock_keys = pd.concat([list0,list1,list3])
table=build_frame(list(stock_keys),start_date,end_date)
csv_df = pd.DataFrame(data=table,index=None)
csv_df.to_csv("./stock_data/"+file_name)