import pandas as pd
import efinance as ef
import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt
import talib as ta
import csv

stock_keys=['QQQ','SOXX','NVDA','TSLA','MSA']
start_date = '20120617'
end_date   = '202301011'

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
        for day in range(len(df[key,'day'])):
            if(df[key,'week']['日期'][week_index]==df[key,'day']['日期'][day]):
                if(week_index+1<len(df[key,'week'])):
                    week_index +=1
                    #print('hahah')
            if(df[key,'month']['日期'][month_index]==df[key,'day']['日期'][day]):
                if(month_index+1<len(df[key,'month'])):
                    month_index +=1
            table.loc[df[key,'day']['日期'][day],str(key)+'date']   = df[key,'day']['日期'][day]
            table.loc[df[key,'day']['日期'][day],str(key)+'close']  = df[key,'day']['收盘'][day]
            table.loc[df[key,'day']['日期'][day],str(key)+'volume'] = df[key,'day']['成交量'][day]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/up week']  = df[key,'day']['收盘'][day]/df[key,'week']['upper'][week_index]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/mid week'] = df[key,'day']['收盘'][day]/df[key,'week']['middle'][week_index]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/low week'] = df[key,'day']['收盘'][day]/df[key,'week']['lower'][week_index]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/up month']  = df[key,'day']['收盘'][day]/df[key,'month']['upper'][month_index]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/mid month'] = df[key,'day']['收盘'][day]/df[key,'month']['middle'][month_index]
            table.loc[df[key,'day']['日期'][day],str(key)+'price/low month'] = df[key,'day']['收盘'][day]/df[key,'month']['lower'][month_index]

            if(day-7>=0):
                table.loc[df[key,'day']['日期'][day],str(key)+'7 day up']   =  ((df[key,'day']['收盘'][day]>df[key,'day']['开盘'][day]) and
                                                            (df[key,'day']['收盘'][day-1]>df[key,'day']['开盘'][day-1]) and
                                                            (df[key,'day']['收盘'][day-2]>df[key,'day']['开盘'][day-2]) and
                                                            (df[key,'day']['收盘'][day-3]>df[key,'day']['开盘'][day-3]) and
                                                            (df[key,'day']['收盘'][day-4]>df[key,'day']['开盘'][day-4]) and
                                                            (df[key,'day']['收盘'][day-5]>df[key,'day']['开盘'][day-5]) and
                                                            (df[key,'day']['收盘'][day-6]>df[key,'day']['开盘'][day-6]))
                table.loc[df[key,'day']['日期'][day],str(key)+'7 day down']   =  ((df[key,'day']['收盘'][day]<df[key,'day']['开盘'][day]) and
                                                            (df[key,'day']['收盘'][day-1]<df[key,'day']['开盘'][day-1]) and
                                                            (df[key,'day']['收盘'][day-2]<df[key,'day']['开盘'][day-2]) and
                                                            (df[key,'day']['收盘'][day-3]<df[key,'day']['开盘'][day-3]) and
                                                            (df[key,'day']['收盘'][day-4]<df[key,'day']['开盘'][day-4]) and
                                                            (df[key,'day']['收盘'][day-5]<df[key,'day']['开盘'][day-5]) and
                                                            (df[key,'day']['收盘'][day-6]<df[key,'day']['开盘'][day-6]))
                                                           

            if(day-20>=0):
                table.loc[df[key,'day']['日期'][day],str(key)+'gain'] = df[key,'day']['收盘'][day]/df[key,'day']['收盘'][day-20]
                 

        
#print(df.shape)
#data_x = torch.from_numpy(df).float()
#x_df = pd.DataFrame(np.reshape(data_x,(df.shape[0],df.shape[-1])))

csv_df = pd.DataFrame(data=table,index=None)
csv_df.to_csv(str(start_date)+str(end_date)+"day.csv")