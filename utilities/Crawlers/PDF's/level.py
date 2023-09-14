from pandas import *
import sys

chnum=['一','二','三','四','五','六','七','八','九','十',]
fnames=[
#"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1020271A) 大潭電廠增建燃氣複循環機組發電計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070401A) 興達電廠燃氣機組更新改建計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070721A) 森霸電力第二期燃氣複循環發電計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070731A) 台中發電廠新建燃氣機組計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1101051A) 中佳燃氣複循環電廠興建計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1110461A) 大林發電廠燃氣機組更新改建計畫環境影響說明書\C07.pdf",
]
fname=fnames[int(sys.argv[1])]
fname=fname.replace('.pdf','outlineR.txt')
with open(fname,'r', encoding='utf-8') as f:
    lines=[l.strip().replace('\n','') for l in f]
df=DataFrame({'tit':lines,'lev':0})
df['id']=df.index
df.loc[df.tit.map(lambda x:x.count('.')==2 and x[0].isdigit() and x[2].isdigit() and x[4].isdigit()),'lev']=2
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[2].isdigit() and x[1]=='.')),'lev']=1
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[0] in chnum)),'lev']=3
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[1] in chnum)),'lev']=4
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[0].isdigit())),'lev']=5
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[1].isdigit() and x[0]=='(' and x[2]==')')),'lev']=6
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[0].isupper())),'lev']=7
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[1].isupper() and x[0]=='(' and x[2]==')')),'lev']=8
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[0].islower())),'lev']=9
df.loc[(df.lev==0)&(df.tit.map(lambda x:x[1].islower() and x[0]=='(' and x[2]==')')),'lev']=10
df['parent_id'] = None
mnlev,mxlev=df.lev.min(),df.lev.max()
for l in range(mnlev,mxlev):
    a=df.loc[df.lev==l]
    n=len(a)
    if n==0:continue
    ai=list(a.index)
    aj=ai[1:]+[len(df)]
    b=df.loc[(df.lev>l) & (df.parent_id.isnull())] 
    for i in range(n):
        boo=(b.index>ai[i]) & (b.index<aj[i] )
        c=b.loc[boo]
        mn=c.lev.min()
        df.loc[c.loc[c.lev==mn].index,'parent_id']=ai[i]
fname=fname.replace('outlineR.txt','.csv')
df.set_index('id').to_csv(fname)        