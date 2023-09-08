#kuang@node03 /nas1/camxruns/2016_v7/outputs/Annual
#$ cat -n By_DIST.py
1
2  import numpy as np
3  from pandas import *
4  import netCDF4
5  import sys, datetime
6
7  def dt2jul(dt):
8    yr=dt.year
9    deltaT=dt-datetime.datetime(yr,1,1)
10    deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
11    return (yr*1000+deltaT.days+1,deltaH*10000)
12
13  def jul2dt(jultm):
14    jul,tm=jultm[:]
15    yr=int(jul/1000)
16    ih=int(tm/10000.)
17    return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)
18
19  P='./'
20  df_twnaq=read_csv(P+'town_aqstEnew.csv')
21
22  #read and store the daily mean incremental values of PM2.5
23  fname,v_in=sys.argv[1],sys.argv[2]
24  nc = netCDF4.Dataset(fname, 'r')
25  tflag=nc.variables['TFLAG'][:,0,0]
26  nt=len(tflag)
27  ymd=[jul2dt([tflag[i],0]).strftime('%Y%m%d') for i in range(nt)]
28  var=nc.variables[v_in][:,0,:,:]
29  nc.close()
30  #read the district fraction distributions
31  nc = netCDF4.Dataset(P+'CNTYFRAC_TWN_3X3.nc','r')
32  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
33  ntt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
34  T=[]
35  for v in V[3]:
36    if v[0] !='T':continue
37    if v == 'T5300': continue
38    T.append(v)
39  nv=len(T)
40  dfrac=np.zeros(shape=(nv,nrow,ncol))
41  for v in T:
42    iv=T.index(v)
43    dfrac[iv,:,:]=nc.variables[v][0,0,:,:]
44    idx=np.where(dfrac[iv,:,:]>0)
45    dfrac[iv,idx[0],idx[1]]=1.
46  nc.close()
47
48  AQD={'Northern':[1,11,12,31,32,33,35],'Central':[17,22,36,37,38,39,40],'Southern':[2,21,41,42,43],
49      'Yilan':[34],'Huadong':[45,46]}
50  NCS=[i for i in AQD]
51  [y_code,s_code,m_code,d_code,h_code,v_code]=[[] for i in range(6)]
52
53  #loop for each township
54  for d in NCS[:]:
55    for i in AQD[d]:
56      dfa = df_twnaq.loc[df_twnaq.code1 == i].reset_index(drop=True)
57      if len(dfa)==0:sys.exit('county not right')
58      for ii in dfa.new_code:
59        if ii == 0: continue
60        dct = 'T' + str(ii)
61        if dct not in T: continue
62        iv=T.index(dct)
63        pp = var[:, :, :] * dfrac[iv, :, :]
64  #    loop for time, only positive values are stored
65        for t in range(nt):
66          idx = np.where(pp[t,:,:] > 0)
67          ni=len(idx[0])
68          if ni==0:continue
69          y_code.append(ymd[t])
70          s_code.append(ii)
71          v_code.append(np.mean([pp[t,idx[0][k],idx[1][k]] for k in range(ni)]))
72
73  df=DataFrame({'tflag':y_code,'cnty':s_code,v_in:v_code})
74  name={i:j for i,j in zip(df_twnaq.new_code,df_twnaq.Name)}
75  df['name']=[name[i] for i in df.cnty]
76  df=df.sort_values(v_in,ascending=False).reset_index(drop=True)
77  df.set_index('tflag').to_csv(fname+'_ByCnty.csv')
78  sys.exit()