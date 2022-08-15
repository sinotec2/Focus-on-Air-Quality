---
layout: default
title: 大氣污染情報網站圖面之下載
parent: Regional AQ Data
grand_parent: AQ Data Analysis
last_modified_date: 2022-02-08 13:46:05
---

# 日本大氣污染情報網站圖面之下載
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
- [大氣污染情報網站](https://pm25.jp/)是公益性質的日文網站，彙集了東亞地區實時觀測(數據)與PM<sub>2.5</sub>模式一週預報(8個等級)。
  - 預報模式為[SPRINTARS](https://sprintars.riam.kyushu-u.ac.jp/)(Spectral Radiation-Transport Model for Aerosol Species)。該模式研究受到2013年度*日本気象学会賞*之殊榮。
- 由於該網站公開其模擬結果圖面，可經由定期執行的wget程式下載後進行圖檔解讀，校正成濃度值。

## 腳本程式說明
### pm25.cs
- 此程式負責每天的下載作業
  - 日期：由`date  --rfc-3339='date'`指令獲取
  - 下載：由wget負責
  - png檔案名稱及位址：由網頁內容拮取

```bash
kuang@master /home/backup/data/pm25.jp_yosoku_parts_casu
$ cat pm25.cs
#this script will be executed every day at 8:00am to download the pngs from pm25.jp
ROOT='/home/backup/data/pm25.jp_yosoku_parts_casu'
ymd=`date  --rfc-3339='date'`
yy=`echo $ymd|cut -d'-' -f1|cut -c3-4`
mm=`echo $ymd|cut -d'-' -f2`
dd=`echo $ymd|cut -d'-' -f3`
mkdir -p $ROOT/20$yy/$yy$mm$dd
cd $ROOT/20$yy/$yy$mm$dd
for i in {10..64};do wget https://pm25.jp/yosoku/parts/casu/$yy$mm$dd/$i.png;done
```

### crontab set-up
- 設定每天8時進行下載

```bash
$ grep pm /etc/crontab
  0  8  *  *  * kuang /home/backup/data/pm25.jp_yosoku_parts_casu/pm25.cs
```

### Post Processing
- 製作GIF檔
  - 使用imageMagicK的[convert](https://imagemagick.org/script/convert.php)來做串流

```bash
convert *png pm25.gif
```

- 由圖面顏色讀取濃度值
  - 詳[rdpng.py]()

## Results
- [2018/04/01大陸砂塵暴襲臺期間PM<sub>2.5</sub>之預報GIF](http://125.229.149.182/soong/pm25.jp.gif)

| ![2018040615_pm25jp.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/2018040615_pm25jp.png) |
|:--:|
| <b>圖 2018/04/06大陸砂塵暴PM<sub>2.5</sub>之預報(SPRINTARS)</b>|

## Reference
