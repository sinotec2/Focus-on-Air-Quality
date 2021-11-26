---
layout: default
title: "CWB地面自動站數據轉成little_R格式"
parent: "CODiS"
grand_parent: "wind models"
nav_order: 2
date:               
last_modified_date:   2021-11-26 14:11:39
---

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

# CWB地面自動站數據轉成little_R格式

## 背景

### little_R格式
多年以來[little_R](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式是NOAA/NCEP儲存全球地面與高空觀測數據所使用的格式，是一個很長的ASCII檔案，如下列範例：
```bash
kuang@master /home/backup/data/NOAA/NCEP
$ head SRF_ds461.0/2021/SURFACE_OBS:2021111918
            15.70000           -87.50000 78706      get data information here.  SURFACE DATA FROM ??????????? SOURCE    FM-12 SYNOP                                                                                  3.00000         1         0         0         0         0         T         F         F   -888888   -888888      20211119150000 101450.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
 101400.00000      0      3.00000      0    300.39999      0    297.89999      0      1.00000      0      0.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
-777777.00000      0-777777.00000      0      1.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
      1      0      0
            51.50000            -0.10000 03770      get data information here.  SURFACE DATA FROM ??????????? SOURCE    FM-12 SYNOP                                                                                  5.00000         1         0         0         0         0         T         F         F   -888888   -888888      20211119150000-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
-888888.00000      0      5.00000      0    285.10001      0    281.89999      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
-777777.00000      0-777777.00000      0      1.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0-888888.00000      0
      1      0      0
```
由於這些數據是驅動或修正模式模擬的重要依據，本地觀測數據如要併入模式系統，須符合其格式內容。

### 方案檢討
- 過去是以`fortran`[程式](http://200.200.31.47/home/backup/data/NOAA/NCEP/cwb_data/cwbsrf/little_r_srf_v2.f)進行轉檔，因此有必要進行更新，應用`python`的新模組功能[fortranformat](https://pypi.org/project/fortranformat/)進行更簡潔的處理。

## 程式分段說明
- 程式說明
  - 目前只有風速風向有詳細檢核，其他項目(溫、濕度等)的FDDA應有所限制
  - 此處僅增加C0測站，傳統46測站未納入處理，以避免與`fortran`程式結果發生衝突
  - 引進模組。其中ff為`fortran`格式專用模組，可能會需要安裝。
```python
kuang@master /home/backup/data/NOAA/NCEP/cwb_data/cwbsrf
$ cat -n add_srfFF.py
     1  #!/Users/miniconda2/bin/python
     2  """
     3  This program appendding the cwbsrf file from e-service website
     4  The data formats(201~4) are translated from the fortran codes
     5  Only C0**** stations are append, the original 46**** are not changed
     6  The units for temperature, precipitation etc. are not checked, only ws wd may be right
     7  TODO: the condition may be changed to do all the transformation from website csv to cwbsrf files
     8  """
     9  from pandas import *
    10  from datetime import datetime, timedelta
    11  import subprocess
    12  import fortranformat as ff
```
- 定義資料路徑、讀取測站位置等基本資料、篩選出自動站備用(有人站仍以`fortran`程式處理)
```python
    13  root='/home/backup/data'
    14  fname = root+'/cwb/e-service/read_web/stats_tab.csv'
    15  pth = fname.replace('read_web/stats_tab.csv','')
    16  dfS = read_csv(fname)
    17  dfS = dfS.loc[dfS.stno.map(lambda x: x[:2] == 'C0')].reset_index(drop=True)
```
- 測站經緯度、名稱與id40之定義
```python
    18  lat, lon, elev, ns = list(dfS.LAT), list(dfS.LON), list(dfS.SLV_m), len(dfS)
    19  name = stno = list(dfS.stno)
    20  id40 = [' ' + name[r3] + ' get data information here.' + 6 * ' ' for r3 in range(ns)]
    21
```
- 引用`fortran`的格式設定，啟用FF模組
```python
    22  # 201   format(2F20.5,4A40,F20.5,5I10,3L10,2I10,A20,13(F13.5,I7))
    23  # 202   format(10(F13.5,I7))
    24  # 203   format(10(F13.5,I7))
    25  # 204   format(3I7)
    26  fmt201='2F20.5,4A40,F20.5,5I10,3L10,2I10,A20,13(F13.5,I7)'
    27  fmt202='10(F13.5,I7)'
    28  fmt203='10(F13.5,I7)'
    29  fmt204='3I7'
    30  for i in range(1,5):
    31    c='20'+str(i)
    32    exec('w_line'+c+' = ff.FortranRecordWriter(fmt'+c+')')
```
- 將無關的變數設為定值
```python
    33
    34  r135 = -888888.0
    35  sut = -888888
    36  julian = -888888
    37  ceiling = -888888.
    38  qc = 0
    39
```
- 決定要處理的日期
  - `byr`:年度
  - `srf_date`:由既有檔案讀取已處理過的日期
  - `cwb`:已由CODiS網站下載好檔案的日期
  - `fname`:尚需進行轉換的日期
```python
    40  #compare the e-service and current directories to find the dates not processed yet
    41  try:
    42    byr=str(int(subprocess.check_output('pwd',shell=True).split(b'/')[-1].strip(b'\n')))
    43  except:
    44    sys.exit('current dir. must under number of year')
    45
    46  try:
    47    srf=subprocess.check_output('ls cwbsrf*',shell=True).split(b'\n')
    48  except:
    49    srf=[]
    50  srf_date=[(i[7:11]+i[12:14]+i[15:17]).decode('utf8') for i in srf]
    51  cwb=[i.decode('utf8') for i in subprocess.check_output('ls '+pth+byr+'/cwb*.csv',shell=True).split(b'\n') if len(i)>0]
    52  ii=cwb[0].index('.csv')
    53  cwb_date=[i[ii-8:ii] for i in cwb if len(i)>=ii+3]
    54
    55  fnames=[]
    56  for dt in set(cwb_date)-set(srf_date):
    57    try:
    58      idt=int(dt)
    59    except:
    60      continue
    61    fnames.append(cwb[cwb_date.index(dt)])
    62  if len(fnames)==0:sys.exit('file check OK, no need to convert')
    63
    64  fnames.sort()
```
- 逐日讀取所有自動站數據  
```python
    65  for fname in fnames[:]:
    66    ymd = DATE = fname[ii-8:ii]
    67    DATE += '00'
    68    bdate = datetime(int(DATE[:4]), int(DATE[4:6]), int(DATE[6:8]), int(DATE[8:]))
    69    try:
    70      df = read_csv(fname)#,encoding='utf8')
    71    except:
    72      continue
    73    print(fname)
    74    df.drop_duplicates(inplace=True)
    75    df['stno'] = [i[:6] for i in df.stno_name]
    76    df = df.loc[df.stno_name.map(lambda x: x[:2] in ['46', 'C0'])].reset_index(drop=True)
    77    df.ObsTime = [int(i) for i in df.ObsTime]
```
- 逐時進行處理
  - 篩選出符合之時間
  - 篩選出無數據之測站(miss)，並加回資料庫、填入無效值，以符合測站數  
```python
    78    for it in range(24):
    79      ymdh = int(ymd) * 100 + it + 1
    80      dfd = df.loc[df['ObsTime'].map(lambda x: x == ymdh)].reset_index(drop=True)
    81      if len(dfd) ==0:continue
    82      if len(dfd) < ns:
    83        ns2 = set(dfd.stno)
    84        miss = set(stno) - set(ns2)
    85        for m in miss:
    86          df2 = DataFrame({'stno_name':[m],'ObsTime':[ymdh]})
    87          dfd = dfd.append(df2,ignore_index=True,sort=False)
    88      dfd = dfd.sort_values('stno_name').reset_index(drop=True)
    89      dfd = dfd.fillna(-888888.0)
```
- 變數名稱之對照、計算utc時間、定義輸出檔名
```python
    90      slp, precip, cloud_cvr, = list(dfd.SeaPres), list(dfd.Precp), list(dfd['Cloud Amount'])
    91      pressure, temp, dew = list(dfd.StnPres), list(dfd.Temperature), list(dfd['Td dew point'])
    92      ws, wd, rh = list(dfd.WS), list(dfd.WD), list(dfd.RH)
    93      pdate = bdate + timedelta(hours=it+1)
    94      udate = pdate - timedelta(hours=8)
    95      UTC = udate.strftime('%Y-%m-%d_%H')
    96      UTC2 = udate.strftime('%Y%m%d%H') + '0000'
    97      srf_fname = 'cwbsrf:' + UTC
```
- 寫出結果
```python
    98      with open(srf_fname, 'a') as srf:
    99        for r3 in range(ns):
   100          if ws[r3] <0:continue
   101          srf.write(w_line201.write(
   102                  [lat[r3], lon[r3], id40[r3], name[r3], 'platform', \
   103                      'TW CWB SRF', elev[r3], 1, 0, 0, 0, 0, 1, 0, 0, sut, julian, UTC2,\
   104                                          slp[r3], qc]+4*[r135, qc]+[precip[r3], qc]+ \
   105                      5*[r135, qc]+[cloud_cvr[r3], qc, ceiling, qc])+'\n')
   106          srf.write(w_line202.write([pressure[r3],qc,elev[r3],qc,temp[r3],qc,dew[r3],qc, \
   107                      ws[r3],qc,wd[r3],qc,r135,qc,r135,qc,rh[r3],qc,r135,qc])+'\n')
   108          srf.write(w_line203.write(2*[-777777.0,qc]+8*[r135,qc])+'\n')
   109          srf.write(w_line204.write([1,0,0])+'\n')
```

## 程式原始碼
可以在公司內部網站找到:
- `fortran`[程式](http://200.200.31.47/home/backup/data/NOAA/NCEP/cwb_data/cwbsrf/little_r_srf_v2.f)
- `python`[程式](http://200.200.31.47/home/backup/data/NOAA/NCEP/cwb_data/cwbsrf/add_srfFF.py)

## Reference
- MM5/WRF之[little_r](https://www2.mmm.ucar.edu/wrf/users/wrfda/OnlineTutorial/Help/littler.html)格式
- Brendan Arnold, **FORTRAN format interpreter for Python**, [fortranformat 1.0.1](https://pypi.org/project/fortranformat/), Released: Apr 6, 2021

