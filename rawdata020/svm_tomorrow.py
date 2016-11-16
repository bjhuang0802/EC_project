import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets, svm
from sklearn.metrics import roc_curve, auc
from sklearn.externals import joblib
import pickle
import timeit
import curdata
import time
import json

nday=5
nday_predict=4
rate=1.0
gamma='0.1'
fp = open('time_log.txt','a+')
fp1= open('general_log.txt','a+')

timew=['30-OCT-18']
x0=[]
y0=[]
f=[]
pattern = '%d-%b-%y'
kpredict = pd.read_csv('/home/ubuntu/2501/rawdata020/predict_keras.csv',dtype={'fid':str})
kscore=kpredict.set_index('fid')['score'].to_dict()
#rawdata = pd.read_csv('rawdata020/dataset'+timew[-1]+'.csv',dtype={'gid':str,'event':str,'productId':str})
clf=joblib.load('/home/ubuntu/2501/model/gamma'+gamma+'/svm_predict_rbfrate0.008-'+str(nday)+'.pkl')
rawdata = pd.read_csv('/home/ubuntu/2501/rawdata020/dataset.csv',dtype={'fid':str,'event':str,'cur_cam':str,'productId':str})
for i in range(0,len(timew)):
    epoch = int(time.mktime(time.strptime(timew[i],pattern)))
    xt=[]
    yt=[]
    ft=[]
    #print 'load data: %s' %(timew[i])
    selectdata=rawdata[rawdata.time < epoch].reset_index(drop=True)
    #x0,y0,f=curdata.load(rate,nday,nday_predict,timew[i])
    xt,yt,ft=curdata.load(selectdata,rate,nday,nday_predict,timew[i])
    #xt,yt,ft=curdata.load(selectdata,rate,nday,nday_predict,timew)
    x0=x0+xt
    y0=y0+yt

showid = True
fp=open("predict_current.csv","w")
y=np.array(y0)
x=np.array(x0)
FP=0
print >>fp, 'fid,member,AD_clicks,buys,Cart1,Cart2,Cart3,Cart4,Cart5,session1,session2,session3,session4,session5,T_pv1,T_pv2,T_pv3,T_pv4,T_pv5,buy_YN,SVC,Kscore'
xlen=len(x0[0])
idneg=np.where(y>0)[0].tolist()
for i in idneg:
    pre=clf.predict([x0[i][1:xlen]])[0]
    if pre >0.0:
        FP = FP +1
        if showid:
            print>>fp, '%-25s,' %(x0[i][0]),
        for j in range(1,4):
            print>>fp, '%2d,' %(int(x0[i][j])),
        for j in range(4,4+nday):
            print>>fp, '%5.1f,' %(float(x0[i][j])),
        for j in range(4+nday,4+2*nday):
            print>>fp, '%2d,' %(int(x0[i][j])),
        for j in range(4+2*nday,4+3*nday):
            print>>fp, '%5.1f,' %(float(x0[i][j])),
        print>>fp, '%2d,%2d,' %(y0[i],clf.predict([x0[i][1:xlen]])[0]),
        if kscore.has_key(x0[i][0]):
            print >>fp,'%5.2f' %(kscore[x0[i][0]])
        else:
            print >>fp,''

rawdata = pd.read_csv('/home/ubuntu/2501/rawdata020/predict_current.csv',dtype={'fid':str})
list1 = rawdata.to_json(orient='records')
with open('/home/ubuntu/2501/json/user.json','w') as outfile1:
    json.dump(list1,outfile1)

print  'user.json is generated.'
