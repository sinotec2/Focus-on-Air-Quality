#kuang@master /nas1/TEDS/teds10_camx/HourlyWeighted/area/adj_dict.py
import json
from pandas import *

fname='dict_xy.csv'
df=read_csv(fname)
ddict=set(df['name'])
adj_dict={}
for c in set(ddict):
    adj_c=set()
    a=df[df['name']==c].reset_index()
    xm=max(list(a['x']))+1000
    ym=max(list(a['y']))+1000
    xn=min(list(a['x']))-1000
    yn=min(list(a['x']))-1000
    boo=(df['x']<=xm) & (df['y']<=ym) & (df['x']>=xn) & (df['y']>=yn)
    b=df[boo]
    for i in xrange(len(a)):
        x=a.loc[i,'x']
        y=a.loc[i,'y']
        for ix in [x-1000,x,x+1000]:
            for iy in [y-1000,y,y+1000]:
                boo=(b['x']==ix) & (b['y']==iy)
                if len(b[boo])==0:continue
                c_add=list(b[boo]['name'])[0]
                if c_add==c:continue
                adj_c.add(c_add)
    adj_c=list(adj_c)
    adj_dict.update({c:adj_c})
adj_dict.update({'xinzhushineiqu':['xinzhushibeiqu','xinzhushidongqu','xinzhushixiqu']})
adj_dict.update({'tainanshizhongqu':['tainanshidongqu','tainanshinanqu','tainanshixiqu','tainanshibeiqu']})
adj_dict.update({'jiayishizhongqu':['jiayishidongqu','jiayishixiqu']})
adj_dict.update({'xinzhuxianxiangshanqu':['xinzhushibeiqu','xinzhushidongqu','xinzhuxianbaoshanxiang','sea','miaolixianzhunanzhen','miaolixiantoufenzhen']})
fname='adj_dict.json'
fn=open(fname,'w')
json.dump(adj_dict,fn)
