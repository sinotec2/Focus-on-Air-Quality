---
layout: default
title:  Download Hiway Forecasting Data
parent: Crawlers
grand_parent: Utilities
has_children: true
last_modified_date: 2023-06-07 16:17:56
permalink: /utilities/Crawlers/tp_future
tags: Crawlers tp_future
---

# 高公局車行時間預測數據之批次下載
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

- 高速公路局對外提供未來任意日時、10條路線、共228個匝道出入口作為起、起端之行車時間預測([高速公路1968](https://1968.freeway.gov.tw/tp_future))。
- 該預測時間與路況相關，具有未來交通量之參考依據。唯數據並未提供批次下載，須一一選單後執行「立即規劃行程」，方能得知。
- 此處以selenium(4.9.1版)與BeautifulSoup(4.12.2版)作為下載與解析之模組，並將結果存成csv檔案。
- 程式見於[github][tp_future]

## 程式說明

### geckodriver之預備

- 由於selenium是靠著Firefox介面來驅動程式，需要有`/usr/bin/geckodriver`檔案，該檔案版本與Firefox的版本有密切關係，須先了解firefox的版本，再行選擇下載，詳見[github/mozilla/geckodriver](https://github.com/mozilla/geckodriver/releases)。
- 本次執行作業使用Firefox為102.11版，因此選用geckodriver 0.31.0版(2022年4月版本)

### 模組相依性

- 使用模組如下。
- 由於selenium的尋找指令(`find_element`)在3版與4版之間有很大的差異。此處使用4版。

```python
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import json
from pandas import DataFrame
from selenium import webdriver
import datetime
import time
import codecs
import numpy as np
```

### 點選相關基本副程式

- 這組沿用以前的程式碼。改成4版2個引數的做法。

```python
def clkid(ID):                                  #click the id
    button_element = driver.find_element("id",ID)
    button_element.click()
    return
def clkpath(ID):                                        #click the xpath (no use)
    button_element = driver.find_element(By.XPATH,ID)
    button_element.click()
    return
def SelectByIDnValue(ID,v):                     #click and select by value
    select = Select(driver.find_element(By.ID,ID))
    select.select_by_index(v)
    return
```

### 主要點選副程式

- 這支為主要點選、輸入、以及執行預測、下載畫面、解讀結果等等動作順序
- 需要引數分別為日、時、高速公路路線序號(1~10)、起訖匝道(序號)
- 佔存html檔約有1.2M。只解讀其中的車行時間預測，共7個時間。

```python
def click_run_save(d,t,w,s1,s2):
    day=datetime.date.today()+datetime.timedelta(days=d)
    clkid("tripFuturePickDate")
    driver.find_element(By.ID,"tripFuturePickDate").clear()
    input_1=driver.find_element(By.ID,"tripFuturePickDate")
    input_1.send_keys(day.strftime("%Y/%m/%d"))
    clkid("tripFuturePickTime")
    SelectByIDnValue("tripFuturePickTime",t)
    clkid("freeway_from")
    SelectByIDnValue("freeway_from",w)
    clkid("section_from")
    SelectByIDnValue("section_from",s1)
    clkid("freeway_from")
    SelectByIDnValue("freeway_end",w)
    clkid("section_from")
    SelectByIDnValue("section_end",s2)
    clkpath('//button[@class="button_primary tripplan_btn"]')
    if abs(s1-s2) >10:time.sleep(5)
    n = os.path.join("/nas2/kuang/tp_future", "results.html")
    f = codecs.open(n, "w", "utf−8")
    h = driver.page_source
    f.write(h)
    fn=open('results.html','r')
    soup = BeautifulSoup(fn,'html.parser')
    span=[str(i) for i in list(soup.find_all('span'))]
    lags=[i.split('約')[1].split('分')[0]+'分' for i in span if '約' in i]
    return lags
```

## 主程式

### firefox之驅動

```python
driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
driver.get("https://1968.freeway.gov.tw/tp_future")
```

### 停等的爬蟲

- 這裡因為副程式使用了`Select.select_by_index`，按照序號選擇，雖然程式較為簡潔，但是後續還是需要另外建立對照關係，以連結到實際的世界。
- 停等的必要性，需要特別說明一下。
  - 若不停等，網頁在輸出成果、更新畫面之前或同時，程式可能就會往下走，造成讀不到結果的情況。
  - 如沒有停等、短時間內大量流量，網站管理者會認為是駭客攻擊，而將本地網址列入黑名單被防火牆遮蔽住。經測試，至少要經過1小時，防火牆才會慢慢打開。
- 程式設計了3種的停等
  1. 副程式內之停等：當2站差距較大時，遠端系統需要一些時間計算出報表，此處停等5秒鐘。(`if abs(s1-s2) >10:time.sleep(5)`)
  2. 相鄰2匝道計算之間，停等1秒鐘(`time.sleep(1)`)。
  3. 迴圈之間，4～30秒之間取隨機值停等(`time.sleep(np.random.randint(low=5,high=30))`)。以規避對方防火牆的分析。

### 迴圈下載


```python
SegOfWay={1:84,2:12,3:7,4:84,5:4,6:8,7:7,8:8,9:6,10:8}
#'1_0': '國道1號', 'N1H_0': '國1高架', '2_0': '國道2號',
# '3_0': '國道3號', 'N3A_0': '國道3甲', '4_0': '國道4號',
# '5_0': '國道5號', '6_0': '國道6號', '8_0': '國道8號', '10_0': '國道10號',

col=['date','hr','highway','segment1','segment2']
col+=['t'+str(i) for i in range(1,8)]
df=DataFrame({i:[] for i in col})
d0=DataFrame({i:[0] for i in col})
d0.set_index('date').to_csv('tp_future.csv')
i=0
for d in range(1,2):
  for t in range(1,49):
    for w in range(1,11):
      for s1 in range(SegOfWay[w]-1):
        s2=s1+1
        lags=click_run_save(d,t,w,s1,s2)
        df.loc[i,'date']=d
        df.iloc[i,1:]=[t,w,s1,s2]+lags
        d0.iloc[0,:]=[d,t,w,s1,s2]+lags
        i+=1
        time.sleep(1)

        lags=click_run_save(d,t,w,s2,s1)
        df.loc[i,'date']=d
        df.iloc[i,1:]=[t,w,s2,s1]+lags
        d0.iloc[0,:]=[d,t,w,s2,s1]+lags
        i+=1
        d0.set_index('date').to_csv('tp_future.csv',header=None,mode='a')
        time.sleep(np.random.randint(low=5,high=30))
```

### 結果之儲存

- 可能因為各種原因造成網路斷線而無法下載，完整下載後再進行儲存，似乎不切實際。
- 此處使用`pandas.DataFrame.to_csv`函數中`append`功能，將每次最內迴圈結束後就將結果儲存起來。
- 由於每次`append`都會出現表頭，此處先寫一空白行，正式寫入時再取消輸出表頭即可。

```python
d0.set_index('date').to_csv('tp_future.csv')
...
        d0.set_index('date').to_csv('tp_future.csv',header=None,mode='a')
```

## 程式下載

{% include download.html content="高公局車行時間預測數據之批次下載[tp_future.py][tp_future]" %}

[tp_future]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Crawlers/tp_future/tp_future.py "高公局車行時間預測數據之批次下載程式"