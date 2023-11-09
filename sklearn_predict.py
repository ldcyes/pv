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

df_org = pd.read_csv("STOCK_DATA.csv")
x_stocks=['SOXX','QQQ']
y_stock='SOXX'
features = ["7 day up","7 day down","price/up day","price/mid day","price/low day","price/up week","price/mid week","volume",
                   "price/low week","price/up month","price/mid month","price/low month","price/20high","price/20low"]
features_remain = []
features_x = []
for stock in x_stocks:
       for feature in features:
              features_remain.append(stock+feature)
              features_x.append(stock+feature)

features_remain.append(y_stock+"gain")

print("orginal data shape")
print(df_org.shape)
filtered_df = df_org[features_remain][0:-2]
print("get require feature data shape")
print(filtered_df.shape)
filtered_df= filtered_df.dropna()
print("drop NA value data shape")
print(filtered_df.shape)
print(filtered_df)
'''
filtered_df = df[(df['SOXXprice/up day'] != 0) & (df['SOXXprice/mid day'] != 0) & (df['SOXXprice/low day'] != 0) &
                 (df['SOXXprice/up week'] != 0) & (df['SOXXprice/mid week'] != 0) & (df['SOXXprice/low week'] != 0)&
                 (df['SOXXprice/up month'] != 0) & (df['SOXXprice/mid month'] != 0) & (df['SOXXprice/low month'] != 0)&
                 (df['SOXXprice/20high'] != 0) & (df['SOXXprice/20low'] != 0) &(df['SOXXgain'] != 0)&(df['SOXXvolume'] != 0)&
                 (df['QQQprice/up day'] != 0) & (df['QQQprice/mid day'] != 0) & (df['QQQprice/low day'] != 0) &
                 (df['QQQprice/up week'] != 0) & (df['QQQprice/mid week'] != 0) & (df['QQQprice/low week'] != 0)&
                 (df['QQQprice/up month'] != 0) & (df['QQQprice/mid month'] != 0) & (df['QQQprice/low month'] != 0)&
                 (df['QQQprice/20high'] != 0) & (df['QQQprice/20low'] != 0) &(df['QQQgain'] != 0)&(df['QQQvolume'] != 0)]
'''

#print(filtered_df)
train,test = train_test_split(filtered_df,test_size=0.1,shuffle=True)

train_x = train[features_x]
test_x = test[features_x]
print("train data shape")
print(train[features_remain].shape)
print("test data shape")
print(test[features_remain].shape)
train_y = train[y_stock+"gain"]
test_y  = test[y_stock+"gain"]

ss = MinMaxScaler()

model_list=[DecisionTreeRegressor(),
            SVR(kernel='rbf',gamma=0.1,C=1.0),
            RandomForestRegressor(),
            #MLPRegressor(hidden_layer_sizes=(64, 16), solver='adm', alpha=1e-5, random_state=1),
            #SGDRegressor(penalty='l2', max_iter=10000, tol=1e-5),
            XGBRegressor(objective='reg:squarederror')]
            #Ridge()]

model_name=['decision tree','SVM','RandomForest',#'MLP','SGD',
'XGboost']
i=0
print(df_org['QQQdate'][-1:])
print(df_org[features_remain][-1:])
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
       price=model.predict(df_org[features_x][-1:])
       print("predict value")
       print(price)




