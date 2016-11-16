"""

========================================
Generate Full user profile
========================================

"""
print(__doc__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
import pickle
import timeit
import mydata
import time

start = timeit.default_timer()

nw=10
nw_predict=4
rate=1.0
fp = open('time_log.txt','a+')

timew=['14-AUG-16','18-AUG-16','22-AUG-16','24-AUG-16','27-AUG-16']
#timew=['29-MAY-16']
x0=[]
y0=[]
f=[]
pattern = '%d-%b-%y'
#rawdata = pd.read_csv('dataset'+timew+'.csv',dtype={'clientId':str,'event':str,'productId':str})
rawdata = pd.read_csv('rawdata/dataset'+timew[-1]+'.csv',dtype={'clientId':str,'event':str,'productId':str})
for i in range(0,len(timew)):
    epoch = int(time.mktime(time.strptime(timew[i],pattern)))
    xt=[]
    yt=[]
    ft=[]
    print 'load data: %s' %(timew[i])
    selectdata=rawdata[rawdata.time < epoch].reset_index(drop=True)
    #x0,y0,f=mydata.load(rate,nw,nw_predict,timew[i])
    xt,yt,ft=mydata.load(selectdata,rate,nw,nw_predict,timew[i])
    x0=x0+xt
    y0=y0+yt

f=ft
#fx_train= open('x0_train_rate'+str(rate)+'-'+str(nw)+'-'+timew+'.pkl','wb')
#fy_train= open('y0_train_rate'+str(rate)+'-'+str(nw)+'-'+timew+'.pkl','wb')
#fx_test= open('x0_test_rate'+str(rate)+'-'+str(nw)+'-'+timew+'.pkl','wb')
#fy_test= open('y0_test_rate'+str(rate)+'-'+str(nw)+'-'+timew+'.pkl','wb')
fx_train= open('x0_all_user.pkl','wb')
fy_train= open('y0_all_user.pkl','wb')
print 'The predict-buy module using svm.'
print 'Use %d weeks train data to predect %d weeks buying members' %(nw,nw_predict)
print 'Data is loaded. Use %d features for each uniq clientId.' %(len(x0[0]))
print ''
X=np.array(x0)
y=np.array(y0)
n_sample = len(X)
np.random.seed(0)
order = np.random.permutation(n_sample)
X = X[order]
y = y[order].astype(np.float)
div=int(n_sample)
X_train0 = X[:div]
y_train = y[:div]
X_train=[]
xlen=len(X_train0[0])
for i in range(0,len(X_train0)):
   X_train.append(X_train0[i][1:xlen])

pickle.dump(X_train0,fx_train)
pickle.dump(y_train,fy_train)

