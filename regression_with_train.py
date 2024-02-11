from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.linear_model import SGDRegressor  
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor  
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

print("------------------=== prepare data ===------------------")
df_org = pd.read_csv("./stock_data/STOCK_TRAIN_DATA.csv")

features_x = []
features_remain = []
for stock in x_stocks:
       features_remain.append(stock+'date')
       features_remain.append(stock+'close')
       
       for feature in features:
              features_remain.append(stock+feature)
              features_x.append(stock+feature)

for target in train_targets:
       features_remain.append(y_stock+"gain"+str(target))

print("orginal data shape")
print(df_org.shape)

net_value = 100000
start_value = 100000
cur_free  = 100000
cur_price = 0
cur_position = 0
buy_position = 10
sell_position = 1
buy_list  = []
sell_list = []
gold_list = []
profile = []
position_list =[]
free_list = []

# increment the data for trainning and inference with new trainning data
first_price=df_org[y_stock+'close'][0]
print(regress_start_date,df_org.shape[0])
for date in range(regress_start_date,df_org.shape[0],1):

     print("------------------=== inc one day and train from beginning ===------------------")

     filtered_df = df_org.iloc[0:date][features_remain]
     print("get require feature data shape")
     print(filtered_df.shape)
     filtered_df= filtered_df.replace([np.inf, -np.inf], np.nan).dropna()
     print("drop NA value data shape")
     print(filtered_df.shape)
     #print(filtered_df)
     train,test = train_test_split(filtered_df[features_remain][0:-2],test_size=test_size,shuffle=True)
     train_x = train[features_x]
     test_x = test[features_x]
     print("train data shape")
     print(train[features_remain].shape)
     print("test data shape")
     print(test[features_remain].shape)

     ss = MinMaxScaler()
     model_list=[#DecisionTreeRegressor(),
                 #SVR(kernel='rbf',gamma=0.1,C=1.0),
                 RandomForestRegressor(),
                 #MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
                 #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
                 XGBRegressor(objective='reg:squarederror')]
     
     model_name=[#'decision tree',
          #'SVM',
          'RandomForest',
          #'MLP',
          #'SGD',
          'XGboost']
     print(filtered_df.iloc[0][y_stock+'date'])
     print(filtered_df.iloc[-2][y_stock+'date'])     
     print(filtered_df.iloc[-1][y_stock+'date'])

     cur_price=filtered_df.iloc[-2][y_stock+'close']

     for target in train_targets:
            
          print("------------------------------ new training and test --------------------------------")
          print(str(target)+" day train predict #################")
          train_y = train[y_stock+"gain"+str(target)]
          test_y  = test[y_stock+"gain"+str(target)]
          i=0
          confidence=[]
          price_list=[]
          mean_price=0
          mean_squared_error_value = 10000
          sel_model = 0
          for model in model_list:
          
               print("------------ switch model ------------")
               print(model_name[i])
               
               model.fit(train_x,train_y)
               predictions = model.predict(test_x)
               print("trainning error")
               print(mean_squared_error(test_y, predictions))
               # the mimimal loss predict will be recorded
               if(mean_squared_error(test_y, predictions)<mean_squared_error_value):
                    mean_squared_error_value =  mean_squared_error(test_y, predictions)
                    sel_model = 1
               # on need to record model
               #with open("./model/"+str(model_name[i])+str(target)+'_model.pkl','wb') as f:
               #       pickle.dump(model, f)
               i=i+1
               print(filtered_df[features_x][-1:].shape)
               print(filtered_df[-1:][y_stock+'date'])
               if(sel_model==1):
                    price=model.predict(filtered_df[features_x][-1:])
                    print("predict value")
                    print(price)
                    price_list.append(price.tolist()[0])
          print("------------------------------ train end ------------------------------")

          buy_condition  = price >= 1.05
          sell_condition = price <= 0.95
          # how much to buy and sell
          buy_position = int(cur_free/cur_price*0.25)
          sell_position = int(cur_position*0.25)

          if(buy_condition):
               if((buy_position * cur_price) < cur_free ):
                    cur_free     = cur_free- buy_position*cur_price
                    cur_position = cur_position+ buy_position
          if(sell_condition):
               if(cur_position>sell_position):
                    cur_free     = cur_free + sell_position*cur_price
                    cur_position = cur_position - sell_position
               else:
                    cur_free = cur_free + cur_price*cur_position
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

print("------=====------")
print("valid days: ",len(profile))
print("predict: ",target,'days')
print("max drawdown: ",calculate_max_drawdown(pd.Series(profile)))
draw_list(profile,buy_list,sell_list,gold_list,position_list,free_list,"./results_pic/"+str(target)+'.jpg')
print("final value :", cur_free+cur_position*cur_price)
print("win rate :", (cur_free+cur_position*cur_price)/gold_list[-1])
    


