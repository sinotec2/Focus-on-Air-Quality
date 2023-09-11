#kuang@master /nas1/TEDS/teds10_camx/HourlyWeighted/area
#$ cat town_aqst.py
from pandas import *
import json
df_town=read_csv('town2.csv')
df_st=read_csv("sta_dict.csv")
fname='adj_dict.json'
fn=open(fname,'r')
adj_dict=json.load(fn)
ddict=set(df_st['dict'])
df_cnty=df_town
df_cnty['aq_st']=['' for i in xrange(len(df_cnty))]
for i in xrange(len(df_cnty)):
    dd=df_cnty.loc[i,'Name']
    if dd in ddict:
        s=str(list(df_st.loc[df_st['dict']==dd,'idx'])[0])+';'
        df_cnty.loc[i,'aq_st']=s
    else:
        for jj in adj_dict[dd]:
            if jj in ddict:
                s=str(list(df_st.loc[df_st['dict']==jj,'idx'])[0])+';'
                if len(df_cnty.loc[i,'aq_st'])==0:
                    df_cnty.loc[i,'aq_st']=s
                else:
                    df_cnty.loc[i,'aq_st']=df_cnty.loc[i,'aq_st']+s
    if len(df_cnty.loc[i,'aq_st'])==0:
         df_cnty.loc[i,'aq_st']='0'+';'
df_cnty.head(5)
df_cnty.tail(5)
df_cnty
df_cnty.set_index('code').to_csv('town_aqst.csv')
