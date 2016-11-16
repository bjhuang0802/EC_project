#!/usr/bin/env python
# -*- coding: utf8 -*-
from flask import Flask, url_for, Response, json
import pandas as pd
import numpy as np
import json


def settime(rawdata,buydata):
    maxct=max(rawdata['time'])
    sstime={}
    ct={}
    secs_a_day  =86400
    uuid=pd.Series(rawdata['fid']).unique()
    for row in uuid:
        sstime[row]=0
        #ct[row]=maxct

    lt=[]
    for i in range(0,len(rawdata)-1):
        lt.append(0)
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
    return data,uuid,sstime

def setproduct(data,buydata):
    pv={}
    pbuy={}
    uuid=pd.Series(data['fid']).unique()
    for row in uuid:
        pv[str(row)]={}
        pbuy[str(row)]={}

    for row in data.iterrows():
        if row[1]['productid'] >0 and row[1]['dt']>0.0:
            if pv[row[1]['fid']].has_key(row[1]['productid']):
                 pv[row[1]['fid']][row[1]['productid']] += row[1]['dt']
            else:
                 pv[row[1]['fid']].update({row[1]['productid']:row[1]['dt']})

    for row in buydata.iterrows():
         if pbuy[row[1]['fid']].has_key(row[1]['productid']):
                subtotal = row[1]['quantity']*row[1]['price']
                pbuy[row[1]['fid']][row[1]['productid']]  = row[1]['productid']
         else:
                pbuy[row[1]['fid']].update({row[1]['productid']:row[1]['productid']})

    return pv,pbuy


def addtocart_pbuy(product,data,addtocart,buydata,AD):

    name=product.set_index('productid')['name'].to_dict()
    #----------------------------------------------
    df=data.groupby(['productid'],as_index=False)['dt'].sum()
    #df=df.sort(['dt']).reset_index(drop=True)
    #----------------------------------------------

    naddtocart=addtocart.groupby(['productid'],as_index=False)['fid'].count()
    addcount=naddtocart.set_index('productid')['fid'].to_dict()
    #---------------------------------
    df1=buydata.groupby(['productid'],as_index=False)['quantity'].sum()
    count=df1.set_index('productid')['quantity'].to_dict()

    output=[]
    for row in naddtocart.iterrows():
        idx=int(row[1]['productid']) 
        
        if AD.has_key(idx):
            if count.has_key(idx) and addcount.has_key(idx):
                xx={'x':addcount[idx],'y':count[idx],'name':name[idx],'AD':AD[idx]}
                output.append(xx)
        else:
            if count.has_key(idx) and addcount.has_key(idx):
                xx={'x':addcount[idx],'y':count[idx],'name':name[idx],'AD':0}
                output.append(xx)

    return output

def pv_addtocart(buydata,data,product,addtocart,pv,AD):

	name=product.set_index('productid')['name'].to_dict()
	#----------------------------------------------
	df=data.groupby(['productid'],as_index=False)['dt'].sum()
	#----------------------------------------------
	naddtocart=addtocart.groupby(['productid'],as_index=False)['fid'].count()
	addcount=naddtocart.set_index('productid')['fid'].to_dict()
	#---------------------------------
	output=[]
	for row in df.iterrows():
	    idx=int(row[1]['productid']) 
	    if addcount.has_key(idx):
	         
	        if row[1]['dt'] > 100000.0:
	            row[1]['dt'] =0.0
	    
	        if row[1]['dt'] >0 and addcount[idx]>-1:
                 if AD.has_key(idx):
    	            xx={'x':round(row[1]['dt'],2),'y':addcount[idx],'name':name[idx],'AD':AD[idx]}
    	            output.append(xx)
                 else:
                    xx={'x':round(row[1]['dt'],2),'y':addcount[idx],'name':name[idx],'AD':0}
                    output.append(xx)

	    else:
	        if row[1]['dt'] > 10000.0:
	            row[1]['dt'] =0.0

	return output

if __name__ == '__main__':
    buydata = pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/Purchased_list.csv',dtype={'fid':str})
    data =pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/dataset.csv',dtype={'fid':str})
    product = pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/2501_product_list.csv')
    addtocart = pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/add_to_cart_list.csv',dtype={'fid':str})
    campaign = pd.read_csv('/Users/abel/ML_ec/2501/rawdata020/uniq_campaign_target_product.txt')
    AD=campaign.set_index('productid')['counts'].to_dict()
    data,uuid,sstime = settime(data,buydata)
    pv,pbuy = setproduct(data,buydata)

    list1 = addtocart_pbuy(product,data,addtocart,buydata,AD)
    list2 = pv_addtocart(buydata,data,product,addtocart,pv,AD)
    js1 = json.dumps(list1,encoding="UTF-8",ensure_ascii=False)
    js2 = json.dumps(list2,encoding="UTF-8",ensure_ascii=False)
    with open('/Users/abel/ML_ec/2501/dashboard/addtocart_pbuy.json','w') as outfile1:
            json.dump(js1,outfile1)

    print 'addtocart_pbuy.json is generated.'
    with open('/Users/abel/ML_ec/2501/dashboard/pv_addtocart.json','w') as outfile2:
            json.dump(js2,outfile2)
    print 'pv_addtocart.json is generated.'

