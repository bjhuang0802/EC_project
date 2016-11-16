#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
import random
import numpy as np
import pandas as pd
import time
#def loadpv(rawdata,ct,nw_x):
#    data,uuid,sstime = settime(rawdata)
#    secs_a_week=604800
#    pv={}   
#    for row in uuid:
#        pv[str(row)]={}
#
#    for row in data.iterrows():
#        if row[1]['productId'] >0 and row[1]['dt']>0.0:
#            if ct - nw_x*secs_a_week<row[1]['time'] and row[1]['time']<ct:
#                if pv[row[1]['fid']].has_key(row[1]['productId']):
#                    pv[row[1]['fid']][row[1]['productId']] += row[1]['dt']
#                else:
#                    pv[row[1]['fid']].update({row[1]['productId']:row[1]['dt']}) 
#
#    for row in pv:
#        if len(pv[row])>0:
#            print '%s,%s,%s' %(row,len(pv[row]),pv[row])


def load(rawdata,rate,nw_x,nw_y,timew):
    ufeat=[]
    y=[]
    invufeat={}
    #buydata = pd.read_csv('Purchased_list.csv',dtype={'fid':str})
    maxct=max(rawdata['time'])
    data,uuid,sstime,purT = settime(rawdata,maxct)
    
    #raw1 = csv.reader(open('session_sort'+timew+'.csv'))
    raw1 = csv.reader(open('/home/ubuntu/2501/rawdata020/session_sort.csv'))
    features=['Member','no. ADs','buy items'+str(nw_x)+'-weeks','no.sessions-'+str(nw_x)+'-weeks','session time-'+str(nw_x)+'-weeks']
    nfeatures=5+3*nw_x
    i=0
    # Initial data set array, set dictionary for fid (invufeat['fid']=sn)
    # ufeat[x][0] define fid
    snfeature=0
    for row in uuid:
        ufeat.append([str(row)])
        invufeat[str(row)]=int(i)
        for x in range(1,nfeatures):
            ufeat[i].append(0)
        ufeat[i].append(1)
        i +=1

    # No. of sessions as a function of week from now
    ssid=[]
    sst=[]
    ssdt=[]
    pattern = '%d-%b-%y'
    epoch = int(time.mktime(time.strptime(timew,pattern)))
    for row in raw1:
        if int(row[1]) < epoch:
            ssid.append(str(row[0]))
            sst.append(int(row[1]))
            ds=(int(row[2])-int(row[1]))*1.0/60.0
            ssdt.append(int(row[3]))

    secs_a_week=604800
    secs_a_day=86400
    secs_a_hour=3600
    secs_2_day=172800
    #July 1
    #secs_a_week=60*60*24*7
    # Member or not? ufeat[x][1]
    #for row in buydata.iterrows():
    #    idx=invufeat[row[1]['fid']]
    #    for j in range(0,nw_x):
    #        if (ct - secs_a_week*(j+1))<row[1]['time'] and (row[1]['time']< ct - secs_a_week*j):
    #                ufeat[idx][4+j] += row[1]['price']        
    for row in data.iterrows():
        idx=invufeat[row[1]['fid']]
        
        if row[1]['member'] == 1:
            ufeat[idx][1]=1
        #if row[1]['cur_cam'] != '0' and (row[1]['time'] > purT[row[1]['fid']]-5*secs_a_day) and (row[1]['time'] < purT[row[1]['fid']]):
        #if row[1]['cur_cam'] != '0' and (row[1]['time'] > purT[row[1]['fid']]-secs_a_week) and (row[1]['time'] < purT[row[1]['fid']]):
        if row[1]['cur_cam'] != '0' and (row[1]['time'] < purT[row[1]['fid']]):
            ufeat[idx][2] +=1
        if row[1]['purchase'] == 2 and (row[1]['time'] < purT[row[1]['fid']]):
            ufeat[idx][3] += 1
        #if row[1]['purchase'] == 2 and (row[1]['time'] >purT[row[1]['fid']]-60) and (row[1]['time'] < purT[row[1]['fid']]+10): 
        if row[1]['purchase'] == 2 and (row[1]['time'] > maxct): 
            ufeat[idx][nfeatures]= 2
        for j in range(0,nw_x):
            if (purT[row[1]['fid']] - secs_2_day*(j+1)-secs_a_hour)<row[1]['time'] and (row[1]['time']< purT[row[1]['fid']] - secs_2_day*j-secs_a_hour):
                 #if row[1]['Final'] == 2:
                 #      ufeat[x][3+j] += 1   
                 #if row[1]['productId'] >0 and row[1]['event'] == 'Product': 
                 #if row[1]['event'] == 'Product': 
                       #ufeat[idx][3+j] += 1   
                 if row[1]['event'] == 'AddToCart': 
                       ufeat[idx][4+j] += 1   
                 if row[1]['event'] == 'AddToWishlist': 
                       ufeat[idx][4+j] += 1   

    snfeat=4+nw_x

    for i in range(len(ssid)):
        for j in range(0,nw_x):
            if (purT[row[1]['fid']] - secs_2_day*(j+1))<sst[i] and (sst[i]< purT[row[1]['fid']] - secs_2_day*j):
                idx=invufeat[ssid[i]]
                ufeat[idx][snfeat+j] += 1
                ufeat[idx][snfeat+nw_x+j] += ssdt[i]


    #0(string).uid, 1(int).member 0/1, 2(int).session, 3(float). tstime, 
    #4(int). ADs, 5(int). no. product-view, 6(float). maximum time of a product view 
    train_y=[]
    train_x=[]

    for i in range(0,len(ufeat)):
        tss=sum(ufeat[i][4+nw_x:4+2*nw_x])
        if tss >0:
            if ufeat[i][nfeatures] == 2:
                train_x.append(ufeat[i][0:nfeatures-1])
                train_y.append(ufeat[i][nfeatures])
            else:
                 if random.random() <rate:
                    train_x.append(ufeat[i][0:nfeatures-1])
                    train_y.append(ufeat[i][nfeatures])

    return train_x,train_y,features

def settime(rawdata,maxct):
 
    sstime={}
    ct={}
    uuid=pd.Series(rawdata['fid']).unique()
    for row in uuid:
        sstime[row]=0
        ct[row]=maxct

    lt=[]
    for i in range(0,len(rawdata)-1):
        lt.append(0)
        #if rawdata['purchase'][i] == 2:
        #    ct[rawdata['fid'][i]]=rawdata['time'][i]
            
        if rawdata['fid'][i+1] == rawdata['fid'][i]:
            time=rawdata['time'][i+1]-rawdata['time'][i]
            time = time * 1.0/60.0
            if time < 30.0:
                lt[i]=time
                sstime[rawdata['fid'][i]]=sstime[rawdata['fid'][i]] +time
 
            else:
                lt[i]=0            
        else:
            lt[i]==0
 
    lt.append(0)
    datalt=pd.DataFrame(lt,columns=['dt'])
    data=pd.concat([rawdata,datalt],axis=1)

    return data,uuid,sstime,ct
