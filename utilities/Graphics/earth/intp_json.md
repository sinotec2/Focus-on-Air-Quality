---
layout: default
title:  時間內插取代初始小時濃度
parent: earth
grand_parent: Graphics
last_modified_date: 2022-10-04 12:07:13
tags: graphics earth
---

# 時間內插取代初始小時濃度
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
- 初始時間[earth](http://125.229.149.182:8085/)的突兀情形，在[cmaq_json3.py][join_nc]有經常性作業的修正方式。此處針對過去、或未正常作業(好幾天停機狀況)的結果，提供獨立的修正程式工具，以備不時之需。
- 最嚴重的情況發生在臺灣地區5:00 ~ 8:00(LST)的模擬結果([http://125.229.149.182:8085/](http://125.229.149.182:8085/)@iMacKuang[^2])

## 程式設計
### 程式I/O
- pwd：程式會讀作業所在目錄，從中解讀網格的解析度，作為IO檔名的一部分
- 引數：需指定要更改的日期、CMAQ起始日(BEGD=YYYY-MM-DD)。該日0時數據將會被修改覆蓋。
- 前後3小時濃度json檔案：如前3小時無值，將會跳出迴圈不執行。
- 檔案名稱管理
  1. 以`dirs`、`hhs`等2個序列分別管理日期及時間訊息。
  1. 以`sp`迴圈依序處理8種污染項目

### 前後時間之平均
- 將前後時間的濃度值讀成`np.array`，以方便進行平均
- 取平均後，還要將結果取成序列，json檔案*不接受* array之形式。

### 程式碼

```python
kuang@DEVP /nas1/Data/javascripts/D3js/earthFcst03/public/data/weather/current
$ cat intp_json.py
#!/opt/anaconda3/envs/py37/bin/python
import numpy as np
import json
import sys, os
import subprocess
import datetime

#the json template
grds=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[5].replace('earthFcst','')
pwd='/nas1/Data/javascripts/D3js/earthFcst'+grds+'/public/data/weather/current/'
bdate=datetime.datetime.strptime(sys.argv[1],"%Y-%m-%d")
dirs=[(bdate+datetime.timedelta(days=i)).strftime("../%Y/%m/%d/") for i in [-1,0,0]]
hhs =[(bdate+datetime.timedelta(hours=i)).strftime("%H00") for i in [-3,3,0]]

for sp in ['no2','ozone','ozone8','pm1','pm10','pm25','so2','vocs']:
  arr=[]
  skip=0
  for id in [0,1]:
    fname=pwd+dirs[id]+hhs[id]+'-'+sp+'-surface-level-fcst-'+grds+'.json'
    if not os.path.isfile(fname):
      print('file '+fname+' not found!')
      skip=1
      break
    with open(fname,'r') as f:
      gfs=json.load(f)
    arr.append(np.array(gfs[0]['data']))
  if skip==1:continue
  fnameO=pwd+dirs[2]+hhs[2]+'-'+sp+'-surface-level-fcst-'+grds+'.json'
  with open(fnameO,'r') as f:
    gfs=json.load(f)
  gfs[0]['data']=list((arr[0]+arr[1])/2.)
  with open(fnameO,'w') as f:
    json.dump(gfs,f)
```
[join_nc]: <https://sinotec2.github.io/FAQ/2022/09/15/join_nc.html> "初始時段濃度模擬結果之均勻化"

[^2]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.
