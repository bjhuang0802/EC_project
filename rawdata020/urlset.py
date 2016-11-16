import pandas as pd
import urllib as ul
import os,time
import datetime
from datetime import timedelta
import json
os.environ['TZ'] = 'Asia/Taipei'
now = datetime.datetime.now()
day_before = now - timedelta(days=1)
data=pd.read_csv('/home/ubuntu/2501/rawdata020/input.csv',names=['fid','time','url','campaign','event'],dtype={'event':str,'campaign':str})
fp=open('/home/ubuntu/2501/rawdata020/user_url.csv','w')
fptrain=open('/home/ubuntu/2501/rawdata020/user_url_train.csv','w')
fpds=open('/home/ubuntu/2501/rawdata020/user_url_ds.csv','w')
fp1=open('/home/ubuntu/2501/rawdata020/urltable.csv','w')
print >>fp,'fid,time,url,campaign,event'
print >>fptrain,'fid,time,url,campaign,event'
print >>fpds,'fid,time,url,campaign,event'
for row in data.iterrows():
    c=datetime.datetime.fromtimestamp(row[1]['time'])
    print >>fp,'%s,%s,%s,%s,%s' %(row[1]['fid'],row[1]['time'],ul.unquote_plus(row[1]['url']),row[1]['campaign'],row[1]['event'])
    if c<day_before:
        print >>fptrain,'%s,%s,%s,%s,%s' %(row[1]['fid'],row[1]['time'],ul.unquote_plus(row[1]['url']),row[1]['campaign'],row[1]['event'])
    s=time.strftime("%Y%m%d/%H:%M:%S",time.localtime(row[1]['time']))
    ss=row[1]['campaign'].split('=')
    if len(ss)==4:
        print >>fpds,'%s,%s,%s,%s,%s' %(row[1]['fid'],s,ul.unquote_plus(row[1]['url']),ss[3],row[1]['event'])
    else:
        print >>fpds,'%s,%s,%s,%s,%s' %(row[1]['fid'],s,ul.unquote_plus(row[1]['url']),ss[0],row[1]['event'])

    #print >>fp,'%s,%s,%s,%s' %(row[1]['fid'],str(s),str(ul.unquote_plus(row[1]['url'])),str(row[1]['campaign']))

fpds.close()
userurl=pd.read_csv('/home/ubuntu/2501/rawdata020/user_url_ds.csv')
userurl=userurl[:20000]
list1= userurl.to_json(orient='records')
with open('/home/ubuntu/2501/json/userurl.json','w') as outfile1:
    json.dump(list1,outfile1)

as_table=data.groupby(['url','event'],as_index=False).count().sort_values(by=['fid']).values
print>>fp1,'sn,url'
print>>fp1,'%d,%s' %(1000,'Purchase')
tmp=[]
for row in as_table:
    if row[1]!='Purchase':
        tmp.append(row[1]+'-'+ul.unquote_plus(row[0]))

df=pd.DataFrame(tmp,columns=['url'])
df1=pd.Series(df['url']).unique()
i=1
for row in df1:
    print >>fp1, '%d,%s' %(i,row)
    i=i+1
