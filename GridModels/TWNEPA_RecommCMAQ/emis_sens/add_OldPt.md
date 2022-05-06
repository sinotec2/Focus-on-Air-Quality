---
layout: default
title: 既有點源檔案
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 3
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 既有點源檔案
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
- 基於點源在公版模式排放檔案中已被網格均化，除非是大型污染源獨佔網格空間，否則難以由背景其他污染源當中切割出來。
- 此處範例以臺中電廠燃煤機組為例，該廠坐落臺中市西南角，燃煤機組排放高度達250m，周圍沒有其他污染源。

## 直接選取TEDS11點源資料庫
- 這個(台中電廠燃煤機組為例)方案較前述[新增點源增量方案](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/TWNEPA_RecommCMAQ/emis_sens/add_NewPt/#程式碼)單純一些，程式碼控制在100行之內

### [add_tzpp.py]()
- TEDS11資料庫(有管制編號CP_NO)：/nas1/cmaqruns/2019base/data/ptse/twn/目錄下之fortBE.413_teds11.ptse01.nc(CAMx nc file)
  - 按照管制編號及煙囪高度2個變數來搜尋資料庫
- 常數與時變量檔案模版：目錄下之teds11.1901.timvar.nc、及teds11.1901.const.nc
- 變量檔
  - 公版的啟動時間(0:ibeg、前月25日至月底)較長，需要填入暫用值。
  - 回存時又遇到[多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)議題
- 常數檔
  - (YLOCA, XLOCA)、(ROW, COL)需要以新的座標系統校正

```python
kuang@DEVP /nas2/cmaq2019/download/input/201901/grid03/smoke
$ cat add_tzpp.py
...
var=np.zeros(shape=(nv,nt,nlay,l_tzpp,ncol))
for v in V[3]:
  var4=nc0[v][:]
  iv=V[3].index(v)
  var[iv,:,:,:,:]=var4[:,:,tzpp.index,:]
...
for v in V[3]:
  iv=V[3].index(v)
  nc[v][:ibeg,:,:,:]=var[iv,:ibeg,:,:,:]
  nc[v][ibeg:nt0,:,:,:]=var[iv,:(nt0-ibeg),:,:,:]
...  
```

