---
layout: default
title: "EPs Emis for CAMx"
parent: "Point Sources"
grand_parent: "Emission Processing"
nav_order: 3
date:               
last_modified_date:   2021-12-06 12:09:47
---

# CAMx高空點源排放檔案之產生
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
- 此處處理TEDS PM/VOCs年排放量之劃分、與時變係數相乘、整併到光化模式網格系統內。
- 高空點源的**時變係數**檔案需先行[展開](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptseE_ONS/)。
- 排放量整體處理原則參見[處理程序總綱](https://sinotec2.github.io/jtd/docs/EmsProc/#處理程序總綱)、針對[點源之處理](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/)及[龐大`.dbf`檔案之讀取](https://sinotec2.github.io/jtd/docs/EmisProc/dbf2csv.py/)，為此處之前處理。程式也會呼叫到[ptse_sub](https://sinotec2.github.io/jtd/docs/EmisProc/ptse/ptse_sub/)中的副程式

## 程式說明

### 排放與CEMS資料檔之讀取及準備

### 輸出結果 

```python
   158  #other sources
   159    fnameO=spe+'_ECP'+str(len(cp))+'_MDH'+str(len(mdh))+'_ONS.bin'
   160    with FortranFile(fnameO, 'w') as f:
   161      f.write_record(cp)
   162      f.write_record(mdh)
   163      f.write_record(ons)
```


## 檔案下載
- `python`程式：[ptseE_ONS.py](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.py)。
- `jupyter-notebook`檔案[ptseE_ONS.ipynb](https://raw.githubusercontent.com/sinotec2/jtd/main/docs/EmisProc/ptse/ptseE_ONS.ipynb)

## Reference
