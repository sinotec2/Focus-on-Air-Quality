---
layout: default
title: 三維軌跡分析
nav_order: 6
parent: Trajectory Models
has_children: true
permalink: /TrajModels/btraj_WRFnests
last_modified_date: 2022-03-31 15:20:02
---

# WRF三維軌跡分析
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

## WRFOUT三維軌跡主程式
### wrfout檔案之彙整、連結
- 由於所需歷年來之wrfout，可能分散在不同目錄、磁碟機檔案系統、需要先做好連結。['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 時間規格：每天一個檔，檔案為逐時，自UTC 0時開始，結束於隔天0時。
- wrf版本：不限、不檢查

### bt2_DVP.py
- 3維軌跡程式參考2維程式進行增修，2維(CWB觀測值內插)軌跡程式公開於github(https://github.com/sinotec2/rd_cwbDay/blob/master/traj2kml.py)
- arguments:     -t daliao -d 20171231 -b T (測站名稱、軌跡起始的年月日時、是否為反軌跡(T/F))
- 輸入檔：sta_list.json：測站編號名稱path+'sta_ll.csv：測站經緯度['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]：各層wrfout檔案(連結)
- 輸出檔：'trj_results'+DATE[2:6]+'/'+'trj'+nam[0]+DATE+'.csv'
- 軌跡點時間間距：15S
- 程式內掛後處理(不執行不影響主要結果)csv2kml.py：繪製google mapcsv2bln.cs：bln file is used for surfer plotting

### download bt2.py

- {% include download.html content="軌跡線上通風指數之計算[addVi.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/ftuv10/addVI.py)" %}

### do_bt1.cs 動態執行批次檔
argument:
     $1=station name
     $2=month(2 digits)
     $3=day

```bash
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat do_bt1.cs
#do_bt1 station mm dd
st=$1
for y1 in {16..16};do
y=20$y1
#for m in {02..03};do
m=$2
ym=$y1$m
#for d in {01..31};do
d=$3
  h=00
  if ! [ -e links/wrfout_d04_${y}-${m}-${d}_${h}:00:00 ];then continue;fi
  for h in {00..23};do
    if [ -e trj_results${ym}/trj${st}${y}${m}${d}${h}.csv ];then continue;fi
    n=$(psg bt2.py|wc -l)
    while true;do
      if [ $n -lt 90 ];then
        touch trj_results${ym}/trj${st}${y}${m}${d}${h}.csv
        sub python bt2.py -t $st -d ${y}${m}${d}${h} -b True >& dum
        sleep 5s
        break
      else
        sleep 5s
        n=$(psg bt2.py|wc -l)
      fi
    done
  done
#done
#done
done
```

## 叢集分析
### choose10 .py(前處理)
從前述bt2.py所得之軌跡點L.csv檔案，選取其中10個點，將20個維度之矩陣進行k_means分析
輸入檔案：
     tmplateD1_3km.nc：讀取網格設定，以簡化軌跡點
     fnames.txt(檔案路徑名稱之listing)
輸出檔案：
     *10.csv

```python
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat -n choose10.py
     1  import os, sys
     2  import netCDF4
     3  import twd97
     4  from pandas import *
     5  import bisect
     6
     7  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
     8  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
     9
    10  nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')
    11
    12  ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
    13  tex=10**ex
    14  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    15  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    16
    17  os.system('ls trjzhongshan*L.csv>fnames.txt')
    18  with open('fnames.txt','r')as f:
    19    fnames=[i.strip('\n') for i in f]
    20
    21  for fname in fnames:
    22  #  if os.path.isfile(fname+'10.csv'):continue
    23    df=read_csv(fname)
    24    x=np.array(df.TWD97_x)-Xcent
    25    y=np.array(df.TWD97_y)-Ycent
    26    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    27    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    28    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    29    reduced_ji=[]
    30    for i in range(1,len(df)):
    31      if df.JI[i-1]!=df.JI[i]:
    32        reduced_ji.append(df.JI[i-1])
    33    df=DataFrame({'JI3':reduced_ji})
    34    if len(df)<10:continue
    35    ji10=[df.JI3[i] for i in range(0,len(df),int(len(df)/10))]
    36    df=DataFrame({'JI3':ji10[:10]})
    37    df.set_index('JI3').to_csv(fname+'10.csv')
```



### km.py
- arguments:條列*10.csv檔案路徑名稱之文字檔nclt: number of clusters
- 輸入檔*10.csv：choose10.py的結果tmplateD1_3km.nc：由JI轉換成網格化座標位置
- 輸出檔lab.csv：逐時的叢集編號'res'+str(l)+'.csv' ：各叢集的代表性軌跡
- 內掛後處理由csv產生kml→google map繪圖

```python
$ cat -n km.py
     1  import os, sys
     2  import netCDF4
     3  import twd97
     4  from pandas import *
     5  import bisect
     6  import numpy as np
     7  from sklearn.cluster import KMeans
     8
     9  txt=sys.argv[1]
    10  nclt=int(sys.argv[2])
    11  with open(txt, 'r') as f:
    12      fnames=[l.strip('\n') for l in f]
    13  idx=fnames[0].index('20')
    14  #ymdh=np.array([int(i[idx:idx+10]) for i in fnames],dtype=int)
    15  #if len(ymdh)!=len(fnames):sys.exit('wrong length in ymdh')
    16
    17  trjs=np.zeros(shape=(len(fnames),20))
    18  tex=10000
    19  n,m=0,0
    20  ymdh=[]
    21  for fname in fnames:
    22    try:
    23      df=read_csv(fname+'10.csv')
    24    except:
    25      m=m+1
    26      continue
    27    trjs[n,:10]=[i//tex for i in df.JI3]
    28    trjs[n,10:]=[i%tex for i in df.JI3]
    29    ymdh.append(int(fname[idx:idx+10]))
    30    n+=1
    31  trjs=trjs[:-m,:]
    32  clt = KMeans(n_clusters = nclt)
    33
    34  clt.fit(trjs)
    35  a=clt.labels_
    36  dfa=DataFrame({'lab':a,'ymdh':ymdh})
    37  dfa.set_index('lab').to_csv('lab.csv')
    38
    39  ji=np.array(clt.cluster_centers_,dtype=int)
    40  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
    41  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    42  nc = netCDF4.Dataset('/nas1/backup/data/cwb/e-service/btraj_WRFnests/tmplateD1_3km.nc','r')
    43  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    44  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    45  for l in range(nclt):
    46    des=['Line'+str(l)+'_'+str(i) for i in range(10)]
    47    df=DataFrame({'TWD97_x':[Xcent+x_mesh[i] for i in ji[l,10:]],'TWD97_y':[Ycent+y_mesh[i] for i in ji[l,:10]],'lab':des,'des':des})
    48    df.set_index('TWD97_x').to_csv('res'+str(l)+'.csv')
    49  os.system('for i in {0..'+str(nclt-1)+'};do cp res$i.csv res${i}L.csv;done')
    50  os.system('for i in {4..'+str(nclt-1)+'};do csv2kml.py -f res$i.csv -g TWD97 -n RL;done')
    51  os.system('for i in {2..3};do csv2kml.py -f res$i.csv -g TWD97 -n HL;done')
    52  os.system('for i in {0..1};do csv2kml.py -f res$i.csv -g TWD97 -n NL;done')
```
## google map繪圖、軌跡命名
由於叢集分析結果為數字，需繪圖後、從google map上軌跡點之說明內容，來定義數字與文字(區域方向)之對照(path.txt)
可以參考筆記(繪製逆軌跡圖流程、csv2kml)


```
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests/kmean_spr
$ cat n_clusters6/path.txt
1SH     5 Shang Hai and northwestern China
2BJ     3 Bei Jing
3SW     1 South Western of stations
4LOCAL  2 Local Circulations
6BH     0 Bo Hai
7SC     4 Southern China
```



## 其他後處理
### acc_prob.py
從軌跡點L.csv檔案，統計網格通過機率，以便進行繪圖
輸入檔案：
     fnames.txt(檔案路徑名稱之listing)
輸出檔案：
     probJ.nc
單位：crossing time/total time

```python
kuang@master /nas1/backup/data/cwb/e-service/btraj_WRFnests
$ cat -n acc_prob.py
     1  import numpy as np
     2  import netCDF4
     3  import os,sys, json
     4  import twd97
     5  from pandas import *
     6  import bisect
     7  import datetime
     8
     9
    10  def dt2jul(dt):
    11    yr=dt.year
    12    deltaT=dt-datetime.datetime(yr,1,1)
    13    deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
    14    return (yr*1000+deltaT.days+1,deltaH*10000)
    15
    16  Latitude_Pole, Longitude_Pole = 23.61000, 120.990
    17  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
    18  os.system('cp ../tmplateD1_27km.nc probJ.nc')
    19  v='O' #v is depend to templates var. names
    20  nc = netCDF4.Dataset('probJ.nc','r+')
    21  nc.XORIG
    22  x_mesh=[nc.XORIG+nc.XCELL*i for i in range(nc.NCOLS)]
    23  y_mesh=[nc.YORIG+nc.YCELL*i for i in range(nc.NROWS)]
    24  #os.system('ls trjj*L.csv > fnames.txt')
    25  with open('fnames.txt', 'r') as f:
    26    fnames=[l.strip('\n') for l in f]
    27  nc.variables[v][0,0,:,:]=np.zeros(shape=(nc.NROWS,nc.NCOLS))
    28  i=fnames[0].index('2')
    29  DATE=fnames[0][i:i+11]
    30  sdate = datetime.datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:10]))
    31  nt,nvars,ndt=nc.variables['TFLAG'].shape
    32  for idt in range(2):
    33    nc.variables['TFLAG'][0,:,idt]=[dt2jul(sdate)[idt] for i in range(nvars)]
    34  ex=int(np.log10(max(nc.NROWS,nc.NCOLS))+1)
    35  tex=10**ex
    36  for fname in fnames:
    37    df=read_csv(fname)
    38    if len(df)==0:continue
    39    x=np.array(df.TWD97_x)-Xcent
    40    y=np.array(df.TWD97_y)-Ycent
    41    ix=[max(0,min(nc.NCOLS-1, bisect.bisect_left(x_mesh,xx)-1)) for xx in x]
    42    iy=[max(0,min(nc.NROWS-1, bisect.bisect_left(y_mesh,yy)-1)) for yy in y]
    43    df['JI']=[j*tex+i for i,j in zip(ix,iy)]
    44    pv=pivot_table(df,index='JI',values='TWD97_x',aggfunc='count').reset_index()
    45    pv.TWD97_x=np.array(pv.TWD97_x)*15./3600./len(fnames) #in unit of hr/total hr in that month
    46    pv['I']=[ji%tex for ji in pv.JI]
    47    pv['J']=[ji//tex for ji in pv.JI]
    48    for i in range(len(pv)):
    49      nc.variables[v][0,0,pv.J[i],pv.I[i]]+=pv.TWD97_x[i]
    50  nc.close()
```


Links
Here：WRF三維軌跡與叢集分析*
