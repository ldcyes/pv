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

df_org = pd.read_csv("./stock_data/STOCK_TRAIN_DATA.csv")

print("------------------=== data preprocess ===------------------")
features_remain = []
features_x = []
for stock in x_stocks:
       for feature in features:
              features_remain.append(stock+feature)
              features_x.append(stock+feature)

for target in train_targets:
       features_remain.append(y_stock+"gain"+str(target))

print("orginal data shape")
print(df_org.shape)
filtered_df = df_org[features_remain][0:-2]
print("trained feature data shape")
print(filtered_df.shape)
filtered_df= filtered_df.dropna()
print("train data drop NA value data shape")
print(filtered_df.shape)
print(filtered_df)


print("------------------=== split train and testset ===------------------")
train,test = train_test_split(filtered_df,test_size=test_size,shuffle=True)

test_x = test[features_x]
train_x = train[features_x]
print("train data shape")
print(train[features_remain].shape)
print("test data shape")
print(test[features_remain].shape)

ss = MinMaxScaler()
model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(),
            MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
            SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
            XGBRegressor(objective='reg:squarederror')]

model_name=['decision tree','SVM','RandomForest','MLP','SGD',
            'XGboost']
i=0
print("------------------=== start trainning ===------------------")
print("latest day date")
print(df_org[y_stock+'date'][-1:])
print("latest day features")
print(df_org[features_remain][-1:])

col_list = []
for target in train_targets:
       for string in [' pred',' confid']:
              col_list.append(str(target)+string)

res_df = pd.DataFrame(columns=col_list,index=model_name)

for target in train_targets:
       print("------------------------------ "+str(target)+" day train predict new training and test --------------------------------")
      
       train_y = train[y_stock+"gain"+str(target)]
       test_y  = test[y_stock+"gain"+str(target)]
       i=0
       confidence=[]
       price_list=[]
       mean_price=0
       for model in model_list:
       
            print("------ switch model ------")
            print(model_name[i])
            model.fit(train_x,train_y)
            predictions = model.predict(test_x)
            print("trainning error")
            print(mean_squared_error(test_y, predictions))
            with open('./model_save/'+str(model_name[i])+str(target)+'_model.pkl','wb') as f:
                   pickle.dump(model, f)
            print("------ test latest day ------")
            print(df_org[features_x][-1:].shape)
            price=model.predict(df_org[features_x][-1:])
            res_df.loc[str(model_name[i]),str(target)+' pred']  =price
            res_df.loc[str(model_name[i]),str(target)+' confid']=mean_squared_error(test_y, predictions)
            print("predict value")
            print(price)      
            i=i+1

print(res_df)