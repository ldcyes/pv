import pandas as pd
import numpy as np
import pickle
from tenrise_global_var import *
from datetime import datetime

def predict_now():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y%m%d')

    df_org = pd.read_csv("./stock_data/10rise_TEST_DATA.csv")

    features_x = []
    features_remain = []
    features_remain.append("date")
    features_remain.append("key")
    features_remain.append("close")
    for feature in features:
        features_x.append(feature)
        features_remain.append(feature)

    for target in test_targets:
        features_remain.append("gain"+str(target))

    filtered_df= df_org[features_remain][0:-1]
    print("with NA value data shape")
    print(filtered_df.shape)
    test_date='2024-03'#str(formatted_date)
    #test_df_new = filtered_df[filtered_df['date'].dt.strftime('%Y-%m').str.contains('2024-03')]
    filtered_df=filtered_df.replace([np.inf, -np.inf], np.nan).dropna(subset=features_x)
    
    print("drop NA value data shape")
    print(filtered_df.shape)
    print("last day price, stock name")
    print(filtered_df['date'][-1:])
    print(filtered_df['key'][-1:])

    res_df=pd.DataFrame()
    import copy

    for test_target in test_targets:
        for model_n in test_model_name:
            print(model_n)
            model = pickle.load(open('./model_save/'+str(model_n)+str(test_target)+'_10rise_model.pkl','rb'))
            test_df=filtered_df#filtered_df[filtered_df['date']==test_date]
            res_df=copy.deepcopy(test_df[['key','date','price/20low']])
            print(test_df[features_x].shape)
            #test_df_new = test_df['date'].str.contains(test_date)
            res_df.loc[:,'pred price']=model.predict(test_df.loc[-1:,features_x].values)
            print("---------------------------- post process ====== -------------------------------")
            print("model name",model_n,"predict hold day",test_target)
            res_df=res_df.sort_values(by='pred price',ascending=False)

            i=0
            res_df=res_df[res_df['date'].astype(str).str.contains(test_date)]
            res_df=res_df.head(20)
            for index in res_df.index:
                i=i+1
                if(i>30):
                    break
                print("key",res_df.loc[index,'key'],
                      "date",res_df.loc[index,'date'],
                      "price rise pred",res_df.loc[index,'pred price'],
                      "present 20day rise",res_df.loc[index,'price/20low'])
    return res_df
if __name__ == '__main__':
    res = predict_now() 
