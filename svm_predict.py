"""

========================================
SVM for product-buying prediction
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

nday=5
nday_predict=4
rate=0.008
gamma=0.1
fp = open('time_log.txt','a+')
fp1= open('general_log.txt','a+')

#timew=['14-AUG-16','18-AUG-16','22-AUG-16','24-AUG-16','27-AUG-16']
timew=['10-OCT-16','11-OCT-16','12-OCT-16','13-OCT-16','14-OCT-16','15-OCT-16','16-OCT-16','17-OCT-16','18-OCT-16','19-OCT-16','20-OCT-16','21-OCT-16','22-OCT-16','23-OCT-16','24-OCT-16','25-OCT-16','26-OCT-16']
x0=[]
y0=[]
f=[]
pattern = '%d-%b-%y'
#rawdata = pd.read_csv('rawdata020/dataset'+timew[-1]+'.csv',dtype={'gid':str,'event':str,'productId':str})
rawdata = pd.read_csv('/home/ubuntu/rawdata020/dataset020.csv',dtype={'fid':str,'event':str,'cur_cam':str,'productId':str})
for i in range(0,len(timew)):
    epoch = int(time.mktime(time.strptime(timew[i],pattern)))
    xt=[]
    yt=[]
    ft=[]
    print 'load data: %s' %(timew[i])
    selectdata=rawdata[rawdata.time < epoch].reset_index(drop=True)
    #x0,y0,f=mydata.load(rate,nday,nday_predict,timew[i])
    xt,yt,ft=mydata.load(selectdata,rate,nday,nday_predict,timew[i])
    #xt,yt,ft=mydata.load(selectdata,rate,nday,nday_predict,timew)
    x0=x0+xt
    y0=y0+yt

f=ft
fx_all= open('model/x0_all-'+str(nday)+'.pkl','wb')
fy_all= open('model/y0_all-'+str(nday)+'.pkl','wb')
fx_train= open('model/x0_train_rate'+str(rate)+'-'+str(nday)+'.pkl','wb')
fy_train= open('model/y0_train_rate'+str(rate)+'-'+str(nday)+'.pkl','wb')
fx_test= open('model/x0_test_rate'+str(rate)+'-'+str(nday)+'.pkl','wb')
fy_test= open('model/y0_test_rate'+str(rate)+'-'+str(nday)+'.pkl','wb')
print 'The predict-buy module using svm.'
print 'Use %d weeks train data to predect %d weeks buying members' %(nday,nday_predict)
print 'The gamma value of rbf kernel is %5.2f' %(gamma)
print 'Data is loaded. Use %d features for each uniq gid.' %(len(x0[0]))
print >>fp1,'The predict-buy module using svm.'
print >>fp1,'The gamma value of rbf kernel is %5.2f' %(gamma)
print >>fp1,'Use %d weeks train data to predect %d weeks buying members' %(nday,nday_predict)
print >>fp1,'Data is loaded. Use %d features for each uniq gid.' %(len(x0[0]))
for i in range(0,len(f)):
    print '%d. %s' %(i+1,f[i])
    print >>fp1,'%d. %s' %(i+1,f[i])
print ''
X=np.array(x0)
y=np.array(y0)
n_sample = len(X)
np.random.seed(0)
order = np.random.permutation(n_sample)
X = X[order]
y = y[order].astype(np.float)
s=int(9)
pickle.dump(X,fx_all)
pickle.dump(y,fy_all)
div=int(n_sample/10*s)
X_train0 = X[:div]
y_train = y[:div]
X_train=[]
xlen=len(X_train0[0])
for i in range(0,len(X_train0)):
   X_train.append(X_train0[i][1:xlen])

pickle.dump(X_train0,fx_train)
pickle.dump(y_train,fy_train)

TP_train = sum(y_train)-len(y_train)
TP_train_rate = TP_train*1.0/len(X_train)*100
X_test0 = X[div:]
y_test = y[div:]

xlen=len(X_test0[0])
X_test=[]
for i in range(0,len(X_test0)):
   X_test.append(X_test0[i][1:xlen])

pickle.dump(X_test0,fx_test)
pickle.dump(y_test,fy_test)

TP_test  = sum(y_test)-len(y_test)
TP_test_rate = TP_test*1.0/len(X_test)*100
print 'There are %d samples.' %(n_sample)
print 'Prepare train(%d percentage) and test(%d percentage) sample: %d/%d %6.2f percentage, %d/%d %6.2f percentage' %(s*10,(10-s)*10,TP_train,len(X_train),TP_train_rate,TP_test,len(X_test),TP_test_rate)
print >>fp1,'There are %d samples.' %(n_sample)
print >>fp1,'Prepare train(%d percentage) and test(%d percentage) sample: %d, %d' %(s*10,(10-s)*10,len(X_train),len(X_test))
# fit the model
#for fig_num, kernel in enumerate(('linear', 'rbf', 'poly')):
for fig_num, kernel in enumerate(('linear','rbf')):
    clf = svm.SVC(kernel=kernel, gamma=gamma,probability=True)
    probas_ = clf.fit(X_train, y_train).predict_proba(X_test)
    fpr, tpr, thresholds = roc_curve(y_test, probas_[:, 1],pos_label=2)
    roc_auc = auc(fpr, tpr)
    #plt.plot(fpr, tpr, lw=1, label='ROC (area = %0.2f)' % ( roc_auc))

    name=kernel
    #joblib.dump(clf, 'model/svm_predict_'+name+'rate'+str(rate)+'-'+str(nday)+'-'+timew+'.pkl') 
    joblib.dump(clf, 'model/gamma'+str(gamma)+'/svm_predict_'+name+'rate'+str(rate)+'-'+str(nday)+'.pkl') 
    strain =clf.score(X_train, y_train)
    stest  =clf.score(X_test,  y_test)


    print 'Kernel:%s, Accuracy(Train,Test):%6.2f,%6.2f, AUC:%6.2f' %(kernel,strain, stest,roc_auc)
    print >>fp, 'Train set:%s,%6.2f' %(kernel, strain)
    print >>fp1,'Kernel:%s, Accuracy(Train,Test):%6.2f,%6.2f, AUC:%6.2f' %(kernel,strain, stest,roc_auc)
    #plt.xlim([-0.05, 1.05])
    #plt.ylim([-0.05, 1.05])
    #plt.xlabel('False Positive Rate')
    #plt.ylabel('True Positive Rate')
    #plt.title('Receiver operating characteristic example '+kernel)
    #plt.legend(loc="lower right")
    #plt.show()

stop = timeit.default_timer()
ds = stop -start
dm = ds/60.0
print ''
print '%d samples, time cost: %8.2f (mins)/ %8d (sec)' %(n_sample,dm,ds)
print >>fp,'%d,%8d,%8.2f' %(n_sample,ds,dm)
print >>fp1,'%d samples, time cost: %8.2f (mins)/ %8d (sec)' %(n_sample,dm,ds)
print >>fp1, '-----------------'
