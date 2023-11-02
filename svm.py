from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd

df = pd.read_excel("my analysis.xlsx")

df["buy"]=df[""]


features_remian = []
train,test = train_test_split(df,test_size=0.3)

train_x = train[features_remian]
test_x = test[features_remian]

train_y = train["buy"]
test_y  = test["buy"]

ss = StandardScaler()
train_x = ss.fit_transform(train_x)
test_x = ss.fit_transform(test_x)

model = SVC(C=1.0,kernel='rbf',gamma='scale')
model.fit(train_x,train_y)

predictions = model.predict(test_x)
print(accuracy_score(test_y,predictions))





