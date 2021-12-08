---
layout: default
title: "TimVar for Ground PTS"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 5
date:               
last_modified_date:   2021-12-06 12:09:47
---

# 地面點源之時變係數
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
- 與高空點源的**時變係數**類似，地面點源也是依據CEMS數據，然而同一工廠無數據、鄰近工業區其他廠無數據者，亦會參考CEMS設定其**時變係數**。重要差異：
  - 因第一層的點源不可能正好有CEMS數據，其時變係數全為0/1之整數，有別於高空點源。
  - 因此分開處理將會大幅降低檔案的大小。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/Focus-on-Air-Quality/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptse_sub/)中的副程式

## 程式說明

### 程式執行
因排放物質類別與污染源製造程序的特徵有關，必須分開個別處理，此處則以個別污染項目執行`ptseG_ONS.py`，執行方式如下：

```bash
for spe in NMHC SNCP;do python ptseG_ONS.py $spe;done
```

- 由於程式消耗記憶體非常大量，如要同時進行，需注意記憶體的使用情形。
- 污染源個數與排放高度限值的設定、地面PM排放條件之給定、以及數據年代等等都有關係，需配套紀錄。


### 程式差異
`diff ptseG_ONS.py ptseE_ONS.py`
- 對切分高度的作法，還包括所有煙道編號不是以`P`起頭的所有污染源

```python
< boo=(df.HEI<Hs) | (df.NO_S.map(lambda x:x[0]!='P'))
< df=df.loc[boo].reset_index(drop=True)
---
> df=df.loc[(df.HEI>=Hs) & (df.NO_S.map(lambda x:x[0]=='P'))].reset_index(drop=True)
```
- 高空源是每污染物逐項執行，地面是`NMHC`和`SNCP`2項。

```python
109,112c106,107
< boo1=df.NMHC_EMI>0
< boo2=(df.SOX_EMI+df.NOX_EMI+df.CO_EMI+df.PM_EMI)>0
< BLS={'NMHC':boo1,'SNCP':boo2}
< lsp={'NMHC':['NMHC_EMI'],'SNCP':'SOX_EMI,NOX_EMI,CO_EMI,PM_EMI'.split(',')}
---
> c2v={'NMHC':'PM','SOX':'SOX','NOX':'NOX','PM':'PM','CO':'NOX'} #point.csv vs cems.csv
> BLS={c:df[c+'_EMI']>0 for c in c2v}
```
- 地面源沒有`CEMS`，因此**時變係數**為整數(`0`或`1`)

```python
127c122
<   ons=np.zeros(shape=(len(cp),len(mdh)),dtype=int)
---
>   ons=np.zeros(shape=(len(cp),nMDH))#,dtype=int)
```
- 結果檔名也有點不一樣

```python
161c159
<   fnameO=spe+'_CP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
---
>   fnameO=spe+'_ECP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
```

## 檔案下載
- `python`程式：[ptseG_ONS.py](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseG_ONS.py)。


## Reference
