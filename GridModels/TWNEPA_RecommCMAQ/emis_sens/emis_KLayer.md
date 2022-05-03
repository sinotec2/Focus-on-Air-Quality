---
layout: default
title: 高層排放量敏感性分析
parent: 背景及增量排放量
grand_parent: Recommend System
nav_order: 5
has_children: true
date: 2022-04-18 09:28:55
last_modified_date: 2022-05-02 15:44:10
---

# 高層排放量敏感性分析
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
- 點源簡化以高空網格型式輸入是公版背景基準排放量特色之一。
  - 由於單一點源年排放量可能有千噸以上，為各界所關注，此一作法會造成什麼樣的效果值得探討。

### 各層排放量分布
- 取全月時間之平均值、單位：gmole/s(gas)、g/s(particle)
- 切割各層檔案、再取最大值

```bash
nc=cmaq_cb06r3_ae7_aq.01-20181225.38.TW3-d4.BaseEms.ncf0-8
tmNC $nc
nc=${nc}T
for k in {0..8};do ncks -O -d LAY,$k $nc ${nc}.$k;done
for k in {0..8};do 
  echo $k $(mxNC ${nc}.$k|grep PMOTHR|awkk 2) \
  $(mxNC ${nc}.$k|grep PEC|awkk 2) \
  $(mxNC ${nc}.$k|grep PSO4|awkk 2) \
  $(mxNC ${nc}.$k|grep POC|awkk 2)
done
```

- 原生性粒狀物各層月均值排放量中之最大值
  - 這些項目的最大值遠較其他粒狀物為高 

|K|PMOTHR|PEC|PSO4|POC|
|---|---|---|---|---|
|0|7.575|1.311|2.932|1.983|
|1|4.108|0.372|0.549|0.28|
|2|5.288|4.364|0.789|0.99|
|3|4.315|1.950|0.666|0.444|
|4|5.235|0.383|0.912|0.28|
|5|0.238|0.017|0.04|0.01|
|6|0.009|0.000|0.000|0.000|
|7|0.001|0.000|0.000|0.0001|

### 第二層(K1)排放造成的地面污染增量
- 氣象條件：201901～31
- K1高度：地面以上39.7\~79.55m約40m厚度
- 

| ![SO2K1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/SO2K1.png) |![PM25K1.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/PM25K1.png) |
|:--:|:--:|
| <b>公版K1排放量造成SO<sub>2</sub>濃度增量(月均值)</b>|<b>公版K1排放量造成PM<sub>25</sub>濃度(月均值)</b>|

