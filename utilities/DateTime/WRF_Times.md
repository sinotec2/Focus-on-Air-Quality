---
layout: default
title:  WRF的時間標籤
parent: Dates and Times
grand_parent: Utilities
last_modified_date:   2021-12-28 21:21:21
---
# WRF的時間標籤
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
## nc bytes to datetime
- `wrfout`的時間標籤變數名稱為`Times`， 為時間及**12**個`byte`的2維序列，內容為`%Y-%m-%d_%H:00:00`
  - 因標籤不是單純的整數，而是含有減號及冒號的字串，在netCDF檔案內要儲存字串，必須是`byte`形式才能儲存。  
- 因此須先轉成**12**個字元的序列，以`decode`指令逐一進行轉換。
- 再將序列串成字串，以`join()`一個序列來整併。
- 此時才能讀成`datetime`，轉成所要的格式。
  - 字串讀成datetime須使用`.strptime()`函數，引數為字串及格式定義
  - datetime轉出格式以`strftime()`函數為之，引數為格式定義
  - python datime模組的格式，約定為一般date指令定義[格式](https://kknews.cc/zh-tw/code/2lr2ey9.html)的方式。
  - 輸出格式須視後續軟體的需求。

```python
strT=[''.join([i.decode('utf-8') for i in nc.variables['Times'][t,:]]) for t in range(nt)]
Times=[datetime.datetime.strptime(a,'%Y-%m-%d_%H:00:00') for a in strT]
tflag=[i.strftime('%Y%m%d%H') for i in Times]
```

## datetime to nc bytes
- 在儲存wrfout檔案時，則需反向操作，如以下範例
  1. 先產生一個空白序列的容器`b`、將發展成時間及byte數的2維矩陣，未來每個單元長度為12個bytes。
  1. 進行迴圈處理每一個時間的標籤
  1. 將datetime輸出成`%Y-%m-%d_%H:00:00`格式的字串，字串長度為12
  1. 字串每個字元轉成`byte`形式（`encode`），存在`b`容器中
  1. 容器裝滿後一次倒入nc檔案中
  
```python
b=[t for t in range(0,tmax)]
for t in range(0,tmax):
  time=beg_time+datetime.timedelta(days=t/24.)
  b[t]=np.array([bytes(i,encoding='utf-8') for i in time.strftime("%Y-%m-%d_%H:%M:%S")])
v='Times'
nc.variables[v][:,:]=[b[t][:] for t in range(tmax)]
```

## Reference
