
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

def draw_list(my_list,buy_point,sell_point,file_name):
     # 使用numpy创建一个时间和数值对  
    time = np.arange(len(my_list))  
    value = my_list  
    
    # 创建曲线图  
    plt.figure(figsize=(10, 6))  
    plt.plot(time, value     ,label='net_value',color='red')
    plt.plot(time, buy_point ,label='buy',color='blue')  
    plt.plot(time, sell_point,label='sell',color='yellow')  
    plt.title('Your Data Curve')  
    plt.xlabel('Time')  
    plt.ylabel('net value')  
    plt.grid(True)  
    #plt.show()
    plt.savefig(file_name)

df_org = pd.read_csv("STOCK_DATA.csv")
#x_stocks=['TSLA','QQQ']
#y_stock='TSLA'
#targets = ['1','5','10','20']
#x_stocks=['中芯国际']
#y_stock='中芯国际'
features = ["7 day up","7 day down","price/up day","price/mid day","price/low day","price/up week","price/mid week","volume",
                   "price/low week","price/up month","price/mid month","price/low month","price/20high","price/20low"]
features_remain = []
features_x = []
for stock in x_stocks:
       for feature in features:
              features_remain.append(stock+feature)
              features_x.append(stock+feature)
for target in targets:
       features_remain.append(y_stock+"gain"+target)

print("orginal data shape")
print(df_org.shape)
print(df_org.shape[0])
#filtered_df = df_org[features_remain][0:-2]
print("get require feature data shape")
#print(filtered_df.shape)
#filtered_df= filtered_df.dropna()
model_name=[
#'decision tree',
#'SVM',
'RandomForest'
#'MLP',
#'SGD',
#'XGboost'
]

net_value = 20000
cur_free  = 20000
cur_price = 0
cur_position = 0
buy_position = 100
sell_position = 100

buy_list  = []
sell_list = []
profile = []

for day in range(400,2600):
    predict_avg = 0
    cur_price=df_org[y_stock+'close'][day]
    buy_condition = 0
    sell_condition = 0

    if(True):#not(df_org[features_x][:day].isna().any())):
        predict_avg = 0
        for target in targets:
            for model_n in model_name:
                model = pickle.load(open(str(model_n)+str(target)+'_model.pkl','rb'))
                predict_result = model.predict(df_org[day:day+1][features_x])
                predict_avg = predict_result+predict_avg
        buy_condition = (predict_avg/(len(targets)*len(model_name))) > 1.05
        sell_condition = (predict_avg/(len(targets)*len(model_name))) < 0.95

        if(buy_condition):
            if((buy_position * cur_price) < cur_free ):
                cur_free     =- buy_position*cur_price
                cur_position =+ buy_position
        if(sell_condition):
            if(cur_position>sell_position):
                cur_free     =+ sell_position*cur_price
                cur_position =- sell_position

    if(buy_condition and ((buy_position * cur_price) < cur_free)):
         buy_list.append(buy_position*cur_price)
    else:
         buy_list.append(0)
    if(sell_condition and (cur_position>sell_position)):
         sell_list.append(sell_position*cur_price)
    else:
         sell_list.append(0)
    
    profile.append(cur_free+cur_position*cur_price)
    
draw_list(profile,buy_list,sell_list,'this.jpg')
print("final value :", cur_free+cur_position*cur_price)