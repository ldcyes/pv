from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
import pandas as pd

df = pd.read_csv("2012061720231107day.csv")
df = df.loc[0:2864,:]
df=df.fillna(0)

features_remian = ["SOXXprice/up day","SOXXprice/mid day","SOXXprice/low day","SOXXprice/up week","SOXXprice/mid week",
                   "SOXXprice/low week","SOXXprice/up month","SOXXprice/mid month","SOXXprice/low month","SOXXprice/20high","SOXXprice/20low"]

print(df.shape)

filtered_df = df[(df['SOXXprice/up day'] != 0) & (df['SOXXprice/mid day'] != 0) & (df['SOXXprice/low day'] != 0) &
                 (df['SOXXprice/up week'] != 0) & (df['SOXXprice/mid week'] != 0) & (df['SOXXprice/low week'] != 0)&
                 (df['SOXXprice/up month'] != 0) & (df['SOXXprice/mid month'] != 0) & (df['SOXXprice/low month'] != 0)&
                 (df['SOXXprice/20high'] != 0) & (df['SOXXprice/20low'] != 0) &(df['SOXXgain'] != 0)]

print(filtered_df)
train,test = train_test_split(filtered_df,test_size=0.03)

train_x = train[features_remian]
test_x = test[features_remian]
#print(test[features_remian].shape)
train_y = train["SOXXgain"]
test_y  = test["SOXXgain"]

ss = MinMaxScaler()
#train_x = ss.fit_transform(train_x)
#print("data max",ss.data_max_)
#test_x = ss.fit_transform(test_x)
##print("data max",ss.data_max_)

#print(test_x)

model = DecisionTreeRegressor()#SVR(kernel='rbf')
print(train_x.shape)
print(train_y.shape)
model.fit(train_x,train_y)

print(test_x.shape)
predictions = model.predict(test_x)
print(predictions.shape)
print(mean_squared_error(test_y, predictions))

list_data = [
0.952793291,1.021870766,1.101747407,0.892838203,0.971634213,1.065684496,0.875137225,1.12606582,1.578738372,0.96806318,1.082120535]

#print(accuracy_score(test_y,predictions))
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
df_test=pd.DataFrame(data)
print(df_test)
#df_test=ss.fit_transform(df_test)
#print("data max",ss.data_max_)
price=model.predict(df_test)
print(df_test.shape)
print(price.shape)
print(price)





