from sklearnex import patch_sklearn,unpatch_sklearn
patch_sklearn()
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
import csv
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
     
def regression(df_org,features_remain,features_x,regress_start_date,regression_train_targtes,change,regression_log,back_time):
     net_value = 100000
     start_value = 100000
     cur_free  = 100000

     cur_position = 0
     buy_position = 10
     sell_position = 1
     buy_list  = []
     sell_list = []
     gold_list = []
     profile = []
     position_list =[]
     free_list = []
     model_list_record = []
     # 将这三个列表按列存储在一个csv文件中

     file = open('profilo_inference_'+str(stock)+'DayRange'+str(regression_train_targtes[0])+'_Sheshold'+str(reg_inc_pcent[str(regression_train_targtes[0])])+'_stock_regression'+str(y_stock)+'_Change'+str(change)+'_Backtime'+str(back_time)+'_DayTrained'+str(df_org.shape[0])+'.csv', 'w', newline='')
     writer = csv.writer(file)
     writer.writerow(["date", "lastday_close_price", "profile","gold profile","price_predict","model","buy condition","buy position","sell condition","sell position","cur position","cur free"])
     
     # increment the data for trainning and inference with new trainning data
     is_first_price = 1
     print(regress_start_date,df_org.shape[0])
     
     for date in range(regress_start_date,df_org.shape[0]+1,1):
     
          print("------------------=== inc one day and train from beginning ===------------------")
          # trainning , must without gain 20 nan
          # inference , gain 20 can have nan
          filtered_df = df_org.iloc[0:date][features_remain].copy()
          #print("last date before filtered",df_org.iloc[-1]['QQQdate'])
          print("get require feature data shape")
          print(filtered_df.shape)
          #print("last line has NA data?",filtered_df.iloc[-1].isna().values.any())
          filtered_df= filtered_df.replace([np.inf, -np.inf], np.nan).copy()
          # 2009-07-01... 2012-08-24 2012-08-27 2012-08-28
          filtered_df_trainning = filtered_df.dropna().copy()
          filtered_df_inference = filtered_df.dropna(subset=features_x).copy()
          print("drop NA value data shape")
          print(filtered_df.shape)
          print("train shape")
          
          #print("last date after filtered",filtered_df_inference.iloc[-1]['QQQdate'])
          # except last day of training
          # 2009-07-01...2012-08-24
          # 637+160=797
          train,test = train_test_split(filtered_df_trainning[features_remain][0:-2],test_size=test_size,shuffle=True)
          train_x = train[features_x]
          test_x = test[features_x]
          print("train data shape")
          print(train[features_remain].shape)
          print("test data shape")
          print(test[features_remain].shape)
     
          ss = MinMaxScaler()
          model_list=[#DecisionTreeRegressor(),
                      #SVR(kernel='rbf',gamma=0.1,C=1.0),
                      RandomForestRegressor(n_jobs=-1),
                      #MLPRegressor(hidden_layer_sizes=(128,512,1024),activation='tanh', solver='adam', alpha=1e-5, random_state=1),
                      #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
                      XGBRegressor(n_jobs=-1)]
          
          model_name=[#'decision tree',
               #'SVM',
               'RandomForest',
               #'MLP',
               #'SGD',
               'XGboost']
          
          print("train start date",filtered_df_trainning.iloc[0][y_stock+'date'])  #    2009-07-01
          #print(filtered_df[features_remain][0:1])
          print("train end date",filtered_df_trainning.iloc[-3][y_stock+'date'])   #    2012-08-24
          #print(filtered_df[features_remain][-2:-1])
          print("test date",filtered_df_inference.iloc[-2][y_stock+'date'])        #    2012-08-27 -> predict 2012-08-28
          #print(filtered_df[features_remain][-1:])
     
          trainendday_close_price    =filtered_df_inference.iloc[-3][y_stock+'close'] # train end day price
          testday_close_price        =filtered_df_inference.iloc[-2][y_stock+'close'] # test day price
          exeday_open_price          =filtered_df_inference.iloc[-1][y_stock+'close']  # exe day open price
          
          sharp_down_sell_condition =  testday_close_price/trainendday_close_price < 0.9566 #test only

          if(is_first_price):
               first_price = testday_close_price
               is_first_price = 0
               cur_position = int(start_value/exeday_open_price)
               cur_free = start_value - cur_position*exeday_open_price
               last_buy_condition = 0
               last_sell_condition = 0
     
          for target in regression_train_targtes:
                 
               print("------------------------------  "+ str(target)+" day new training and test --------------------------------")
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
                    model.fit(train_x.values,train_y)
                    predictions = model.predict(test_x.values)
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
                    #print(filtered_df_inference[features_x][-1:].shape)
                    print(filtered_df_inference[-2:][y_stock+'date']) # 2012-08-27
                    if(sel_model==1):
                         #print(filtered_df_inference[features_remain][-1:]) # 2012-08-27
                         # where price is a rise ratio , not absolute price
                         price=model.predict(filtered_df_inference[features_x][-2:-1].values)
                         print("predict value")
                         print(price)
                         model_list_record.append(model_name[i-1])
                         price_list.append(price.tolist()[0])

               print("------------------------------ train end ------------------------------")

               buy_shreshold  = 1+reg_inc_pcent[str(target)]
               sell_shreshold = 1-reg_inc_pcent[str(target)]
               
               sell_condition = price <= sell_shreshold and last_sell_condition >= cnt_sell
               sell_condition = sell_condition or sharp_down_sell_condition
               if(sell_condition==False):
                    buy_condition  = price >= buy_shreshold and last_buy_condition >= cnt_buy

               # 连续记录达到sell和buy条件的次数
               if(price >= buy_shreshold):
                    last_buy_condition += price >= buy_shreshold
               else:
                    last_buy_condition = 0
               if(price <= sell_shreshold):
                    last_sell_condition += price <= sell_shreshold
               else:
                    last_buy_condition = 0
     
               # how much to buy and sell
               buy_position = 0
               sell_position = 0
               if(sell_condition):
                    sell_position = int(cur_position*change)
                    if(cur_position>=sell_position):
                         cur_free     = cur_free + sell_position*exeday_open_price
                         cur_position = cur_position - sell_position
                    else:
                         cur_free = cur_free + exeday_open_price*cur_position
                         cur_position = 0
               elif(buy_condition):
                    buy_position = int(cur_free/exeday_open_price*change)
                    if((buy_position * exeday_open_price) < cur_free ):
                         cur_free     = cur_free- buy_position*exeday_open_price
                         cur_position = cur_position+ buy_position
     
               position_list.append(cur_position*100)
               free_list.append(cur_free)
     
               if(buy_condition and ((buy_position * exeday_open_price) < cur_free)):
                    buy_list.append(buy_position*exeday_open_price)
               else:
                    buy_list.append(0)
               if(sell_condition and (cur_position>sell_position)):
                    sell_list.append(sell_position*exeday_open_price)
               else:
                    sell_list.append(0)
     
               profile.append(cur_free+cur_position*exeday_open_price)
               gold_list.append(exeday_open_price*start_value/first_price)
               
               writer.writerow([filtered_df_inference[-1:][y_stock+'date'],        # exe date 2012-08-28
                                exeday_open_price,                                 # exe date price 2012-08-28 price
                                cur_free+cur_position*exeday_open_price,           # profile
                                exeday_open_price*(start_value/first_price),       # always hold value
                                price,
                                model_name,
                                buy_condition,                # buy condition   
                                buy_position,                    # buy position
                                sell_condition,
                                sell_position,
                                cur_position,          # cur position
                                cur_free])             # cur free
     
     print("------=====------")
     print("valid days: ",len(profile))
     print("predict: ",target,'days')
     print("max drawdown: ",calculate_max_drawdown(pd.Series(profile))) 
     draw_list(profile,buy_list,sell_list,gold_list,position_list,free_list,
               "./results_pic/DayWeekMonthRange"+str(target)+'_Sheshold'+str(reg_inc_pcent[str(target)])+'_StockRegression'+str(y_stock)+'_Change'+str(change)+'_Backtime'+str(back_time)+'_Dayspend'+str(len(profile))+'.jpg')
     print("final value :", cur_free+cur_position*exeday_open_price)
     print("win rate :", (cur_free+cur_position*exeday_open_price)/gold_list[-1])
     writer.writerow([str(y_stock), regression_train_targtes,
                              change,len(profile),calculate_max_drawdown(pd.Series(profile)),
                              reg_inc_pcent[str(target)],
                              cur_free+cur_position*exeday_open_price,(cur_free+cur_position*exeday_open_price)/gold_list[-1]])
     regression_log.writerow([str(y_stock), regression_train_targtes,
                              change,len(profile),calculate_max_drawdown(pd.Series(profile)),
                              reg_inc_pcent[str(target)],
                              cur_free+cur_position*exeday_open_price,(cur_free+cur_position*exeday_open_price)/gold_list[-1],back_time])
     file.close()

if __name__ == "__main__":

     print("------------------=== prepare data ===------------------")

     df_org = pd.read_csv("./stock_data/SOXXSTOCK_TRAIN_DATA.csv")
     
     file = open('profilo_inference_all.csv', 'w', newline='')
     writer = csv.writer(file)
     writer.writerow(["stock","train_target","change","valid days","max drawdown","inc_sheshold","final value","win rate","back_time"])

     for back_time in back_times:
     
          features =get_features_name(back_time)
          features_x = []
          features_remain = []

          for stock in x_stocks:
               features_remain.append(stock+'date')
               features_remain.append(stock+'close')

               for feature in features:
                    features_remain.append(stock+feature)
                    features_x.append(stock+feature)

          features_remain.append(y_stock+'date')
          features_remain.append(y_stock+'close')
          for feature in features:
               features_remain.append(y_stock+feature)
               features_x.append(y_stock+feature)

          for target in train_targets:
                 features_remain.append(y_stock+"gain"+str(target))

          print("orginal data shape")
          print(df_org.shape)

          for train_target in regression_train_targtes:
               for change in changes:
                    regression(df_org,features_remain,features_x,regress_start_date,train_target,change,writer,back_time)

