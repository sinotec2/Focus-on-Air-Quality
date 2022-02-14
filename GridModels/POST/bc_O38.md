---
layout: default
title: 境外PM2.5佔台灣平均值比例之計算
parent: Post Processing
grand_parent: CMAQ Model System
nav_order: 3
last_modified_date: 2022-02-13 21:05:14
---

# 境外O3 8小時值佔比之計算
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景
- 計算臭氧8小時模擬結果中，邊界流入濃度之相對比例，需要檔案：
  - TWN_CNTY_3X3.nc：縣市分區fraction值檔，用以判斷島內或海面
  - 16{:02d}d4.2dD：日均U10V10值，用以判斷邊界濃度是否為流入
  - 16{:02d}baseEF3.S.grd01D：日最大8小時值
  
## 計算要項：
### 流入邊界之定義
- 以邊界上日均值U10/V10為依據，西南邊界上之正值、東北邊界上之負值情況為流入邊界。
- 當日有任何點是流入邊界才進行(空間)平均值之計算，否則為0(無流入)
- 內陸點之選擇
  - 因為臭氧濃度在陸地上具有高度的變異性，因此需要特別考量檢討其代表性。
  - 測站：點數太少、且位於市區，可能偏向較低值
  - 所有陸地點：點數太多，且大多數點位落在山區低值，也有可能會趨向低值較低之內陸點，將會提高境外濃度所佔之比例
- 由於邊界點(81+135)*2=432點，因此在島內代表性的考量上也必須約有400點，以使平均值具有相同的基準。
- 取較高之400點濃度，以使境外比例較為合理  

### 境外比例之計算
- 取4邊界之平均最大8小時值做為邊界平均值，除以當日島內最大8小時值平均值，即為當日之境外貢獻比例

## [bnd-in.py]()
### 完整程式碼下載
- [github](https://github.com/sinotec2/cmaq_relatives/blob/master/post/bnd-in.py)

### 讀取海陸遮罩、邊界位置
- 引用`PseudoNetCDF.camxfiles.Memmaps.uamiv`以讀取CAMx模式模擬結果檔案(avrg格式)
- 讀取縣市代碼檔(`TWN_CNTY_3X3.nc`)，以辨識陸地及海域，mask儲存在`idx`矩陣裏。
- 定義邊界點位置的index備用

```python
kuang@master /nas1/camxruns/2016_v7/outputs
$ cat ./Annual_F2/base/bnd-in.py
from PseudoNetCDF.camxfiles.Memmaps import uamiv
...

#read the interio point indices
fname='/nas1/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/TWN_CNTY_3X3.nc'
...
idx=np.where(var>0.)
...
#boundary indices
S,N,W,E=[(1,i) for i in range(1,ncol-1)],[(nrow-2,i) for i in range(1,ncol-1)],[(i,ncol-2) for i in range(1,nrow-1)],[(i,ncol-2) for i in range(1,nrow-1)]
Sb,Nb=np.array(S).flatten().reshape(81,2),np.array(S).flatten().reshape(81,2)
Wb,Eb=np.array(W).flatten().reshape(135,2),np.array(E).flatten().reshape(135,2)
lenBC=sum([len(i) for i in [S,N,W,E]])
seq='SNWE'
```
### 日最大8小時值之處理、讀取及分析
- 先以[NC8]()進行處理

```python
#the avrg files were processed by dmavrg, 8 hr daily max O3 is highlighted
v="O3eD"
#initalized the dataframe
df=DataFrame({})
for m in range(1,13):
  fname='16{:02d}baseEF3.S.grd01D'.format(m)
  conc= uamiv(fname,'r+')
  nt, nlay, nrow, ncol = (conc.variables[v].shape[i] for i in range(4))
  # surface daily mean UV10 were also been prepared by dmavrg
  fmet='/nas1/camxruns/2016_v7/met/16{:02d}d4.2dD'.format(m)
  uv10= uamiv(fmet,'r')
  #inward time and location indices at each boundaries
  Si=np.where(uv10.variables['V10_MpSD'][:,0,Sb[:,0],Sb[:,1]]>0)
  Ni=np.where(uv10.variables['V10_MpSD'][:,0,Nb[:,0],Nb[:,1]]<0)
  Wi=np.where(uv10.variables['U10_MpSD'][:,0,Wb[:,0],Wb[:,1]]>0)
  Ei=np.where(uv10.variables['U10_MpSD'][:,0,Eb[:,0],Eb[:,1]]<0)
  bc=np.zeros(shape=(4,nt))
  for s in seq:
    o3bc=[]
    exec('ii='+s+'i')
    for t in range(nt):
      if t in set(ii[0]):
        idxs=np.where(ii[0]==t)
        if s=='S':avg=np.mean(conc.variables[v][t,0,1,Si[1][idxs[0]]])
        if s=='N':avg=np.mean(conc.variables[v][t,0,nrow-2,Ni[1][idxs[0]]])
        if s=='W':avg=np.mean(conc.variables[v][t,0,Wi[1][idxs[0]],1])
        if s=='E':avg=np.mean(conc.variables[v][t,0,Ei[1][idxs[0]],ncol-2])
        o3bc.append(avg)
      else:
        o3bc.append(0.)
    js=seq.index(s)
    bc[js,:]=np.array(o3bc)
  #sort the max. 400 pts among interio points and take mean
  o3in=[]
  for t in range(nt):
    a=list(conc.variables[v][t,0,idx[0],idx[1]])
    a.sort()
    o3in.append(np.mean(a[-lenBC:]))
  js=seq.index(s)
  DD={'JDATE':np.array(conc.variables['TFLAG'][:,0,0]),'o3in':o3in}
  for s in seq:
    js=seq.index(s)
    DD.update({s:bc[js,:]})
  df=df.append(DataFrame(DD),ignore_index=True)
bcm=[]
for i in range(len(df)):
  a=np.array(df.iloc[i,2:6])
  bcm.append(np.nanmean(np.where(a>0,a,np.nan)))
df['bcR']=[j/i for i,j in zip(list(df.o3in),bcm)]
df.set_index('JDATE').to_csv('bc-in.csv')

P,N,R=[],[],[]
for p in range(60,101):
  a=df.loc[df.o3in>p]
  N.append(len(a))
  R.append(np.mean(a.bcR))
  P.append(p)
DD={}
for s in 'PNR':
  exec('DD.update({"'+s+'":'+s+'})')
dfp=DataFrame(DD)
dfp.set_index('P').to_csv('dfp.csv')
```
