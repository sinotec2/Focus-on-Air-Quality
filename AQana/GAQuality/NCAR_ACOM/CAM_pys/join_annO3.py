cd /nas1/CAM-chem/Annuals
!lst
!lst
df=DataFrame({})
for y in range(7,19):
    yr='{:02d}'.format(y)
    fname=yr+'IC.S.grd04T.nc.csv'
    dft=read_csv(fname,header=None)
    dft.columns=col
    dft['y']=int('20'+yr+'0101')
    df=df.append(dft,ignore_index=True)
len(df)
df.head()
df.tail
df.tail()
pwd
a=read_csv('y_s_v00.csv')
coef={i:j for i,j in zip(a.s,a.name)}
len(coef)
df['s']=df.cnt1*1000+df.cnt2
df['name']=[coef[i] for i in df.s]
i
type(i)
10018020 in coef
df.head()
df.tail()
len(set(df.s))
set(df.s)-set(a.s)
coef.update({10018010:'xinzhushineiqu'})
coef.update({10018020:'xinzhushibeiqu'})
df['name']=[coef[i] for i in df.s]
df.head()
df['v']=df.val
df['ymd']=df.y
col3='ymd,name,s,v'.split(',')
df[col3].set_index('ymd').to_csv('y_s_vO300.csv')

