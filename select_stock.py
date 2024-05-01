import get_stock
import pandas as pd
from datetime import datetime
import get_stock_data
from global_var import *
import train_once

#stock_list = get_stock_data.get_stock_list()
stock_list = NASDAQ_100

col_list = []
for target in train_targets:
    for string in [' pred',' confid']:
        col_list.append(str(target)+string)

model_name=['RandomForest',#'MLP','SGD',
            'XGboost']

res_df = pd.DataFrame(columns=col_list,index=model_name)

for stock in stock_list:
    
    current_date = datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')

    if(train):
        start_date = train_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TRAIN_DATA.csv"
    else:
        start_date = test_start_date
        end_date   = str(formatted_date)
        file_name = "STOCK_TEST_DATA.csv"

    table= get_stock_data.build_frame(['QQQ',stock],start_date,end_date)

    csv_df = pd.DataFrame(data=table,index=None)
    csv_df.to_csv("./stock_data/"+str(stock)+file_name)
    
    res_df = train_once.train_once(csv_df,res_df,x_stocks=['QQQ',stock],train_targets=train_targets,y_stock=stock,features=features)

res_df = res_df.sort_values(by=' pred',ascending=False)
print(res_df)
res_df.to_csv("./stock_data/stock_select_result.csv",index=False)
