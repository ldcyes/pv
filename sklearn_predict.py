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

df = pd.read_csv("STOCK_DATA.csv")
df=df.fillna(0)

features_remian = ["SOXX7 day up","SOXX7 day down","SOXXprice/up day","SOXXprice/mid day","SOXXprice/low day","SOXXprice/up week","SOXXprice/mid week","SOXXvolume",
                   "SOXXprice/low week","SOXXprice/up month","SOXXprice/mid month","SOXXprice/low month","SOXXprice/20high","SOXXprice/20low",
                   "QQQ7 day up","QQQ7 day down","QQQprice/up day","QQQprice/mid day","QQQprice/low day","QQQprice/up week","QQQprice/mid week","QQQvolume",
                   "QQQprice/low week","QQQprice/up month","QQQprice/mid month","QQQprice/low month","QQQprice/20high","QQQprice/20low"]

print(df.shape)

filtered_df = df[(df['SOXXprice/up day'] != 0) & (df['SOXXprice/mid day'] != 0) & (df['SOXXprice/low day'] != 0) &
                 (df['SOXXprice/up week'] != 0) & (df['SOXXprice/mid week'] != 0) & (df['SOXXprice/low week'] != 0)&
                 (df['SOXXprice/up month'] != 0) & (df['SOXXprice/mid month'] != 0) & (df['SOXXprice/low month'] != 0)&
                 (df['SOXXprice/20high'] != 0) & (df['SOXXprice/20low'] != 0) &(df['SOXXgain'] != 0)&(df['SOXXvolume'] != 0)&
                 (df['QQQprice/up day'] != 0) & (df['QQQprice/mid day'] != 0) & (df['QQQprice/low day'] != 0) &
                 (df['QQQprice/up week'] != 0) & (df['QQQprice/mid week'] != 0) & (df['QQQprice/low week'] != 0)&
                 (df['QQQprice/up month'] != 0) & (df['QQQprice/mid month'] != 0) & (df['QQQprice/low month'] != 0)&
                 (df['QQQprice/20high'] != 0) & (df['QQQprice/20low'] != 0) &(df['QQQgain'] != 0)&(df['QQQvolume'] != 0)]

#print(filtered_df)
train,test = train_test_split(filtered_df,test_size=0.1)

train_x = train[features_remian]
test_x = test[features_remian]
#print(test[features_remian].shape)
train_y = train["SOXXgain"]
test_y  = test["SOXXgain"]

ss = MinMaxScaler()

model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(),
            MLPRegressor(hidden_layer_sizes=(16, 64), solver='adam', alpha=1e-5, random_state=1),
            SGDRegressor(penalty='l2', max_iter=10, tol=1e-3),
            XGBRegressor(objective='reg:squarederror')]
            #Ridge()]

model_name=['decision tree','SVM','RandomForest','MLP','SGD','XGboost']
i=0
print(df['QQQdate'][-1:])
print(df[features_remian][-1:])
for model in model_list:
       
       print("------------------------------ new training and test --------------------------------")
       print(model_name[i])
       i=i+1
       model.fit(train_x,train_y)

       predictions = model.predict(test_x)
       print("trainning error")
       print(mean_squared_error(test_y, predictions))

       list_data = [
       0.952793291,1.021870766,1.101747407,0.892838203,0.971634213,1.065684496,0.875137225,1.12606582,1.578738372,0.96806318,1.082120535]

       #print(accuracy_score(test_y,predictions))
       '''
       data ={"SOXXprice/up day"   :[list_data[0]],
              "SOXXprice/mid day"  :[list_data[1]],
              "SOXXprice/low day"  :[list_data[2]],
              "SOXXprice/up week"  :[list_data[3]],
              "SOXXprice/mid week" :[list_data[4]],
              "SOXXprice/low week" :[list_data[5]],
              "SOXXprice/up month" :[list_data[6]],
              "SOXXprice/mid month":[list_data[7]],
              "SOXXprice/low month":[list_data[8]],
              "SOXXprice/20high"   :[list_data[9]],
              "SOXXprice/20low"    :[list_data[10]]}
       '''
       #df_test=pd.DataFrame(data)
       price=model.predict(df[features_remian][-1:])
       print("predict value")
       print(price)





