
from pandas import *
import json
path='/nas1/TEDS/teds10_camx/HourlyWeighted/area'
df_town=read_csv(path+'/town3.csv',encoding='big5')
df_st=read_csv("stats_dict.csv")
fname=path+'/adj_dict.json'
fn=open(fname,'r')
adj_dict=json.load(fn)
ddict=set(df_st['name'])
df_cnty=df_town
df_cnty['aq_st']=''
for i in range(len(df_cnty)):
    dd=df_cnty.loc[i,'Name']
    if dd in ddict:
        s=str(list(df_st.loc[df_st['name']==dd,'stno'])[0])+';'
        df_cnty.loc[i,'aq_st']=s
    else:
        for jj in adj_dict[dd]:
            if jj in ddict:
                s=str(list(df_st.loc[df_st['name']==jj,'stno'])[0])+';'
                if len(df_cnty.loc[i,'aq_st'])==0:
                    df_cnty.loc[i,'aq_st']=s
                else:
                    df_cnty.loc[i,'aq_st']=df_cnty.loc[i,'aq_st']+s
    if len(df_cnty.loc[i,'aq_st'])==0:
         df_cnty.loc[i,'aq_st']='0'+';'
df_cnty=df_cnty.loc[df_cnty.aq_st.map(lambda x:x!='0;')].reset_index(drop=True)
df_cnty.set_index('code').to_csv('town_cwb.csv')
