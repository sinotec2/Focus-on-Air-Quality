from pandas import *
df=read_csv('ymd_s_v08.csv')
dfa=df.loc[df.ymd==20080101]
s_n={i:j for i,j in zip(dfa.s,dfa.name)}
for fname in ['ymd_s_v0'+str(i)+'.csv' for i in range(7,10)]+['ymd_s_v'+str(i)+'.csv' for i in range(10,19)]:
    df=read_csv(fname)
    dfv=pivot_table(df,index='s',values='v',aggfunc=np.mean).reset_index()
    dfv['name']=[s_n[i] for i in dfv.s]
    dfv.set_index('name').to_csv(fname.replace('ymd','y'))

dfy=DataFrame({})
for fname in ['y_s_v0'+str(i)+'.csv' for i in range(7,10)]+['y_s_v'+str(i)+'.csv' for i in range(10,19)]:
    df=read_csv(fname)
    df['ymd']=[int('20'+fname[5:7]+'0101') for i in range(len(df))]
    del df['y']
    dfy=dfy.append(df,ignore_index=True)
dfy.set_index('ymd').to_csv('y_s_v00.csv')

