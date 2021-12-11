---
layout: default
title: "AreaS for Selected NSC"
parent: "Marine Sources"
grand_parent: "Emission Processing"
nav_order: 1
date:               
last_modified_date:   2021-12-10 17:43:45
---

# 特定面源類別之CAMx排放檔
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
- 因應船舶排放之處理，將原有之[area_YYMM.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/)加設篩選條件，只針對特定類別進行處理轉寫。
- 將[環保署資料庫](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx)進行排放類別(`NSC`)之篩選，其餘程序完全與[area_YYMM.py](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/)一樣。

## 程式執行
- 程式名稱：[area_YYMM_NSC.py](https://github.com/sinotec2/TEDS_ship/blob/main/area_YYMM_NSC.py)
- 2個引數
  - 4碼年月
  - `NSC`單一值或序列
- 如`python area_YYMM_NSC.py 1901 51A,51B,51C,51D`

## 程式差異
- 讀取引數中的類別。如有多項類別，如船舶有4類船隻種類，則以逗號區隔(`51A,51B,51C,51D`)。

```python
$ diff area_YYMM_NSC.py  ../area/area_YYMM.py
102,105c102
< try:
<   NSCi=sys.argv[2].split(',')
< except:
<   NSCi=[sys.argv[2]]
---
>
```
- 結果檔名`area`換成第1個`NSC`名稱

```python
113c110
< fname='fortBE.413_teds'+teds+'.'+NSCi[0]+'_'+mm+'.nc'
---
> fname='fortBE.413_teds'+teds+'.area'+mm+'.nc'
```
- 針對輸入資料庫檔案進行篩選，只處理指定之`NSC`。

```python
213d209
< df=df.loc[df.nsc2.map(lambda x: x in NSCi)].reset_index(drop=True)
```

## 檔案下載
- `python`程式：[area_YYMM_NSC.py](https://github.com/sinotec2/TEDS_ship/blob/main/area_YYMM_NSC.py)。

## Reference
- 行政院環保署, **空氣污染排放清冊**, [air.epa.gov](https://air.epa.gov.tw/EnvTopics/AirQuality_6.aspx), 網站更新日期：2021-12-1
- `area_YYMM.py`程式說明：[面源資料庫轉CAMx排放nc檔](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/area/area_YYMMinc/)