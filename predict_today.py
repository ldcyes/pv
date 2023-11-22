
import pandas as pd
import pickle
from global_var import *

df_org = pd.read_csv("STOCK_TEST_DATA.csv")

features_x = []
for stock in x_stocks:
       for feature in features:
              features_x.append(stock+feature)

print(df_org[y_stock+'date'][-1:])

for test_target in test_targets:
    for model_n in test_model_name:
        model = pickle.load(open(str(model_n)+str(test_target)+'_model.pkl','rb'))
        price=model.predict(df_org[features_x][-1:])
        print("---------------------------- ====== -------------------------------")
        print("model name",model_n,"predict day",test_target,"predict value")
        print(price)
        