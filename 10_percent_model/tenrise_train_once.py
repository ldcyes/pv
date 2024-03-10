from sklearn import svm
from sklearnex import patch_sklearn,unpatch_sklearn
patch_sklearn()
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
from tenrise_global_var import *

df_org = pd.read_csv("./stock_data/10rise_TRAIN_DATA.csv")

print("------------------=== data preprocess ===------------------")
features_remain=[]
features_x = []

features_remain.append("date")
for target in train_targets:
       features_remain.append("gain"+str(target))

for feature in features:
       features_x.append(feature)
       features_remain.append(feature)

print("orginal data shape")
print(df_org.shape)
filtered_df = df_org[features_remain][0:-1]
print("get require feature data shape")
print(filtered_df.shape)

filtered_df= filtered_df.replace([np.inf, -np.inf], np.nan).dropna()

print("drop NA value data shape")
print(filtered_df.shape)
print(filtered_df)

ss = MinMaxScaler()

model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(n_jobs=-1),
            MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
            SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
            XGBRegressor(objective='reg:squarederror')]

model_name=['decision tree','SVM','RandomForest','MLP','SGD',
            'XGboost']

i=0
print(filtered_df['date'][-1:])
print(filtered_df[features_remain][-1:])

col_list = []
for target in train_targets:
       for string in [' confid']:
              col_list.append(str(target)+string)

res_df = pd.DataFrame(columns=col_list,index=model_name)

for target in train_targets:

       train,test= train_test_split(filtered_df,test_size=test_size,shuffle=True)
       test_x = test[features_x]
       train_x = train[features_x]
       train_y = train["gain"+str(target)]
       test_y  = test["gain"+str(target)]
       print("train data shape")
       print(train_x.shape)
       print("test data shape")
       print(test_x.shape)

       print("------------------------------ "+ str(target)+ " day new training and test --------------------------------")

       i=0
       confidence=[]
       price_list=[]
       mean_price=0

       for model in model_list:
       
              print("------ switch model ------")
              print(model_name[i])
              model.fit(train_x.values,train_y)
              predictions = model.predict(test_x.values)
              print("trainning error")
              print(mean_squared_error(test_y, predictions))
              res_df.loc[str(model_name[i]),str(target)+' confid']=mean_squared_error(test_y, predictions)

              with open("./model_save/"+str(model_name[i])+str(target)+'_10rise_model.pkl','wb') as f:
                     pickle.dump(model, f)

              i=i+1

              #price=model.predict(df_org[features_x][-1:])
              #print("predict value")
              #print(price)
              #price_list.append(price.tolist()[0])

print("------------------------------ summary --------------------------------")
print(res_df)



