from math import floor
import pandas as pd
import numpy as np
import pickle
from global_var import *
import matplotlib.pyplot as plt

def draw_list(my_list,buy_point,sell_point,gold_point,positon,free,file_name):
     # 使用numpy创建一个时间和数值对  
    time = np.arange(len(my_list))  
    value = my_list  
    
    # 创建曲线图  
    plt.figure(figsize=(30, 18))  
    plt.plot(time, value     ,label='net_value',color='red')
    plt.plot(time, buy_point ,label='buy',color='blue')  
    plt.plot(time, sell_point,label='sell',color='yellow')  
    plt.plot(time, gold_point,label='gold',color='green')  
    plt.plot(time, positon,label='position',color='k')
    plt.plot(time, free,label='free',color='c')  
    plt.title(y_stock)  
    plt.xlabel('Time')  
    plt.ylabel('net value')  
    plt.grid(True)  
    plt.legend()
    plt.savefig(file_name)

def calculate_max_drawdown(prices):
    """
    计算最大回撤

    参数：
    - prices: 时间序列的价格数据（例如股票价格）

    返回：
    - max_drawdown: 最大回撤
    """
    cumulative_return = (1 + prices.pct_change()).cumprod()
    peak = cumulative_return.expanding(min_periods=1).max()
    drawdown = (cumulative_return - peak) / peak
    max_drawdown = drawdown.min()
    return max_drawdown

df_org = pd.read_csv("./stock_data/10percent_TEST_DATA.csv")

features_remain = features
features_x = features

print("orginal data shape")
print(df_org.shape)
#filtered_df = df_org[features_remain][0:-2]
print("get require feature data shape")
#print(filtered_df.shape)
#filtered_df= filtered_df.dropna()

for test_target in test_targets:
    for model_n in test_model_name:
        net_value = 100000
        start_value = 100000
        cur_free  = 100000
        cur_price = 0
        cur_position = 0
        buy_position = 10
        sell_position = 10

        buy_list  = []
        sell_list = []
        gold_list = []
        profile = []
        position_list =[]
        free_list = []

        is_start_day =1

        for day in range(len(df_org[:])):

            predict_avg = 0
            cur_price=df_org['close'][day]
            sell_price=df_org['day'+str(test_target)+'gain'][day]
            buy_condition = 0
            sell_condition = 0

            if(not(df_org.iloc[day][features_x].isna().any())):
                if(is_start_day):
                    first_price = cur_price
                    cur_position = 0#floor(net_value/cur_price)
                    cur_free = cur_free
                    print(cur_position,"start postion")
                    is_start_day=0
                predict_avg = 0
                model = pickle.load(open("./10_percent_model/"+str(model_n)+str(test_target)+'_model.pkl','rb'))
                
                predict_result = model.predict(df_org[features_x][day:day+1])
                predict_avg = predict_result+predict_avg
                buy_condition  = predict_avg >= 1.05
                sell_condition = buy_condition
                buy_position = cur_free/cur_price
                sell_position = cur_position

                if(buy_condition):
                    if((buy_position * cur_price) < cur_free ):
                        cur_free     = cur_free- buy_position*cur_price
                        cur_position = cur_position+ buy_position
                if(sell_condition):
                    if(cur_position>sell_position):
                        cur_free     = cur_free + sell_position*sell_price
                        cur_position = cur_position - sell_position
                    else:
                        cur_free = cur_free + sell_price*cur_position
                        cur_position = 0

                position_list.append(cur_position*100)
                free_list.append(cur_free)

                if(buy_condition and ((buy_position * cur_price) < cur_free)):
                     buy_list.append(buy_position*cur_price)
                else:
                     buy_list.append(0)
                if(sell_condition and (cur_position>sell_position)):
                     sell_list.append(sell_position*cur_price)
                else:
                     sell_list.append(0)

                profile.append(cur_free+cur_position*cur_price)
                gold_list.append(cur_price*start_value/first_price)
                
        print("------=====------",model_n)
        print("valid days: ",len(profile))
        print("predict: ",test_target,'days')
        print("max drawdown: ",calculate_max_drawdown(pd.Series(profile)))
        draw_list(profile,buy_list,sell_list,gold_list,position_list,free_list,"./results_pic/"+str(test_target)+str(model_n)+'.jpg')
        print("final value :", cur_free+cur_position*cur_price)
        print("win rate :", (cur_free+cur_position*cur_price)/gold_list[-1])
    

