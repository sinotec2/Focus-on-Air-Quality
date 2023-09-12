#kuang@master /home/backup/data/cwb/e-service/read_web
#$ cat town_cwb2.py

from pandas import *
import json
path='/home/QGIS/Data/TWN_town'
df_town=read_csv(path+'/TOWN_MOI_1090727E.csv',encoding='big5')
path2='/home/backup/data/cwb/e-service/read_web'
df_st=read_csv(path2+"/stats_dict.csv")
fname=path+'/adj_dict.json'
fn=open(fname,'r')
adj_dict=json.load(fn)
ddict=[str(i) for i in set(df_st['twnid'])]
df_cnty=df_town
df_cnty['aq_st']=''
for i in range(len(df_cnty)):
  dd=str(df_cnty.loc[i,'TOWNCODE'])
  if dd in ddict:
    stnos=list(df_st.loc[df_st['twnid']==int(dd),'stno'])
    if len(stnos)==0:sys.exit('fail')
    for s in stnos:
      if s not in df_cnty.loc[i,'aq_st']:df_cnty.loc[i,'aq_st']+=s+';'
for i in range(len(df_cnty)):
  dd=str(df_cnty.loc[i,'TOWNCODE'])
  if dd in adj_dict:
    for jj in adj_dict[dd.decode('utf-8')].split(';'):
      j=str(jj)
      if len(j)==0:continue
      if j in ddict:
        stnos=list(df_st.loc[df_st['twnid']==int(j),'stno'])
        if len(stnos)==0:sys.exit('fail')
        for s in stnos:
          if s not in df_cnty.loc[i,'aq_st']:df_cnty.loc[i,'aq_st']+=s+';'
  if len(df_cnty.loc[i,'aq_st'])==0:
    df_cnty.loc[i,'aq_st']='0'+';'

df_cnty=df_cnty.loc[df_cnty.aq_st.map(lambda x:x!='0;')].reset_index(drop=True)
df_cnty.set_index('TOWNCODE').to_csv(path2+'/town_cwb.csv')
