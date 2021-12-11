---
layout: default
title: "prep_TimVar"
parent: "Area Sources"
grand_parent: "TEDS Processing"
nav_order: 2
date:               
last_modified_date:   2021-12-01 14:16:46
---

# 計算時間變異係數對照表
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
- 為消除資料庫在時間與空間的相依性，需要消除資料庫**類別-縣市**之維度，此處即針對面源的**時間變異係數與類別-縣市之對照表**(`nc_fac.json`)進行計算，以備未來套用。主要問題出現在環保署提供的**時變係數檔**，空間資料為**中文名稱**，與主資料庫是鄉鎮區代碼**2碼編號**不能對應，分3個程式說明：
  - 時間變異係數(`csv`)檔案前處理
  - `csv`檔案之產生
  - 將`csv`檔案應用到面源排放量資料庫，並展開至全年逐時之序列，存成`nc_fac.json`。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[面源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)與[重新計算網格座標](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/prep_areagridLL/)，為此處之前處理。  

## 時間變異係數檔案前處理([prep_dfAdmw.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_dfAdmw.py))分段說明
- 此程式為可執行的主程式，主要處理**縣市名稱**與**編號**的對照，中文改成英文。
- 引用模組
  - 會用到中文轉英文的`pypinyin`模組，以使程式可以在py27/py37都可以使用
  - 引用副程式`prep_df`，說明如後。
```python
kuang@node03 /nas1/TEDS/teds11/area
$ cat -n prep_dfAdmw.py
     1  #!coding=utf8
     2  import numpy as np
     3  from pandas import *
     4  from pypinyin import pinyin, lazy_pinyin
     5  import subprocess
     6  import json
     7  from datetime import datetime, timedelta
     8  from prep_df import PrepDf
     9  import sys, os
    10
    11
```
- 從中文檔案[cnty.csv](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/cnty.csv)開始處理
  - 補充連江縣
```python    
    12  #input and prepare the cnty names
    13  df_cnty=read_csv('cnty.csv',encoding='big5')
    14  for i in range(len(df_cnty)):
    15    cha=df_cnty.loc[i,'cnty']
    16    ll=lazy_pinyin(cha)
    17    s=''
    18    for l in ll:
    19      s=s+l
    20    df_cnty.loc[i,'cnty']=s
    21  df_cnty['no']=[str(s) for s in df_cnty.no]
    22  df_cnty['no']=['0'*(2-len(s))+s for s in df_cnty.no]
    23  df_cnty.loc[len(df_cnty),'no']=51
    24  df_cnty.loc[len(df_cnty)-1,'cnty']='lianjiangxian'
```
- 補充五都名稱、機場名稱
```python    
    25
    26  #dictionary of region name to county number
    27  d_cnty={x:str(int(y)) for x,y in zip(df_cnty['cnty'],df_cnty['no'])}
    28  d_cnty.update({'xinbeishi':'31','taoyuanshi':'32',\
    29  'hualianjichang':'45','taidongjichang':'46','lvdaojichang':'46','lanyujichang':'46','magongjichang':'44','jinmenjichang':'50', \
    30  'taizhongjichang':'36','tainanjichang':'21','jiayijichang':'40','qimeijichang':'44','wanganjichang':'44','beiganjichang':'51',\
    31  'nanganjichang':'51','songshanjichang':'1','xiaogangjichang':'2','taoyuanjichang':'32'})
    32
```
- 新的直轄市與舊編號的對照
```python
    33  #combination of 5 Municipalities
    34  NewCities={'tainanshi':{'21','41'},'taizhongshi':{'17','36'},'gaoxiongshi':{'2','42'}}
    35
```
- 補充港口名稱與縣市編號之對照
```python    
    36  #including the harbors
    37  gangko='gaoxionggang jilonggang anpinggang shenaozhuanyongyougang taibeigang shalunwaihaixieyoufutong suaogang taizhonggang mailiaogang budaigang xingdadianchangxiemeimatou yonganyehuatianranqijieshouzhan magonggang hualiangang hepinggang jinmengang mazugang'.split()
    38  gangkoC=['2','11','21','31','31','36','34','36','39','40','42','42','44','45','45','50','51']
    39  d_gangko={i:j for i,j in zip(gangko,gangkoC)}
    40  d_cnty.update(d_gangko)
    41
```
- 環保署提供的**時變係數檔案**亦有以空品區為單位之情形，需另建對照表
```python    
    42  # air quality basins
    43  d_kpq={'beibukongpinqu':['taibeishi','taoyuanshi','xinbeishi','jilongshi'], \
    44  'gaopingkongpinqu':['gaoxiongshi','gaoxiongxian','pingdongxian'],\
    45  'huadongkongpinqu':['hualianxian','taidongxian'], \
    46  'yilankongpinqu':['yilanxian'],'yunjianankongpinqu':['yunlinxian','jiayixian','jiayishi','tainanshi'], \
    47  'zhongbukongpinqu':['taizhongshi','taizhongxian','zhanghuaxian','nantouxian'], \
    48  'zhumiaokongpinqu':['miaolixian','xinzhushi','xinzhuxian']}
    49  d_kpq.update({'quanguo':list(df_cnty['cnty'])})
    50  d_kpq.update({'lidao':['jinmenxian','lianjiangxian','penghuxian']})
    51
```
- 分別執行月變化、週變化與日變化檔案之整理與輸出
```python    
    52  #execution of dataframe formings and savings
    53  csvs={'m':'mon.csv','w':'week.csv','d':'day.csv'}
    54  for t in 'mwd':
    55    df='df_A'+t
    56    try:
    57      exec(df+'=read_csv("'+df+'")')
    58    except:
    59      exec(df+'=PrepDf("'+csvs[t]+'")')
    60      exec(df+'.set_index("nsc2").to_csv("'+df+'")')
    61
```
- 由於分段執行，需將對照表寫出備用。如合併執行則無此需要。
```python
    62  # output the dictionary
    63  for kc in ['cnty','kpq']:
    64    with open('d_'+kc+'.json', 'w', newline='') as jsonfile:
    65      exec('json.dump(d_'+kc+', jsonfile)')
```

## 副程式([prep_df.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_df.py))分段說明
主程式處理對照，副程式則處理**時變係數檔**內部的不一致性
- 引用模組

```python
     1  import numpy as np
     2  from pandas import *
     3  from pypinyin import pinyin, lazy_pinyi
```
- 先將中文改成英文，以便對照

```python
     4  #prepare the dataframe
     5  def PrepDf(fname):
     6    path=''#'/home/sespub/teds10/08-時間分配權重/月週日時間權重/'
     7    df=read_csv(path+fname,encoding='big5')
     8    df.loc[df.NSC_SUB.map(lambda x: isna(x)),'NSC_SUB']='b'
     9    df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
    10    for i in range(len(df.REGION)):
    11      cha=df.loc[i,'REGION']
    12      if type(cha) in [int,float]:continue
    13      ll=lazy_pinyin(cha)
    14      if len(ll)==0:continue
    15      s=''
    16      for l in ll:
    17        s=s+l
    18      df.loc[i,'REGION']=s
```
- **時變係數檔**中有以全形頓號「、」來表示縣市的聯集，需逐一拆解改成資料庫對應關係
```python
    19    a=df.loc[df.DICT.map(lambda x:type(x)==str and '、' in x)]
    20    idx=a.index
    21    df=df.drop(idx).reset_index(drop=True)
    22    a=a.reset_index(drop=True)
    23    for i in range(len(a)):
    24      dct=a.loc[i,'DICT'].split('、')
    25      b=DataFrame({})
    26      for j in range(len(dct)):
    27        b=b.append(a.loc[i],ignore_index=True)
    28        b.loc[j,'DICT']=dct[j]
    29      df=df.append(b,ignore_index=True)
```
- **時變係數檔**中有空白者，意即全國，需填以明確的文字
```python
    30    idx=df.loc[df.REGION.map(lambda x:type(x)==float and np.isnan(x))].index
    31    df.loc[idx,'REGION']=['quanguo' for i in idx]
    32    for c in df.columns:
    33      if c in ['REGION','NSC','NSC_SUB','nsc2','DICT']:continue
    34      df[c]=[float(i) for i in list(df[c])]
```
- **時變係數檔**中以`51`代表所有類別的船舶，與主資料檔的作法又有出入
```python
    35  #change 51b to 51A~51D, no need changing it manually
    36    snsc2=set(df.nsc2)
    37    if '51b' in snsc2:
    38      df51=df.loc[df.nsc2=='51b'].reset_index(drop=True)
    39      for s in 'ABCD':
    40        if '51A' not in snsc2:
    41          tmp=df51
    42          tmp.nsc2='51'+s
    43          df=df.append(tmp,ignore_index='True',sort=False)
```
- 確認是否漏了臺中機場的時間變化，如是，則以臺南機場變化形態代之。
```python
    44  # taizhongjichang is missing, fill it according tainanjichang
    45    if 'taizhongjichang' not in set(df.REGION):
    46      a=df.loc[df.REGION=='tainanjichang'].reset_index(drop=True)
    47      a.DICT=3605
    48      a.REGION='taizhongjichang'
    49      df=df.append(a,ignore_index=True)
```
- 刪去重覆記錄、重置順序、輸出DataFrame檔案
```python
    50    df.drop_duplicates(inplace=True)
    51    df=df.reset_index(drop=True)
    52    return df
```

## `nc_fac.json`檔案產生程式([prep_json.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_json.py))分段說明
- 引用模組
```python
kuang@node03 /nas1/TEDS/teds11/area
$ cat -n prep_json.py
     1  #!coding=utf8
     2  import numpy as np
     3  from pandas import *
     4  import subprocess
     5  import json
     6  from datetime import datetime, timedelta
     7  import sys, os
     8
```
- 讀入前面[prep_dfAdmw.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_dfAdmw.py)的執行成果：`df_Am`、`df_Aw`、`df_Ad`三個檔案
```python
     9  # read the time variation factors
    10  csvs={'m':'mon.csv','w':'week.csv','d':'day.csv'}
    11  for t in 'mwd':
    12    df='df_A'+t
    13    try:
    14      exec(df+'=read_csv("'+df+'")')
    15    except:
    16      sys.exit('df_A? not found, please re-run prep_dfAdmw.py ')
    17
```
- `s_nsc2`：所有面源分類項目形成的集合，有時間變化者
```python
    18  #union of nsc2 in time variation files
    19  s_nsc2=set(df_Ad.nsc2) | set(df_Am.nsc2) | set(df_Aw.nsc2)
    20
```
- 開啟檔案、刪除重複記錄、產生`nsc2`、`CNTY`，此2項目為對照表的主要索引。
```python
    21  #open the TEDS area csv file
    22  pwd=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n')
    23  teds=pwd.split('/')[3][4:6]
    24  fname='areagrid'+teds+'LL.csv'
    25  df = read_csv(fname)
    26  df.drop_duplicates(inplace=True)
    27  df=df.reset_index(drop=True)
    28  if 'nsc2' not in df.columns:
    29    df.loc[df['NSC_SUB'].map(lambda x: (type(x)==float and np.isnan(x)==True) or ( x==' ')),'NSC_SUB']='b'
    30    df['nsc2']=[str(x)+y for x,y in zip(df['NSC'],df['NSC_SUB'])]
    31  df.loc[df['DICT'].map(lambda x:np.isnan(x)==True),'DICT']=5300.
    32  if 'CNTY' not in df.columns:
    33    df['CNTY']=[str(int(s/100)) for s in list(df['DICT'])]
    34
```
- 定義資料庫的座標系統，去尾到1公里解析度
```python
    35  #definition the coordinates of database
    36  minx,miny=min(df.UTME),min(df.UTMN)
    37  df.UTME=round(df.UTME-minx,-3)
    38  df.UTMN=round(df.UTMN-miny,-3)
    39  df['YX']=np.array(df.UTMN+df.UTME/1000,dtype=int)
    40
```
- 同1網格、同一縣市別、同一類別，可能有好幾筆資料(不同鄉鎮區，由**時變檔案**角度無法區分)，排放量予以加總。縮減資料表。
```python
    41  #sum-up the grids which length maybe smaller than 1KM
    42  cole=['EM_SOX','EM_NOX','EM_CO','EM_PM25','EM_PM','EM_NMHC']
    43  coli=['CNTY', 'nsc2','YX']
    44  df=pivot_table(df,index=coli,values=cole,aggfunc=np.sum).reset_index()
```
- 形成縣市代碼、面源類別、位置的序列、序列長度、標籤對照表
```python
    45  #nXXX:len of list XXX; dXXX:index dictionary of listXXX, iXXX:index of XXX
    46  for c in ['CNTY','nsc2','YX']:
    47    exec(c+'=list(set(df.'+c+'))')
    48    exec(c+'.sort()')
    49    exec('n'+c+'=len('+c+')')
    50    exec('d'+c+'={'+c+'[i]:i for i in range(n'+c+')}')
    51    exec('df["i'+c+'"]=[d'+c+'[i] for i in df.'+c+']')
    52
```
- **時變係數檔**之面源類別可能只有大類，而資料表中含細類，必須全都適用大類的係數
```python
    53  #same NSC in df_A? and df, but without NSC_SUB, all add to s_nsc2
    54  nsc2b=set([i for i in s_nsc2 if i[-1]=='b'])
    55  for ii in nsc2b-set(df.nsc2):
    56    i=int(ii[:-1])
    57    s_nsc2=s_nsc2|set(df.loc[df.nsc2.map(lambda x:x[:-1]==i),'nsc2'])
```
- 區域代碼組合(`rgn`)的個數`n_rgn`,、集合`s_rgn`、對照表`d_rgn`
```python
    58  #Tuple_of_Length ={0, 101, 10000, 10101, 131313, 171717, 202020, 212121, 250101}
    59  n_rgn,s_rgn,d_rgn={},[],{}
    60  for n in s_nsc2:
    61    tl_rgn=(len(df_Am[df_Am.nsc2==n])*100+len(df_Aw[df_Aw.nsc2==n]))*100+len(df_Ad[df_Ad.nsc2==n])
    62    s_rgn.append(tl_rgn)
    63    n_rgn[n]=tl_rgn
    64    d_rgn[tl_rgn]=n #recording last nsc2 for calling
    65  s_rgn=set(s_rgn) #tuple of region numbers
    66
```
- 由teds版本計算年代(`yr`)
  - `dts`為全年逐時之**時間標籤**（`datetime`）
```python
    67  yr=2016+(int(teds)-10)*3
    68  bdate=datetime(yr,1,1)-timedelta(days=1)
    69  nd365=365+2
    70  if yr%4==0:nd365=366+2
    71  nty=nd365*24
    72  dts=[bdate+timedelta(days=i/24.) for i in range(nty)]
    73
```
- 讀取或產生`nsc2`及可能應用的縣市代碼`CNTY`對照表
```python
    74  #n_cnty: the dictionary of nsc2 vs cnties applied
    75  if os.path.exists('n_cnty.json'):
    76    with open('n_cnty.json', 'r', newline='') as jsonfile:
    77      n_cnty=json.load(jsonfile)
    78  else:
    79    for kc in ['cnty','kpq']:
    80      jsname='d_'+kc+'.json'
    81      if os.path.exists(jsname):
    82        with open(jsname, 'r', newline='') as jsonfile:
    83          exec('d_'+kc+'=json.load(jsonfile)')
    84      else:
    85        sys.exit('d_'+kc+'.json not found, please re-run prep_dfAdmw.py ')
```
- 對每種區域代碼組合進行迴圈
  - 挑出符合對類別、建立二者的對照關係
  - 存檔備用
```python
    86    n_cntys={}
    87    for tl in s_rgn: #tuple of lengs
    88      n=d_rgn[tl]
    89      cntys=[]
    90      for t in 'mwd':
    91        exec('regs=list(df_A'+t+'.loc[df_A'+t+'.nsc2==n,"REGION"])')
    92        if len(regs)==0:continue
    93        for r in regs:
    94          if r in d_kpq:
    95            cntys+=[d_cnty[i] for i in d_kpq[r]]
    96          else:
    97            cntys+=[d_cnty[r]]
    98      cntys=list(set(cntys))
    99      for n in [i for i in n_rgn if n_rgn[i]==tl]:
   100        n_cntys[n]=cntys
   101    with open('n_cnty.json', 'w', newline='') as jsonfile:
   102      json.dump(n_cntys, jsonfile)
   103
   104
```
- 如果沒有`nc_fac.json`，建立逐時**時間標籤**的月份、星期、小時序列備用
```python
   105  if not os.path.exists('nc_fac.json'):
   106    mns=np.array([dts[i].month-1 for i in range(nty)])
   107    wks=np.array([dts[i].weekday() for i in range(nty)])
   108    hrs=np.array([dts[i].hour for i in range(nty)])
   109
```
- 將df_A?的2欄內容(`df_A.nsc2`,`df_A.REGION`)，轉變成單一組合(`f_A[(n,c)]`)對照表
  - 先將`df_A`拉長
```python
   110    nts={'m':12,'w':7,'d':24}
   111    for t in 'mwd':
   112      exec('df_A=df_A'+t)
   113      df=DataFrame({})
   114      df_A['CNTY']=0
   115      for i in range(len(df_A)):
   116        cntys=[]
   117        a=df_A.loc[i]
   118        r=df_A.loc[i,'REGION']
   119        if r in d_kpq:
   120          cntys+=[d_cnty[i] for i in d_kpq[r]]
   121        else:
   122          cntys+=[d_cnty[r]]
   123        for c in cntys:
   124          a.CNTY=c
   125          df=df.append(a,ignore_index=True)
```
  - 整併標籤與其後的**時變係數**欄位內容 
```python
   126      f_A={}
   127      for j in range(len(df)):
   128        n=df.loc[j,'nsc2']
   129        c=df.loc[j,'CNTY']
   130        f_A[(n,c)]=[df.loc[j,str(i)] for i in range(1,nts[t]+1)]
   131      exec('f_A'+t+'=f_A')
```
- 有月變化而無週變化者，週變化係數設為1.0、有月變化而無日變化者，日變化係數設為1.0、
```python
   132    for i in set(f_Am)-set(f_Aw):
   133      f_Aw[i]=np.ones(shape=7)
   134    for i in set(f_Am)-set(f_Ad):
   135      f_Ad[i]=np.ones(shape=24)
   136
```
- 對每一個`(nsc2,cnty)`組合，計算全年的**時變係數**、存檔
```python
   137    nc_fac={}
   138    for n in s_nsc2:
   139      for c in n_cntys[n]:
   140        tup=(n,c)
   141        tp=n+'_'+c
   142        if tup not in f_Am:continue
   143        lfac=np.array([f_Am[tup][m]*f_Aw[tup][w]*f_Ad[tup][d] for m,w,d in zip(mns,wks,hrs)])
   144        sfac=sum(lfac)
   145        nc_fac[tp]=list(lfac/sfac)
   146
   147    with open('nc_fac.json', 'w', newline='') as jsonfile:
   148      json.dump(nc_fac, jsonfile)
   149
```
## 檔案下載
- 環保署**時變係數檔案**:[day.csv](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/day.csv)、[mon.csv](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/mon.csv)、[week.csv](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/area/week.csv)
- `python`程式：[prep_dfAdmw.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_dfAdmw.py)、[prep_df.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_df.py)、[prep_json.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/area/prep_json.py)

## Reference
