from random import shuffle
import model as md
import get_features as gf
from torch import nn
import torch
import numpy as np
from torch.utils.data import DataLoader
from torch.utils.data import TensorDataset
import pandas as pd
import matplotlib.pyplot as plt

# basic config
stock_codes = ['QQQ','NVDA','TSM','INTC']
key = 'SOXX'
log_interval = 1
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',None)
np.set_printoptions(threshold=np.inf)

epoch_num = 10
train_start_date = '20090617'
train_end_date = '20180617'
test_start_date = '20180617'
test_end_date = '20190617'

print("---====== create train data =======---")
train_xy = gf.create_dataset(stock_codes=stock_codes,targe_key=key,start_date=train_start_date,end_date=train_end_date)
train_x,train_y = gf.dataset_reshape(df=train_xy,target_key=key,stock_codes=stock_codes)
train_x  =  torch.where(torch.isnan(train_x),torch.full_like(train_x,0),train_x)

print("---====== create test data =======---")
test_xy = gf.create_dataset(stock_codes=stock_codes,targe_key=key,start_date=test_start_date,end_date=test_end_date)
test_x,test_y = gf.dataset_reshape(df=test_xy,target_key=key,stock_codes=stock_codes)
test_x  =  torch.where(torch.isnan(test_x),torch.full_like(test_x,0),test_x)

print(train_x.shape)
print(train_y.shape)
batch = 8
dataset = TensorDataset(train_x,train_y)
train_loader = DataLoader(dataset=dataset,batch_size=batch,shuffle=True,num_workers=1)

model = md.tuEncoder(input_size=1428,d_model=512,ffn_hidden=2048,n_head=8,n_layers =6,drop_prob=0.3)
#model.load_state_dic(torch.load("tuEncoder128_32.pt"))
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.01)

train_loss_list=[]

for epoch in range(epoch_num):
    if epoch == epoch_num -1:
        out_arr = torch.empty(0)
        label_arr = torch.empty(0)

    for i ,(inputs,lables) in enumerate(train_loader):
        optimizer.zero_grad()
        out = model.forward(x=inputs,s_mask=None)
        loss = criterion(out.view(-1),lables.view(-1))
        print("epoch",epoch,"step",i,"batch",i*len(inputs),"MSE:",loss.item())

        loss.backward()
        optimizer.step()

        if(i%log_interval==0):
            train_loss_list.append(loss.item())

        if(epoch==epoch_num -1):
            out_arr = torch.cat((out.view(-1),out_arr),0)
            label_arr = torch.cat((lables.view(-1),label_arr),0)

torch.save(model.state_dict(),'tuEncoder.pt')

# LOSS diagram , start from 20 epoch
plt.plot(train_loss_list[20:-1],'b',label='train_loss')
plt.legend(loc='best')
plt.savefig('train_loss.jpg')

plt.clf()
# flatten to 1d
plt.plot(out_arr.view(-1).data.numpy(),'b',label='train_pred')
plt.plot(label_arr.view(-1).data.numpy(),'r',label='train_true')
plt.legend(loc='best')
plt.savefig('final_train.jpg')

pred_test = model(x=test_x,s_mask=None)

plt.clf()
plt.plot(pred_test.view(-1).data.numpy(),'b',label='test_pred')
plt.plot(test_y.view(-1).data.numpy(),'r',label='test_true')
plt.legend(loc='best')
plt.savefig('test.jpg')