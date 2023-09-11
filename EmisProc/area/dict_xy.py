from pandas import *
import numpy as np
from pypinyin import pinyin, lazy_pinyin
fname='areagrid.csv'
df = read_csv(fname)
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300
df['DICT']=[int(i) for i in list(df['DICT'])]
df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
subX=['44','50','51']
df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']=[x-201500 for x in df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']]
df['YX']=[int(y)+int(x/1000) for x,y in zip(df['UTME'],df['UTMN'])]

df_cnty=read_csv('town3.csv')
d_cnty={x:y for x,y in zip(df_cnty['code'],df_cnty['Name'])}
d_cnty.update({5300:'sea'})

df['YXCO']=[str(x)+str(y) for x,y in zip(df['YX'],df['DICT'])]
s_xy=list(set(df['YXCO']))
co=[int(x[7:]) for x in s_xy]
yx=[int(x[:7]) for x in s_xy]
x=[i%1000*1000 for i in yx]
y=[int(i/1000)*1000 for i in yx]
df=DataFrame({'x':x,'xx':x,'y':y,'dict':co})
df.loc[df['xx']>400000,'x']=df.loc[df['xx']>400000,'x']-1000000
df.loc[df['xx']>400000,'y']=df.loc[df['xx']>400000,'y']-df.loc[df['xx']>400000,'x']
del df['xx']
df['name']=[d_cnty[i] for i in df['dict']]
df.set_index('dict').to_csv('dict_xy.csv')

