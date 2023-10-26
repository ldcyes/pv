import pandas as pd
import matplotlib.pyplot as plt

train_out = pd.read_csv('train_out.csv',index_col=0)
train_target = pd.read_csv('train_target.csv',index_col=0)

plt.clf()
plt.plot(train_out[700:-1],'b',label='test_pred')
plt.plot(train_target[700:-1],'r',label='test_true')
plt.legend(loc='best')
plt.savefig('compare.jpg')