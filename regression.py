
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
from sklearn.externals import joblib

df_org = pd.read_csv("STOCK_DATA.csv")
x_stocks=['TSLA','QQQ']
y_stock='TSLA'
targets = ['1','5','10','20']
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
filtered_df = df_org[features_remain][0:-2]
print("get require feature data shape")
print(filtered_df.shape)
filtered_df= filtered_df.dropna()

model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(),
            #MLPRegressor(hidden_layer_sizes=(64, 16), solver='adm', alpha=1e-5, random_state=1),
            #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
            XGBRegressor(objective='reg:squarederror')]
            #Ridge()]

model_name=['decision tree','SVM','RandomForest','XGboost']

net_value = 10000
cur_free  = 10000
cur_price = 0
cur_position = 0
buy_position = 100
sell_position = 100

for day in df:
    cur_price = dd
    i=0
    for model in model_list: 
        model = joblib.load(model_name[i]+'_model.pkl')
        i=i+1
        predict_price=model.predict(df_org[features_x][-1:])
    if(predict_price>1.05):
        if((buy_position * cur_price) < cur_free ):
            cur_free     =- buy_position*cur_price
            cur_position =+ buy_position
    if(predict_price<0.95):
        cur_free     =+ sell_position*cur_price
        cur_position =- sell_position

print("final value :", cur_free+cur_position*cur_price)