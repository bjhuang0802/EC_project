#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
import sklearn
from sklearn.externals import joblib
import numpy as np
import matplotlib.pyplot as plt

weeks=5
nw_pred=4
rate=0.008
gamma='0.1'
#timew='26-JUN-16'
showid = True
clf=joblib.load('model/gamma'+gamma+'/svm_predict_rbfrate'+str(rate)+'-'+str(weeks)+'.pkl')
x0=pickle.load(open('model/x0_all-'+str(weeks)+'.pkl'))
y0=pickle.load(open('model/y0_all-'+str(weeks)+'.pkl'))

y=np.array(y0)
x=np.array(x0)
FP=0
xlen=len(x0[0])
idneg=np.where(y>0)[0].tolist()
for i in idneg:
    pre=clf.predict([x0[i][1:xlen]])[0]
    if pre >0.0:
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
            print '%2d, %2d' %(y0[i],clf.predict([x0[i][1:xlen]])[0])
# print '------------------------'
# print 'All set'
# nfe=len(xpos[0][0])
# nsample=len(xpos)
# xavg=[]
# for x in range(0,nfe):
#        xavg.append(0)
# for i in range(0,nsample):
#      for x in range(0,nfe):
#          xavg[x] += float(xpos[i][0].tolist()[x])*1.0

# #for x in range(0,nfe):
# #     print '%-20s,%5.1f' %(features[x],xavg[x]/(1.0*nsample))

