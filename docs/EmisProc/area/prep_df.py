import numpy as np
from pandas import *
from pypinyin import pinyin, lazy_pinyin
import subprocess
import json
from datetime import datetime, timedelta
#prepare the dataframe
def PrepDf(fname):
  path=''#'/home/sespub/teds10/08-時間分配權重/月週日時間權重/'
  df=read_csv(path+fname,encoding='big5')
  df.loc[df.NSC_SUB.map(lambda x: isna(x)),'NSC_SUB']='b'
  df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
  for i in range(len(df.REGION)):
    cha=df.loc[i,'REGION']
    if type(cha) in [int,float]:continue
    ll=lazy_pinyin(cha)
    if len(ll)==0:continue
    s=''
    for l in ll:
      s=s+l
    df.loc[i,'REGION']=s
  a=df.loc[df.DICT.map(lambda x:type(x)==str and '、' in x)]
  idx=a.index
  df=df.drop(idx).reset_index(drop=True)
  a=a.reset_index(drop=True)
  for i in range(len(a)):
    dct=a.loc[i,'DICT'].split('、')
    b=DataFrame({})
    for j in range(len(dct)):
      b=b.append(a.loc[i],ignore_index=True)
      b.loc[j,'DICT']=dct[j]
    df=df.append(b,ignore_index=True)
  idx=df.loc[df.REGION.map(lambda x:type(x)==float and np.isnan(x))].index
  df.loc[idx,'REGION']=['quanguo' for i in idx]
  for c in df.columns:
    if c in ['REGION','NSC','NSC_SUB','nsc2','DICT']:continue
    df[c]=[float(i) for i in list(df[c])]
#change 51b to 51A~51D, no need changing it manually
  snsc2=set(df.nsc2)
  if '51b' in snsc2:
    df51=df.loc[df.nsc2=='51b'].reset_index(drop=True)
    for s in 'ABCD':
      if '51A' not in snsc2:
        tmp=df51
        tmp.nsc2='51'+s
        df=df.append(tmp,ignore_index='True',sort=False)	
# taizhongjichang is missing, fill it according tainanjichang
  if 'taizhongjichang' not in set(df.REGION):
    a=df.loc[df.REGION=='tainanjichang'].reset_index(drop=True)
    a.DICT=3605
    a.REGION='taizhongjichang'
    df=df.append(a,ignore_index=True)
  df.drop_duplicates(inplace=True)
  df=df.reset_index(drop=True)
  return df
