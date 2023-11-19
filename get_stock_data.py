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

#stock_keys=['QQQ','SOXX','NVDA','TSLA','中芯国际']
#stock_keys=['中芯国际']
#start_date = '20120617'
end_date   = str(formatted_date)#'20231110'

# price
# price/boll_low(week)
# price/boll_med
# price/boll_high
# price/boll_low(month)
# price/boll_med
# price/boll_high
# price/20 day high
# price/20 day low
# price/price(-20)
def get_near_high(df,day,day_range):
    cur_high=df[key,'day']['收盘'][day]
    for i in range(day_range):
        if(day-i>=0):
            if((df[key,'day']['收盘'][day-i]>cur_high) and (day-i>=0)):
                cur_high = df[key,'day']['收盘'][day-i]
    return cur_high

def get_near_low(df,day,day_range):
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

df = {}
table = pd.DataFrame()
for key in stock_keys:
        df[key,'day']   = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=101)# day
        df[key,'week']  = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=102)# week
        df[key,'month'] = ef.stock.get_quote_history(stock_codes=key,beg=start_date,end=end_date,fqt=1,klt=103)# month
        df[key,'day']   = get_bolls(df[key,'day'])
        df[key,'week']  = get_bolls(df[key,'week'])
        df[key,'month'] = get_bolls(df[key,'month'])
        week_index = 0
        month_index = 0
        new_week_index=0
        new_month_index=0
        for day in range(len(df[key,'day'])):
            # example week = 2012-7-12 day = 2012-7-11 week
            if(df[key,'week']['日期'][new_week_index]==df[key,'day']['日期'][day]):
                if(week_index+1<len(df[key,'week'])):
                    week_index = new_week_index
                    new_week_index +=1
            if(df[key,'month']['日期'][new_month_index]==df[key,'day']['日期'][day]):
                if(month_index+1<len(df[key,'month'])):
                    month_index = new_month_index
                    new_month_index +=1
            if(week_index>=1 and month_index>=1):
                table.loc[df[key,'day']['日期'][day],str(key)+'date']   = df[key,'day']['日期'][day]
                # the current week contain futrue data, please check 
                table.loc[df[key,'day']['日期'][day],str(key)+'week_date']   = df[key,'week']['日期'][week_index]
                table.loc[df[key,'day']['日期'][day],str(key)+'month_date']  = df[key,'month']['日期'][month_index]
                table.loc[df[key,'day']['日期'][day],str(key)+'close']  = df[key,'day']['收盘'][day]
                table.loc[df[key,'day']['日期'][day],str(key)+'volume'] = df[key,'day']['成交量'][day]
                if(month_index-4>=0):
                # near 5 week price and data
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0w_open']   = df[key,'week']['开盘'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0w_close']  = df[key,'week']['收盘'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0w_high']   = df[key,'week']['最高'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0w_low']    = df[key,'week']['最低'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0w_volume'] = df[key,'week']['成交量'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1w_open']   = df[key,'week']['开盘'][week_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1w_close']  = df[key,'week']['收盘'][week_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1w_high']   = df[key,'week']['最高'][week_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1w_low']    = df[key,'week']['最低'][week_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1w_volume'] = df[key,'week']['成交量'][week_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2w_open']   = df[key,'week']['开盘'][week_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2w_close']  = df[key,'week']['收盘'][week_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2w_high']   = df[key,'week']['最高'][week_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2w_low']    = df[key,'week']['最低'][week_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2w_volume'] = df[key,'week']['成交量'][week_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3w_open']   = df[key,'week']['开盘'][week_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3w_close']  = df[key,'week']['收盘'][week_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3w_high']   = df[key,'week']['最高'][week_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3w_low']    = df[key,'week']['最低'][week_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3w_volume'] = df[key,'week']['成交量'][week_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4w_open']   = df[key,'week']['开盘'][week_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4w_close']  = df[key,'week']['收盘'][week_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4w_high']   = df[key,'week']['最高'][week_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4w_low']    = df[key,'week']['最低'][week_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4w_volume'] = df[key,'week']['成交量'][week_index-4]
                    # near 5 month price and data
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0m_open']   = df[key,'month']['开盘'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0m_close']  = df[key,'month']['收盘'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0m_high']   = df[key,'month']['最高'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0m_low']    = df[key,'month']['最低'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near0m_volume'] = df[key,'month']['成交量'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1m_open']   = df[key,'month']['开盘'][month_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1m_close']  = df[key,'month']['收盘'][month_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1m_high']   = df[key,'month']['最高'][month_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1m_low']    = df[key,'month']['最低'][month_index-1]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near1m_volume'] = df[key,'month']['成交量'][month_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2m_open']   = df[key,'month']['开盘'][month_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2m_close']  = df[key,'month']['收盘'][month_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2m_high']   = df[key,'month']['最高'][month_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2m_low']    = df[key,'month']['最低'][month_index-2]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near2m_volume'] = df[key,'month']['成交量'][month_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3m_open']   = df[key,'month']['开盘'][month_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3m_close']  = df[key,'month']['收盘'][month_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3m_high']   = df[key,'month']['最高'][month_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3m_low']    = df[key,'month']['最低'][month_index-3]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near3m_volume'] = df[key,'month']['成交量'][month_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4m_open']   = df[key,'month']['开盘'][month_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4m_close']  = df[key,'month']['收盘'][month_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4m_high']   = df[key,'month']['最高'][month_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4m_low']    = df[key,'month']['最低'][month_index-4]
                    table.loc[df[key,'day']['日期'][day],str(key)+'near4m_volume'] = df[key,'month']['成交量'][month_index-4]

                    table.loc[df[key,'day']['日期'][day],str(key)+'price/up day']  = df[key,'day']['收盘'][day]/df[key,'day']['upper'][day]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/mid day'] = df[key,'day']['收盘'][day]/df[key,'day']['middle'][day]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/low day'] = df[key,'day']['收盘'][day]/df[key,'day']['lower'][day]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/up week']  = df[key,'day']['收盘'][day]/df[key,'week']['upper'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/mid week'] = df[key,'day']['收盘'][day]/df[key,'week']['middle'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/low week'] = df[key,'day']['收盘'][day]/df[key,'week']['lower'][week_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/up month']  = df[key,'day']['收盘'][day]/df[key,'month']['upper'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/mid month'] = df[key,'day']['收盘'][day]/df[key,'month']['middle'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/low month'] = df[key,'day']['收盘'][day]/df[key,'month']['lower'][month_index]
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/20high']  = df[key,'day']['收盘'][day]/get_near_high(df,day,20)
                    table.loc[df[key,'day']['日期'][day],str(key)+'price/20low'] = df[key,'day']['收盘'][day]/get_near_low(df,day,20)

                    if(day-7>=0):
                        table.loc[df[key,'day']['日期'][day],str(key)+'7 day up']   =  int((df[key,'day']['收盘'][day]>df[key,'day']['开盘'][day]) and
                                                                    (df[key,'day']['收盘'][day-1]>df[key,'day']['开盘'][day-1]) and
                                                                    (df[key,'day']['收盘'][day-2]>df[key,'day']['开盘'][day-2]) and
                                                                    (df[key,'day']['收盘'][day-3]>df[key,'day']['开盘'][day-3]) and
                                                                    (df[key,'day']['收盘'][day-4]>df[key,'day']['开盘'][day-4]) and
                                                                    (df[key,'day']['收盘'][day-5]>df[key,'day']['开盘'][day-5]) and
                                                                    (df[key,'day']['收盘'][day-6]>df[key,'day']['开盘'][day-6]))
                        table.loc[df[key,'day']['日期'][day],str(key)+'7 day down']   =  int((df[key,'day']['收盘'][day]<df[key,'day']['开盘'][day]) and
                                                                    (df[key,'day']['收盘'][day-1]<df[key,'day']['开盘'][day-1]) and
                                                                    (df[key,'day']['收盘'][day-2]<df[key,'day']['开盘'][day-2]) and
                                                                    (df[key,'day']['收盘'][day-3]<df[key,'day']['开盘'][day-3]) and
                                                                    (df[key,'day']['收盘'][day-4]<df[key,'day']['开盘'][day-4]) and
                                                                    (df[key,'day']['收盘'][day-5]<df[key,'day']['开盘'][day-5]) and
                                                                    (df[key,'day']['收盘'][day-6]<df[key,'day']['开盘'][day-6]))
                    if(day+20<len(df[key,'day'])):
                        table.loc[df[key,'day']['日期'][day],str(key)+'gain20'] = df[key,'day']['收盘'][day+20]/df[key,'day']['收盘'][day]
                    if(day+10<len(df[key,'day'])):
                        table.loc[df[key,'day']['日期'][day],str(key)+'gain10'] = df[key,'day']['收盘'][day+10]/df[key,'day']['收盘'][day]
                    if(day+5<len(df[key,'day'])):
                        table.loc[df[key,'day']['日期'][day],str(key)+'gain5'] = df[key,'day']['收盘'][day+5]/df[key,'day']['收盘'][day]
                    if(day+1<len(df[key,'day'])):
                        table.loc[df[key,'day']['日期'][day],str(key)+'gain1'] = df[key,'day']['收盘'][day+1]/df[key,'day']['收盘'][day]                                                           


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

csv_df = pd.DataFrame(data=table,index=None)
csv_df.to_csv("STOCK_DATA.csv")