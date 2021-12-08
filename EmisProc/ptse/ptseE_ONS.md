---
layout: default
title: "TimVar for Elevated PTS"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 2
date:               
last_modified_date:   2021-12-06 12:09:47
---

# 高空點源之時變係數
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
- 高空點源的**時變係數**骨幹是CEMS數據，然而同一工廠無數據、鄰近工業區其他廠無數據者，亦會參考CEMS設定其**時變係數**。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)中的副程式

## 程式說明

### 程式執行
因排放物質類別與污染源製造程序的特徵有關，必須分開個別處理，此處則以個別污染項目執行`ptseE_ONS.py`，執行方式如下：

```bash
for spe in CO NMHC NOX PM SOX;do python ptseE_ONS.py $spe;done
```

- 由於程式消耗記憶體非常大量，如要同時進行，需注意記憶體的使用情形。
- 污染源個數與排放高度限值的設定、地面PM排放條件之給定、以及數據年代等等都有關係，需配套紀錄。


### 排放與CEMS資料檔之讀取及準備
- 引用模組
  - 程式用到[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)中的副程式`CORRECT`, `add_PMS`, `check_nan`, `check_landsea`, `FillNan`, `WGS_TWD`, `Elev_YPM`

```python
kuang@node03 /nas1/TEDS/teds11/ptse
$ cat -n ptseE_ONS.py
     1
     2  #! crding = utf8
     3  from pandas import *
     4  import numpy as np
     5  import os, sys, subprocess
     6  import netCDF4
     7  import twd97
     8  import datetime
     9  from calendar import monthrange
    10  from scipy.io import FortranFile
    11
    12  from ptse_sub import CORRECT, add_PMS, check_nan, check_landsea, FillNan, WGS_TWD, Elev_YPM
    13
```

- 從工作目錄讀取teds版本與年代
```python
    14  #Main
    15  P=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')+'/'
    16  teds=int(P.split('/')[3][-2:])
    17  yr=2016+(teds-10)*3
    18  ndays=365
    19  if yr%4==0:ndays=366
    20  s365=set([i*24 for i in range(ndays)])
    21  nhrs=ndays*24
    22
```
- 檔案讀取與品質確認
  - 此個案將所有點源資料庫的數據都以「高空」方式處理(cutting height of stacks`Hs=10`)

```python
    23  Hs=10 #cutting height of stacks
    24  #Input the TEDS csv file
    25  try:
    26    df = read_csv('point.csv', encoding='big5')
    27  except:
    28    df = read_csv('point.csv')
    29  # check_NOPandSCC(0)
    30  df = check_nan(df)
    31  # check and correct the X coordinates for isolated islands
    32  df = check_landsea(df)
    33  df = WGS_TWD(df)
    34  df = Elev_YPM(df)
```
- 使用`Hs`進行篩選「高空」點源

```python
    35  df=df.loc[(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))].reset_index(drop=True)
```
- 排除沒有SNCPV排放者

```python
    36  df['SUM']=[i+j+k+l+m for i,j,k,l,m in zip(df.SOX_EMI,df.NOX_EMI,df.CO_EMI,df.PM_EMI,df.NMHC_EMI)]
    37  df=df.loc[df.SUM>0].reset_index(drop=True)
    38  df['CP_NO'] = [i + j for i, j in zip(list(df['C_NO']), list(df['NO_S']))]
    39  df['DY1']=[i*j for i,j in zip(df.DW1,df.WY1)]
    40  df['HY1']=[i*j for i,j in zip(df.HD1,df.DY1)]
    41
```
### 讀取並填滿CEMS資料檔
- 填滿資料表
  - 程式運作需要每筆**管煙**(**管編**+**煙編**)、每個小時都要有數值。將DataFrame轉成矩陣，再轉回DataFrame即可。

```python
    42  #71 factories with CEMS will emit (at ground) when stacks are operating
    43  fname=P+'point_cems.csv'
    44  cems=read_csv(fname)
    45  val='SOX PM NOX FLOW X_BLANK1 X_BLANK2'.split()
    46  nval=len(val)
```
- **管煙**欄位為處理過後檔案的特徵

```python
    47  if 'CP_NO' not in cems.columns: #pre-process
    48    cems=cems.drop(cems.loc[cems.C_NO=='C_NO'].index).reset_index(drop=True)
```
- 新增**管編**+**煙編**(**管煙**)之新標籤、新增PM(設為SN之平均值)

```python
    49    cems['CP_NO'] = [i + j for i, j in zip(list(cems['C_NO']), list(cems['NO_S']))]
    50    cems['PM']=[(i+j)/2 for i,j in zip(cems.SOX,cems.NOX)]
```
- 新增時間標籤`MDH`。有的年度提供的CEMS檔案小時標記為0000~2300，有的是0~23，因此需要判斷一下

```python
    51    if max(cems.HOUR)>100:
    52      cems['MDH']=[int(i*10000+j*100+k/100) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
    53    else:
    54      cems['MDH']=[int(i*10000+j*100+k) for i,j,k in zip(cems.MONTH,cems.DATE,cems.HOUR)]
```
- 一個(**管煙**,**時籤**)組合只應對應一組CEMS數據，以`pivot_table sum`進行整併  

```python
    55    cems=pivot_table(cems,index=['CP_NO','MDH'],values=val,aggfunc=sum).reset_index()
```
- 維度標籤之計算。如果使用`標籤=序列.index(值)`指令將會非常耗時，直接使用`dict{值:標籤}`，會快很多。

```python
    56    #cems(df) convert to cemsM(matrix)
    57    for MC in ['CP_NO','MDH']:
    58      mc=MC.lower()
    59      exec(mc+'=list(set(cems.'+MC+'))');exec(mc+'.sort()')
    60      exec('n'+MC+'=len('+mc+')')
    61      exec('d'+MC+'={'+mc+'[i]:i for i in range(n'+MC+')}')
    62      exec('cems["i'+MC+'"]=[d'+MC+'[i] for i in cems.'+MC+']')
    63    if len(mdh)!=ndays*24:sys.exit('mdh coverage not enough!')
```
- `DataFrame`轉成`Array`，因所有值預設為0，如此就補滿空缺值了。有數據的部分再填入`Array`。

```python
    64    cemsM=np.zeros(shape=(nMDH,nCP_NO,nval))
    65    for i in range(nval):
    66      cemsM[cems.iMDH[:],cems.iCP_NO[:],i]=cems[val[i]]
```
- Array再轉回`DataFrame`。因後面CEMS數據使用邏輯太多樣了，`Array`形式不敷應用。

```python
    67    DD={}
    68    for i in range(nval):
    69      DD[val[i]]=cemsM[:,:,i].flatten()
    70    DD['MDH']  =[i for i in mdh for j in cp_no]
    71    DD['CP_NO']=[j for i in mdh for j in cp_no]
    72    cems=DataFrame(DD)
    73    cems['C_NO']=[i[:8] for i in cems.CP_NO]
    74    cems['MD']=[i//100 for i in cems.MDH]
    75    cems.set_index('CP_NO').to_csv(fname)
```

### 整理CEMS各廠運作時間模式
- 讀取資料庫欄位(**管編**`C_NO`, **管煙**`CP_NO`, 月日時`MDH`, 月日`MD`,)

```python
    76  for MC in ['CP_NO','MDH','MD','C_NO']:
    77    mc=MC.lower()
    78    exec(mc+'=list(set(cems.'+MC+'))');exec(mc+'.sort()')
    79    exec('n'+MC+'=len('+mc+')')
    80
```
- 沒有CEMS之同家工廠其它煙道、或鄰近工廠，可能具有上下游連動關係，因此適用該CEMS的操作特性，此處先行備妥。
  - 個別廠的日操作特性，分析全年SOX排放量之小時變化，按排放量排序，代表最有可能運作之小時。
  - 先執行`pivot_table`加總

```python
    81  #Hour of Day pattern
    82  cems['HR']=[i%100 for i in cems.MDH]
    83  pv_cems1=pivot_table(cems,index=['C_NO','HR'],values='SOX',aggfunc=sum).reset_index()
    84
```
  - 以**管編**為索引之新的`DataFrame`，其內容為小時之序位

```python
    85  cems_HROD=DataFrame({'C_NO':c_no})
    86  cems_HROD['SOX_HR_ODER']=0
    87  for ic in cems_HROD.index:
    88    pv1=pv_cems1.loc[pv_cems1.C_NO==c_no[ic]]
    89    pv3=pv1.sort_values('SOX',ascending=False).reset_index(drop=True)
    90    cems_HROD.loc[ic,'SOX_HR_ODER']=''.join(['{:d} '.format(i) for i in pv3.HR])
```
- 同樣原理應用在全年的逐日變化，內容為序列`mdh`的標籤。排序依據全天的流量總計，值越高者表當天最可能運作。 

```python
    91  #orders for DY1
    92  pv_cems2=pivot_table(cems,index=['C_NO','MD'],values='FLOW',aggfunc=sum).reset_index()
```
  - `MD`欄位由**月日**轉變成`mdh`的標籤，轉變需要2步驟，否則會出錯

```python  
    93  #Indexing is an exhaustive process.
    94  iMD=[mdh.index(i*100) for i in pv_cems2.MD] #change the MMDD into index sequence among MMDD00's
    95  pv_cems2.MD=iMD
```
  - 以**管編**為索引之新的`DataFrame`，其內容為**日期標籤之序位**

```python
    96  cems_DAOD=DataFrame({'C_NO':c_no})
    97  cems_DAOD['FLOW_DA_ODER']=0
    98  for ic in cems_DAOD.index:
    99    pv1=pv_cems2.loc[pv_cems2.C_NO==c_no[ic]]
   100    pv3=pv1.sort_values('FLOW',ascending=False).reset_index(drop=True)
   101    cems_DAOD.loc[ic,'FLOW_DA_ODER']=''.join(['{:d} '.format(i) for i in pv3.MD])
   102
```

### 套用CEMS或運作時間模式
- 建立各**管編**座標值之資料表

```python
   103  dfxy=pivot_table(df,index='C_NO',values=['UTM_E','UTM_N'],aggfunc=np.mean).reset_index()
   104
```
- `BLS`為污染項目與布林值的對照表。以直接提取資料庫中符合布林值、要處理的筆數。
  - `{'NMHC':'PM', 'NMHC':'PM'}`因為`NMHC`及`CO`沒有`CEMS`數據，假設與`PM`、`NOX`一樣。

```python
   105  #booleans for pollutant selection
   106  c2v={'NMHC':'PM','SOX':'SOX','NOX':'NOX','PM':'PM','NMHC':'PM'} #point.csv vs cems.csv
   107  BLS={c:df[c+'_EMI']>0 for c in c2v}
   108  colT=['HD1','DY1','HY1']
   109  col=['C_NO','CP_NO','HD1','DY1','HY1']+[i for i in df.columns if 'EMI' in i]
```
- `s`為物質種類，須由引數讀取，且限定在`BLS`的索引範圍(`c2v`)

```python
   110  for spe in [s for s in [sys.argv[1]] if s in BLS]:
   111    dfV=df[col].loc[BLS[spe]].reset_index(drop=True)   
```
- 對全廠加總並形成新的資料庫`dfV`

```python
   112    dfV1=pivot_table(dfV,index='CP_NO',values=spe+'_EMI',aggfunc=sum).reset_index()
   113    dfV2=pivot_table(dfV,index='CP_NO',values=colT,aggfunc=np.mean).reset_index()
   114    dfV=merge(dfV1,dfV2,on='CP_NO')
   115    dfV['C_NO']=[i[:8] for i in dfV.CP_NO]
   116    for c in colT:
   117      dfV[c]=np.array(dfV[c],dtype=int)
```
- 對照資料庫(`a`)與cems(`b`)的**管編**`cp`
  - `ab`為二者交集
  - `b1`為`b-a`，有CEMS數據卻不在資料庫中、沒有座標
  - `c1`為`ab-b1`(就等於`ab`)
  - 列出所有`c1`的座標序列

```python
   118    a,b=list(set(dfV.C_NO)),list(set(cems.C_NO));a.sort();b.sort()
   119    ab=[i for i in a if i in b]
   120    cp=list(set(dfV.CP_NO))
   121    cp.sort()
   122    ons=np.zeros(shape=(len(cp),nMDH))#,dtype=int)
   123    #other fatories without CEMS, take the nearest one
   124    b1=set(b)-set(dfxy.C_NO) #cems factory but without UTM location
   125    c1=[c for c in b if c not in b1 and c in a] #cems plant with X,Y
   126    cemsX=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0] for c in c1])
   127    cemsY=np.array([list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0] for c in c1])
```
- 逐一**管編**進行迴圈
  - 如果工廠沒有CEMS(`c not in ab`)，則以最近的一家廠的日變化特徵為其**時變係數**，令`c_cems`為該廠**管編**
  - 如果該廠**日期標籤之序位**不足全年日數(ndays)，也將補足缺漏日之標籤`list(s365-set(pv2MD))`

```python
   128    #loop for every factories
   129    for c in [i for i in a if i not in b1]:
   130      c_cems=c
   131      if c not in ab:
   132        x0,y0=list(dfxy.loc[dfxy.C_NO==c,'UTM_E'])[0],list(dfxy.loc[dfxy.C_NO==c,'UTM_N'])[0]
   133        dist=(cemsX-x0)**2+(cemsY-y0)**2
   134        idx=list(dist).index(min(dist))
   135        c_cems=c1[idx]
   136      pv2MD=np.array(list(cems_DAOD.loc[cems_DAOD.C_NO==c_cems,'FLOW_DA_ODER'])[0].split(),dtype=int)
   137      if len(pv2MD)<ndays: pv2MD=np.array(list(pv2MD)+list(s365-set(pv2MD)))
   138      df_cp=dfV.loc[dfV.C_NO==c].reset_index(drop=True)
```
- 該廠所有**煙編**逐一進行  

```python
   139      #loop for every NO_S in this factory
   140      for p in set(df_cp.CP_NO):
   141        ip=cp.index(p)
```
  - 如果是CEMS煙道，其全年變化即為CEMS資料表中數值
  - **point_cems.csv**檔案內容須事先確認其單位，此處要求其全年總合為1.0

```python
   142        if p in set(cems.CP_NO):
   143          ons[ip,:]=cems.loc[cems.CP_NO==p,c2v[spe]]*nhrs
```
  - 將工廠操作矩陣(維度為`(日數、時數)`)先設定為0
  - 如果不是，則由資料庫中讀取工作日數及小時數
    - 如果是全天連續操作，則逐時都需標籤
```python
   144        else:
   145          dy1=dfV.DY1[ip]
   146          hd1=dfV.HD1[ip]
   147          md3=pv2MD[:dy1]
   148          days=np.zeros(shape=(dy1,hd1),dtype=int)
   149          if hd1==24:
   150            hrs=np.array([i for i in range(24)],dtype=int)
```   
  - 不是24小時，最有可能的小時，則由前面準備好的`cems_HROD.SOX_HR_ODER`第1小時開始，依序填入工作時數。
    - 工作日則由為前述最可能工作的**日期標籤之序位**依序填入，形成`days`(月、日、時標籤)
    - 將`days`壓平成為一維矩陣
    - 這些有運作的時間，其`ons`值為1(其餘內設為0)   

```python    
   151          else:
   152            first=np.array(list(cems_HROD.loc[cems_HROD.C_NO==c_cems,'SOX_HR_ODER'])[0].split(),dtype=int)[0]
   153            hrs=np.array([(first+ih)%24 for ih in range(hd1)])
   154          for id in range(dy1):
   155            days[id,:]=md3[id]+hrs[:]
   156          idx=days.flatten()
   157          ons[ip,idx]=1.
```

### 輸出結果 

```python
   158  #other sources
   159    fnameO=spe+'_ECP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
   160    with FortranFile(fnameO, 'w') as f:
   161      f.write_record(cp)
   162      f.write_record(mdh)
   163      f.write_record(ons)
```


## 檔案下載
- `python`程式：[ptseE_ONS.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseE_ONS.py)。
- `jupyter-notebook`檔案[ptseE_ONS.ipynb](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseE_ONS.ipynb)
- [nbviewer](https://nbviewer.org/github/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/ptse/ptseE_ONS.ipynb)

## Reference
