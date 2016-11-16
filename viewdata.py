#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import sklearn
from sklearn.externals import joblib
import numpy as np
import matplotlib.pyplot as plt

weeks=2
nw_pred=4
rate=0.01
gamma='0.1'
#timew='26-JUN-16'
showid = True
#=======================
# Figure
#=======================
#fig = plt.figure()
#ax = fig.add_subplot(1,1,1)
#width = 0.35
#ind = np.arange(weeks)
#ax.set_ylable('Staying time on etungo (in mins)')
#ax.set_xlim(-width,len(ind)+width)
#ax.set_set_xticks(ind+0.5*width)
#uid=2
#plt.plot([str(i) for i in range(1,weeks)],x0[uid][1:weeks],marker='o',linestyle='--',color='r',label='Square')
#plt.show()
#========================
features=['會員','廣告點擊','曾購買產品','願望清單1st','願望清單2nd','願望清單3rd','願望清單4th','sessions_1st','sessions_2nd','sessions_3rd','sessions_4th','time_1st','time_2nd','time_3rd','time_4th']
#clf=joblib.load('model/svm_predict_rbfrate'+str(rate)+'-'+str(weeks)+'-'+timew+'.pkl')
#x0=pickle.load(open('x0_train_rate'+str(rate)+'-'+str(weeks)+'-'+timew+'.pkl'))
#y0=pickle.load(open('y0_train_rate'+str(rate)+'-'+str(weeks)+'-'+timew+'.pkl'))
#clf=joblib.load('model/gamma'+gamma+'/svm_predict_rbfrate'+str(rate)+'-'+str(weeks)+'.pkl')
x0=pickle.load(open('x0_train_rate'+str(rate)+'-'+str(weeks)+'.pkl'))
y0=pickle.load(open('y0_train_rate'+str(rate)+'-'+str(weeks)+'.pkl'))

y=np.array(y0)
x=np.array(x0)
FP=0
xlen=len(x0[0])
idneg=np.where(y<2)[0].tolist()
for i in idneg:
    #pre=clf.predict([x0[i][1:xlen]])[0]
    pre=5
    if pre >1.0:
        FP = FP +1
        if showid:
            print '%-25s,' %(x0[i][0]),
        for j in range(1,4):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4,4+weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+weeks,4+2*weeks):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4+2*weeks,4+3*weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+3*weeks,4+3*weeks+1):
            print '%2d, %2d' %(y0[i],pre)
print 'Among '+str(len(idneg))+' negative data, there are '+str(FP)+' false positive' 
   
idy=np.where(y>1)[0].tolist()
FN=0
xlen=len(x0[0])
xpos=[]
for i in idy:
    xpos.append([x0[i][1:xlen]])
    #pre=clf.predict([x0[i][1:xlen]])[0]
    pre=-1
    if pre < 2.0:
        FN = FN +1
        if showid:
            print '%-25s,' %(x0[i][0]),
        for j in range(1,4):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4,4+weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+weeks,4+2*weeks):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4+2*weeks,4+3*weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+3*weeks,4+3*weeks+1):
            print '%2d, %2d' %(y0[i],pre)
print '------------------------'
xlen=len(x0[0])
TP=0
for i in idy:
    #pre=clf.predict([x0[i][1:xlen]])[0]
    pre=5
    if pre > 1.0:
        TP = TP + 1
        if showid:
            print '%-25s,' %(x0[i][0]),
        for j in range(1,4):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4,4+weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+weeks,4+2*weeks):
            print '%2d,' %(int(x0[i][j])),
        print '|',
        for j in range(4+2*weeks,4+3*weeks):
            print '%5.1f,' %(float(x0[i][j])),
        print '|',
        for j in range(4+3*weeks,4+3*weeks+1):
            print '%2d, %2d' %(y0[i],pre)
print '------------------------'
print 'Train set'
print 'False Negative: True Positive = %2d : %2d' %(FN,TP)
print 'Dataset use %d weeks to predict %d weeks buying customers' %(weeks,nw_pred)
nfe=len(xpos[0][0])
nsample=len(xpos)
xavg=[]
for x in range(0,nfe):
       xavg.append(0)
for i in range(0,nsample):
     for x in range(0,nfe):
         xavg[x] += float(xpos[i][0].tolist()[x])*1.0

for x in range(0,nfe):
     print '%-20s,%5.1f' %(features[x],xavg[x]/(1.0*nsample))

