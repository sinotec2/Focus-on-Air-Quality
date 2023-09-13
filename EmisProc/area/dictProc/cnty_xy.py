from pandas import *
import numpy as np
from pypinyin import pinyin, lazy_pinyin
fname='areagrid.csv'
df = read_csv(fname)
df.loc[df['NSC_SUB'].map(lambda x: type(x)==float and np.isnan(x)==True),'NSC_SUB']='b'
df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
subX=['44','50','51']
df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']=[x-201500 for x in df.loc[df['CNTY'].map(lambda x: x in subX),'UTME']]
df['YX']=[int(y)+int(x/1000) for x,y in zip(df['UTME'],df['UTMN'])]

df_cnty=read_csv('cnty.csv')
for i in xrange(len(df_cnty)):
    cha=df_cnty.loc[i,'cnty']
    ll=lazy_pinyin(cha.decode('big5'))
    s=''
    for l in ll:
        s=s+l
    df_cnty.loc[i,'cnty']=s
df_cnty.loc[24,'no']=51
df_cnty.loc[24,'cnty']='lianjiangxian'
d_cnty={x:str(int(y)) for x,y in zip(df_cnty['cnty'],df_cnty['no'])}
d_cnty.update({'xinbeishi':'41','taoyuanshi':'32'})
d_cnty.update({'sea':'53'})

df['YXCO']=[str(x)+str(y) for x,y in zip(df['YX'],df['CNTY'])]
s_xy=list(set(df['YXCO']))
co=[int(x[7:]) for x in s_xy]
yx=[int(x[:7]) for x in s_xy]
x=[i%1000*1000 for i in yx]
y=[int(i/1000)*1000 for i in yx]
df_xyc=DataFrame({'x':x,'xx':x,'y':y,'cnty':co})
df.loc[df['xx']>400000,'x']=df.loc[df['xx']>400000,'x']-1000000
df.loc[df['xx']>400000,'y']=df.loc[df['xx']>400000,'y']-df.loc[df['xx']>400000,'x']
del df['xx']
d2_cnty={x:y for x,y in zip(d_cnty.values(), d_cnty.keys())}
df_xyc['name']=[d2_cnty[str(i)] for i in df_xyc['cnty']]
df_xyc.set_index('cnty').to_csv('cnty_xy.csv')

