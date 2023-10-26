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
stock_codes = ['SOXX']#'NVDA','TSM','INTC','QQQ']
key = 'SOXX'
log_interval = 100
pd.set_option('display.width',1000)
pd.set_option('display.max_rows',None)
np.set_printoptions(threshold=np.inf)

epoch_num = 100
train_start_date = '20120617'
train_end_date   = '20220617'
test_start_date  = '20220617'
test_end_date    = '20230817'
torch.cuda.is_available()
print("---====== create train data =======---")
train_xy,train_close_min,train_close_scalar= gf.create_dataset(stock_codes=stock_codes,targe_key=key,start_date=train_start_date,end_date=train_end_date)
train_x,train_y = gf.dataset_reshape(df=train_xy,target_key=key,stock_codes=stock_codes)
train_x  =  torch.where(torch.isnan(train_x),torch.full_like(train_x,0),train_x)

plt.clf()
plt.plot(train_xy[key,'day']['收盘'],'b',label='train_target')
plt.savefig('train_target.jpg')

plt.clf()
plt.plot(train_xy[key,'day']['收盘_norm'],'b',label='train_target_norm')
plt.savefig('train_target_norm.jpg')


print("---====== create test data =======---")
test_xy,test_close_min,test_close_scalar = gf.create_dataset(stock_codes=stock_codes,targe_key=key,start_date=test_start_date,end_date=test_end_date)
test_x,test_y = gf.dataset_reshape(df=test_xy,target_key=key,stock_codes=stock_codes)
test_x  =  torch.where(torch.isnan(test_x),torch.full_like(test_x,0),test_x)
# where y is normlized close price
plt.clf()
plt.plot(test_xy[key,'day']['收盘'],'b',label='test_target')
plt.savefig('test_target.jpg')

plt.clf()
plt.plot(test_xy[key,'day']['收盘_norm'],'b',label='test_target_norm')
plt.savefig('test_target_norm.jpg')

print(train_x.shape)
print(train_y.shape)
batch = 8

dataset = TensorDataset(train_x,train_y)
train_loader = DataLoader(dataset=dataset,batch_size=batch,shuffle=False,num_workers=1)

model = md.tuEncoder(input_size=1428,d_model=2048,ffn_hidden=2048*4,n_head=16,n_layers =12,drop_prob=0.5)
#model = md.MLP(input_dimension=357,hidden_dimension=2048)
model.cuda()

#model.load_state_dict(torch.load("tumlp_epoch_100.pt"))
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(),lr=0.01)
#optimizer = torch.optim.SGD(lr=0.01,params=model.parameters())

train_loss_list=[]
out_arr = torch.empty(0)
out_arr = out_arr.to(device=torch.device('cuda'))
label_arr = torch.empty(0)
label_arr= label_arr.to(device=torch.device('cuda'))

for epoch in range(epoch_num):

    for i ,(inputs,lables) in enumerate(train_loader):
        optimizer.zero_grad()
        #out = model.forward(x=inputs,s_mask=None)
        inputs= inputs.to(device=torch.device('cuda'))
        lables= lables.to(device=torch.device('cuda'))
        #out = model.forward(inputs)
        out = model.forward(x=inputs,s_mask=None)
        loss = criterion(out,lables.reshape([-1,1,1]))

        loss.backward()
        optimizer.step()

        if(i%log_interval==0):
            train_loss_list.append(loss.item())
            print("epoch",epoch,"step",i,"batch",i*len(inputs),"MSE:",loss.item())

        #if(epoch==epoch_num -1):
        out_arr = torch.cat((out_arr,out.view(-1)),0)
        label_arr = torch.cat((label_arr,lables.view(-1)),0)

    if epoch == epoch_num -1:
        label_arr=label_arr.to(device=torch.device('cpu'))
        out_arr=out_arr.to(device=torch.device('cpu'))
        pd.DataFrame(out_arr.detach().numpy()).to_csv("train_out.csv")
        pd.DataFrame(label_arr.detach().numpy()).to_csv("train_target.csv")
        plt.plot(train_loss_list[20:-1],'b',label='train_loss')
        plt.legend(loc='best')
        plt.savefig('loss.jpg')

#torch.save(model.state_dict(),'MLP_epoch_100.pt')

plt.clf()
# flatten to 1d
plt.plot(out_arr[-15000:-1].view(-1).data.numpy(),'b',label='train_pred')
plt.plot(label_arr[-15000:-1].view(-1).data.numpy(),'r',label='train_true')
plt.legend(loc='best')
plt.savefig('train.jpg')

#x_tmp=test_x.reshape([-1,1428])
#print(x_tmp.shape)
#for i in range(3):
    #print("test start")
    #print(x_tmp[i])
test_x = test_x.cuda()
pred_test = model(x=test_x,s_mask=None)
pred_test = pred_test.cpu()

    #print(pred_test)

plt.clf()
plt.plot(pred_test.view(-1).data.numpy(),'b',label='test_pred')
plt.plot(test_y.view(-1).data.numpy(),'r',label='test_true')
plt.legend(loc='best')
plt.savefig('test.jpg')

print(test_close_min,test_close_scalar)

pd.DataFrame(pred_test.view(-1).detach().numpy()).to_csv("test_out.csv")
pd.DataFrame(test_y.view(-1).detach().numpy()).to_csv("test_target.csv")
pd.DataFrame(pred_test.view(-1).detach().numpy()*test_close_scalar+test_close_min).to_csv("test_out_norm.csv")
pd.DataFrame(test_y.view(-1).detach().numpy()*test_close_scalar+test_close_min).to_csv("test_target_norm.csv")