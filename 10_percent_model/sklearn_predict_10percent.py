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

df_org = pd.read_csv("./stock_data/10percent_TRAIN_DATA.csv")

features_remain=features
features_x     =features

for target in train_targets:
       features_remain.append("gain"+target)

print("orginal data shape")
print(df_org.shape)
filtered_df = df_org[features_remain][0:-2]

print("get require feature data shape")
print(filtered_df.shape)

filtered_df= filtered_df.replace([np.inf, -np.inf], np.nan).dropna()

print("drop NA value data shape")
print(filtered_df.shape)
print(filtered_df)

ss = MinMaxScaler()

model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(),
            MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
            #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
            XGBRegressor(objective='reg:squarederror')]
            #Ridge()]

model_name=['decision tree','SVM','RandomForest','MLP',#'SGD',
            'XGboost']

i=0
print(df_org['date'][-1:])
print(df_org[features_remain][-1:])

for target in train_targets:

       x_train,x_test,y_train,y_test = train_test_split(filtered_df[features_x],filtered_df["gain"+target],test_size=test_size,shuffle=True)

       print("train data shape")
       print(x_train.shape)
       print("test data shape")
       print(x_test.shape)
       print("------------------------------ new training and test --------------------------------")
       print(str(target)+" day train predict #################")
       i=0
       confidence=[]
       price_list=[]
       mean_price=0
       for model in model_list:
       
              print("------ switch model ------")
              print(model_name[i])
              model.fit(x_train,y_train)
              predictions = model.predict(x_test)
              print("trainning error")
              print(mean_squared_error(y_test, predictions))
              with open("./10_percent_model/"+str(model_name[i])+str(target)+'_model.pkl','wb') as f:
                     pickle.dump(model, f)

              i=i+1

              price=model.predict(df_org[features_x][-1:])
              print("predict value")
              print(price)
              price_list.append(price.tolist()[0])

       print("------------------------------ summary --------------------------------")
       import math




