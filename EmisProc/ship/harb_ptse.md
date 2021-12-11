---
layout: default
title: "Elev. PointS for Harbors"
parent: "Marine Sources"
grand_parent: "Emission Processing"
nav_order: 1
date: 2021-12-11 20:06:18              
last_modified_date:   2021-12-11 20:06:24
---

# 港區船舶之點源排放
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
- 港區船舶因屬靜止停靠狀態，其排放型態為典型的點源。因此需要特定的點源參數（`XYHDTV`）,此處參考大型貨櫃輪船的[形狀](https://kknews.cc/news/boq3xeo.html)進行假設：
  - 位置：由VERDI之平面圖（`Tile Plot`）上、配合內政部縣市邊界`shape`檔的海岸線，找到船舶排放在港埠的集中點，網格位置（`IX`, `IY`)_`start from 1`分別為：
    - `IXYfromVerdi=[(26,93),(54,124),(55,124),(67,124),(71,104),(15,75),(63,82),(19,32),(20,31),(15,46)]`
    - `HarbName=['TaiZhong','TaiBeiW','TaiBeiE','JiLong','SuAuo','MaiLiao','HuaLian','KS_W','KS_E','AnPin']`
  - 高度：75M(顯然符合高空點源的定義)
  - 內徑：30M（集束煙道等似內徑）
  - 溫度：100C
  - 流速：10M/S
- 排放量變動
  - 新增點源：`原3公里網格 - 臨近9格平均值`
  - 面源修正為：`臨近9格平均值`
- 船舶總排放量之CAMx格式檔案：由[area_YYMM_NSC.py](https://github.com/sinotec2/TEDS_ship/blob/main/area_YYMM_NSC.py)產生
- 船舶面源\～點源處理考量的理由：[船舶排放之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship)
- [CAMx高空點源排放檔案之轉寫](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/wrtE/)及[wrtE.py](https://github.com/sinotec2/TEDS_PTSE/blob/main/wrtE.py)


## 程式執行
- 程式名稱：[harb_ptse.py](https://github.com/sinotec2/TEDS_ship/blob/main/harb_ptse.py)
- 1個引數
  - 4碼年月
- 如`python harb_ptse.py 1901 `
  - 需要檔案：`fortBE.413_teds11.51A_01.nc`
  - 產生檔案
    - 新增港埠點源排放：`fortBE.413_teds11.HRBE01.nc`
    - 修正後的船舶面源排放：`fortBE.413_teds11.51Ab01.nc`

## 程式設計
- 因台灣港區位置不會更動，直接以程式碼定義。
  - VERDI的空間標籤仍然是`fortran`的習慣，自1開始計數，所以要扣掉以符合`python`的約定方式

```python
    12	P='/'+hmp+'/TEDS/teds11/ship/'
    13	
    14	IXYfromVerdi=[(26,93),(54,124),(55,124),(67,124),(71,104),(15,75),(63,82),(19,32),(20,31),(15,46)]
    15	HarbName=['TaiZhong','TaiBeiW','TaiBeiE','JiLong','SuAuo','MaiLiao','HuaLian','KS_W','KS_E','AnPin']
    16	IYX=[(j-1,i-1) for (i,j) in IXYfromVerdi]
    17	nhb=len(IYX)
```
- 讀取[area_YYMM_NSC.py](https://github.com/sinotec2/TEDS_ship/blob/main/area_YYMM_NSC.py)的結果檔案

```python
    25	fname='fortBE.413_teds11.51A_'+mm+'.nc'
    26	fname1=fname.replace('A_','Ab')
    27	os.system('cp '+fname+' '+fname1)
    28	try:
    29	  nc = netCDF4.Dataset(fname1, 'r+')
    30	except:
    31	  sys.exit(fname1+' not found')
    32	
```
- 重新分配港區點源及面源排放量
  - 點源部分：`hb[:,:,ihb]=var[:,:,yx[0],yx[1]]-base[:,:]`
  - 面源部分：`nc.variables[v][:,0,yx[0],yx[1]]=base[iv,:]`
```python
    52	hb=np.zeros(shape=(nv,nt,nhb))
    53	for yx in IYX:
    54	  ihb=IYX.index(yx)
    55	  neibi=[]
    56	  for j in range(yx[0]-1, yx[0]+2):
    57	    for i in range(yx[1]-1, yx[1]+2):
    58	      if (j,i) in IYX:continue
    59	      neibi.append((j,i))
    60	  nnb=len(neibi)
    61	  b=np.array(neibi).flatten().reshape(nnb,2)
    62	  base=np.mean(var[:,:,b[:,0],b[:,1]],axis=2)
    63	  hb[:,:,ihb]=var[:,:,yx[0],yx[1]]-base[:,:]
    64	#modified the ground level emission
    65	  for v in V[3]:
    66	    iv=V[3].index(v)
    67	    nc.variables[v][:,0,yx[0],yx[1]]=base[iv,:]
    68	nc.close()
```
- 產生煙囪參數之資料表`pv`
  - 引用[wrtE.py](https://github.com/sinotec2/TEDS_PTSE/blob/main/wrtE.py)寫出CAMx高空點源排放量檔案

```python
   139	pv=DataFrame({
   140	'xcoord':[(i+0.5)*XCELL+XORIG for (j,i) in IYX],
   141	'ycoord':[(j+0.5)*YCELL+YORIG for (j,i) in IYX],
   142	'stkheight':[75. for i in range(nhb)],
   143	'stktemp'  :[100. for i in range(nhb)],
   144	'stkspeed'  :[10. for i in range(nhb)],
   145	'stkdiam'  :[30. for i in range(nhb)],
   146	})
   147	pv['CP_NOb'] = [[bytes(i,encoding='utf-8') for i in j]+[bytes(' ',encoding='utf-8')]*(8-len(j)) for j in HarbName ]
   148	
```

## 檔案下載
- `python`程式：[harb_ptse.py](https://github.com/sinotec2/TEDS_ship/blob/main/harb_ptse.py)。

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1
- 信德海事, **世界上最大的那 8 艘超級貨櫃船！**, [每日頭條](https://kknews.cc/news/boq3xeo.html), 2017-05-22
- `area_YYMM.py`程式說明：[面源資料庫轉CAMx排放nc檔](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/)