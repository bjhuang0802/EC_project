import pandas as pd
import numpy as np

def load_Purchase(flag):

    urlmap=pd.read_csv("/home/ubuntu/2501/rawdata020/urltable.csv")
    if flag == 'predict':
        data=pd.read_csv('/home/ubuntu/2501/rawdata020/user_url.csv')
    else:
        data=pd.read_csv('/home/ubuntu/2501/rawdata020/user_url_train.csv')

    url2int=urlmap.set_index('url')['sn'].to_dict()
    uuid=data.groupby('fid',as_index=False)['time'].count()['fid'].tolist()
    seq=[]
    y=[]
    tmp=[]
    sn = -1
    oldfid='s0'
    secs_of_session=1800
    for row in data.iterrows():
        if row[1]['event'] != 'Purchase':
            ckey=row[1]['event']+'-'+row[1]['url']
        else:
            ckey='Purchase'

        if row[1]['fid'] == oldfid:
            if row[1]['time'] - oldtime < secs_of_session:
                oldtime=row[1]['time']

                #---------------------------
                if 'Purchase' in ckey:
                    #print  row[1]['url']
                    y[sn]=1
                #---------------------------
                if y[sn]<1:
                    if url2int.has_key(ckey):
                        #seq[sn].append(url2int[ckey])
                        tmp.append(url2int[ckey])
                    else:
                        #seq[sn].append(0)
                        tmp.append(0)

            else:
                # if y[sn]!=1:
                seq[sn]=seq[sn]+tmp

                tmp=[]
                #y.append(0)
                #seq.append([])
                tmp.append(0)
                tmp.append(0) 
                tmp.append(0)
                #sn = sn + 1

                if 'Purchase' in ckey:
                    y[sn]=1

                oldtime=row[1]['time']
                if y[sn]<1:
                    if url2int.has_key(ckey):
                        #seq[sn].append(url2int[ckey])
                        tmp.append(url2int[ckey])
                    else:
                        #seq[sn].append(0)
                        tmp.append(0)
        else:
            if row[0]>0 and sn>0:
                seq[sn]=seq[sn]+tmp

            seq.append([])
            tmp=[]

            y.append(0)
            sn = sn + 1
            seq[sn].append(row[1]['fid'])
            oldfid=row[1]['fid']
            oldtime=row[1]['time']

            #---------------------------
            if 'Purchase' in ckey:
                y[sn]=1

            if y[sn]<1:
                if url2int.has_key(ckey):
                    #seq[sn].append(url2int[ckey])
                    tmp.append(url2int[ckey])
                else:
                    #seq[sn].append(0)
                    tmp.append(0)

    seq=np.array(seq)
    y=np.array(y)
    n_sample =  len(seq)
    order = np.random.permutation(n_sample)
    seq=seq[order]
    y=y[order]
    div=int(n_sample/10*8)
    X_train=seq[:div]
    y_train=y[:div]
    X_test=seq[div:]
    y_test=y[div:]
    # for i in range(len(X_train)):
    #     if y[i]>0:
    #         print X_train[i]
    if flag == 'train':
        return  (X_train,y_train),(X_test,y_test)
    else:
        return (seq, y)


def load_ADpredict():
    urlmap=pd.read_csv("/home/ubuntu/2501/rawdata020/urltable.csv")
    data=pd.read_csv('/home/ubuntu/2501/rawdata020/user_url.csv',dtype={'campaign':str})

    url2int=urlmap.set_index('url')['sn'].to_dict()
    uuid=data.groupby('fid',as_index=False)['time'].count()['fid'].tolist()
    seq=[]
    y=[]
    y0=[] #AD +1
    y1=[] #Purchasae +2
    sn = -1
    oldfid='s0'
    secs_of_session=1800
    for row in data.iterrows():
        if row[1]['event'] != 'Purchase':
            ckey=row[1]['event']+'-'+row[1]['url']
        else:
            ckey='Purchase'
        #print row[1]['event'],row[1]['fid']

        if row[1]['fid'] == oldfid:
            if row[1]['time'] - oldtime < secs_of_session:
                oldtime=row[1]['time']
                #---------------------------
                if 'utm' in row[1]['campaign']:
                    y0[sn]=1
                if 'Purchase' in ckey:
                    y1[sn]=2
                #---------------------------
                if url2int.has_key(ckey):
                    seq[sn].append(url2int[ckey])
                else:
                    seq[sn].append(0)
            else:
                #y.append(0)
                seq[sn].append(0)
                seq[sn].append(0) 
                seq[sn].append(0)
                ##The gap between sessions is 000
                #sn = sn + 1
                #---------------------------
                if 'utm' in row[1]['campaign']:
                    y0[sn]=1
                if 'Purchase' in ckey:
                    y1[sn]=2
                #---------------------------
                oldtime=row[1]['time']
                if url2int.has_key(ckey):
                    #print sn,ckey, url2int[ckey]
                    seq[sn].append(url2int[ckey])
                else:
                    seq[sn].append(0)
        else:
            seq.append([])
            y0.append(0)
            y1.append(0)
            sn = sn + 1
            seq[sn].append(row[1]['fid'])
            #print '------',sn,ckey
            #---------------------------
            if 'utm' in row[1]['campaign']:
                y0[sn]=1
            if 'Purchase' in ckey:
                y1[sn]=2
            #---------------------------
            oldfid=row[1]['fid']
            oldtime=row[1]['time']
            if url2int.has_key(ckey):
                #print '------',sn,ckey, url2int[ckey]
                seq[sn].append(url2int[ckey])
            else:
                seq[sn].append(0)
    y0=np.array(y0)
    y1=np.array(y1)
    seq=np.array(seq)
    y=np.add(y0,y1)
    n_sample =  len(seq)
    order = np.random.permutation(n_sample)
    seq=seq[order]
    y=y[order]
    div=int(n_sample/10*8)
    X_train=seq[:div]
    y_train=y[:div]
    X_test=seq[div:]
    y_test=y[div:]
    print 'Size of data:'
    print 'X_train,y_train,X_test,y_test:%d,%d,%d,%d' %(len(X_train),len(y_train),len(X_test),len(y_test))
    return  (X_train,y_train),(X_test,y_test)
