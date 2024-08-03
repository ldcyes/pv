from sklearnex import patch_sklearn,unpatch_sklearn
patch_sklearn()
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler,StandardScaler
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
import argparse

def train_once(df_org,res_df,x_stocks=['QQQ','SOXX'],train_targets=[3,5,10,20],y_stock='SOXX',features=[]):
       #df_org = pd.read_csv("./stock_data/STOCK_TRAIN_DATA.csv")

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
       filtered_df = df_org[features_remain][0:-2].copy()
       print("trained feature data shape")
       print(filtered_df.shape)
       #filtered_df.to_csv("./stock_data/raw_STOCK_TRAIN_DATA.csv",index=False)
       filtered_df_trainning = filtered_df.replace([np.inf, -np.inf], np.nan).dropna().copy()
       filtered_df_inference = filtered_df.dropna(subset=features_x).copy()
       print("train data drop NA value data shape")
       print(filtered_df.shape)
       print(df_org)

       if(scale_type==0):
              scaler = StandardScaler()
       else:
              scaler = MinMaxScaler()
       
       #filtered_df.to_csv("./stock_data/before_STOCK_TRAIN_DATA.csv",index=False)
       #filtered_df['near1m_open'] = pd.DataFrame(scaler.fit_transform(filtered_df[['near1m_open']]))
       #filtered_df.to_csv("./stock_data/after_STOCK_TRAIN_DATA.csv",index=False)

       print("------------------=== split train and testset ===------------------")
       train,test = train_test_split(filtered_df_trainning,test_size=test_size,shuffle=True,random_state=88)

       test_x = test[features_x].values
       train_x = train[features_x].values
       print("train data shape")
       print(train[features_remain].shape)
       print("test data shape")
       print(test[features_remain].shape)

       model_list=[
                   #DecisionTreeRegressor(),
                   #SVR(kernel='rbf',gamma=0.1,C=1.0),
                   RandomForestRegressor(n_estimators=1000,n_jobs=-1,random_state=88),
                   #MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
                   #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
                   XGBRegressor(objective='reg:squarederror',random_state=88)]

       model_name=[#'decision tree',#'SVM',
                   'RandomForest',#'MLP','SGD',
                   'XGboost']
       i=0
       print("------------------=== start trainning ===------------------")
       print("latest day date")
       print(df_org[y_stock+'date'][-1:])
       print("latest day features")
       print(df_org[features_remain][-1:])

       # check the latest day features
       pd.DataFrame(data=df_org[features_remain][-1:].values,index=None).to_csv("./stock_data/latest_day_features.csv",index=False) 

       # result column name 
       col_list = []
       for target in train_targets:
              for string in [' pred',' confid']:
                     col_list.append(str(target)+string)

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
                   csv_df = pd.DataFrame(data=train_x,index=None)
                   csv_df.to_csv("./stock_data/"+str(model_name[i])+str(target)+'_train_x.csv',index=False)
                   model.fit(train_x,train_y)
                   predictions = model.predict(test_x)
                   print("trainning error")
                   print(mean_squared_error(test_y, predictions))
                   with open('./model_save/'+str(model_name[i])+str(target)+'_model.pkl','wb') as f:  
                        pickle.dump(model, f)
                   print("------ test latest day ------")
                   #print(df_org[features_x][-1:])
                   price=model.predict(df_org[features_x][-1:].values)
                   res_df.loc[str(model_name[i]),str(target)+' pred']  =price
                   res_df.loc[str(model_name[i]),str(target)+' confid']=mean_squared_error(test_y, predictions)
                   res_df.loc[str(model_name[i]),str(target)+' stock']=str(stock)
                   print("predict value")
                   print(price)      
                   i=i+1

       #print(res_df)

       return res_df

if __name__ == "__main__":

       parser = argparse.ArgumentParser(description='trainning model')
       parser.add_argument('--y_stock', type=str, default='SOXX', help='trainning stock')
       args = parser.parse_args()
       df_org = pd.read_csv("./stock_data/"+str(args.y_stock)+"STOCK_TRAIN_DATA.csv")
       
       col_list = []
       
       for target in train_targets:
              for string in [' pred',' confid']:
                     col_list.append(str(target)+string)
       
       model_name=[#'decision tree',#'SVM',
                   'RandomForest',#'MLP','SGD',
                   'XGboost']
       
       res_df = pd.DataFrame(columns=col_list,index=model_name)
       features = get_features_name(back_times[0])
       res_df=train_once(df_org,res_df,x_stocks=x_stocks+[str(args.y_stock)],train_targets=train_targets,y_stock=args.y_stock,features=features)
       print(res_df)