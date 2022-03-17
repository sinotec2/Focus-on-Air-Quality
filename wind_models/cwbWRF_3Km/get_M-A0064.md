---
layout: default
title: "中央氣象局WRF_3Km數值預報產品之下載"
parent: "cwb WRF_3Km"
grand_parent: "wind models"
nav_order: 1
date:               
last_modified_date:   2021-11-30 10:43:16
---

# 中央氣象局WRF_3Km數值預報產品之下載

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
- 續[樓上](/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/)的討論，此處進一步說明下載細節。
- 目前為止CWB是要求會員登錄的，登入後方能瀏覽檔案網址，經網址定位與確認後，實際自動下載時(如用`wget`)反而不必帳密。
  - 其會員帳號為電子郵件、密碼須包括大小寫、數字、特殊字元（`shift 1～0`）
- 檔案網址的資訊，寫在`xml`檔案內容內，範例如下：
  - 2021/10/12前舊址：
    - `https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A006${dom}-0$i.grb2`
  - 新址：
    - `https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MIC/M-A006${dom}-0$i.grb2`
    - 舊版`wget`(1.12)會需要加上選項`--no-check-certificate`
- 檔案為逐6小時，按小時分檔儲存。
  - 自0時開始計算，直到第84小時(3天半)
  - 因`macOS`對數字與文字的檢核較為嚴格，`for`迴圈的設法有些差異

## centos的下載程式
- `for`使用`range`的寫法，分別為`{起..迄..間隔}`。

```bash
    for i in {00..84..6};do
      hour=`printf "%02d" $i`
      echo "### DOWNLOADING DATA FOR FORECAST HOUR "${hour}" ###"
      if ! [ -e M-A0061-0$i.grb2 ];then
        wget -q --no-check-certificate https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MIC/M-A0061-0$i.grb2
      fi
      if ! [ -e M-A0064-0$i.grb2 ];then
        wget -q --no-check-certificate https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MIC/M-A0064-0$i.grb2
      fi
    done
```

## macOS的下載程式
- 前2行的語言設定(`LANG`、`LC_ALL`)是因應新`python(3.9)`的檢核
- `for`完全採數字的寫法，再使用`printf`將數字改成文字

```bash
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
today=$(date +%Y%m%d)
rundate=$(date -v-1d -j -f "%Y%m%d" "$today" +%Y%m%d)
yr=$(date -v-1d -j -f "%Y%m%d" "$today" +%Y)
pth=/Users/Data/cwb/WRF_3Km/$yr/${rundate}
mkdir -p $pth

WGET=/usr/local/bin/wget
cd $pth
for ((d=0;d<=84;d+=6));do
  i=`printf "%02d" $d`
  echo "### DOWNLOADING DATA FOR FORECAST HOUR "${i}" ###"
  for dom in 1 4;do
  if ! [ -f M-A006${dom}-0$i.grb2 ];then
#    $WGET -q https://opendata.cwb.gov.tw/fileapi/opendata/MIC/M-A006${dom}-0$i.grb2
    $WGET -q https://cwbopendata.s3.ap-northeast-1.amazonaws.com/MIC/M-A006${dom}-0$i.grb2
  fi
  done
done
```

## 日期的計算
CWB每日的檔案名稱都一樣，因此儲存時必須要加以命名，涉及日期的計算。就此，`macOS`和`centos`的指令是不同的：
- `centos`的指令是將增減時間放在引數的後面。
- `macOS`則是在引數日期之前，進行時間的加、減。
```bash
$ diff get_M-A0064.cs ~/mac/Data/cwb/WRF_3Km/get_M-A0064.cs
4,6c4,6
< rundate=$(date -ud "${today}-1days" +"%Y%m%d")
< yr=$(date -ud "$today" +%Y)
< pth=/nas1/Data/cwb/WRF_3Km/$yr/${rundate}
---
> rundate=$(date -v-1d -j -f "%Y%m%d" "$today" +%Y%m%d)
> yr=$(date -v-1d -j -f "%Y%m%d" "$today" +%Y)
> pth=/Users/Data/cwb/WRF_3Km/$yr/${rundate}
```

## 自動下載排程
- 設定每天0時30分開始下載
```bash
kuang@MiniWei /Users/Data/cwb/WRF_3Km
$ crontab -l|grep 3Km
30 0  *  *  *   /Users/Data/cwb/WRF_3Km/get_M-A0064.cs &> /Users/Data/cwb/WRF_3Km/get_M-A0064.out 2>&1
```

## 檢核

### 個數與大小
- 檔案個數大小：每層共**15個檔**(84/6+1)，3Km檔案共約**2.8G**，15Km檔案共約**0.8G**。
```bash
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ ls M-A0064-0??.grb2|wc -l
      15
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ du -ach M-A0064-0??.grb2|tail -n1
2.8G    total
kuang@MiniWei /Users/Data/cwb/WRF_3Km/2021/20211129
$ du -ach M-A0061-0??.grb2|tail -n1
878M    total
```

### 轉成`nc`檔案
- `wgrib2`：`wgrib2 xx.grb2 –netcdf xx.nc`，參[blog.csdn](https://blog.csdn.net/jiangshuanshuan/article/details/93466122)。
- `ncl_convert2nc`：先啟動`ncl_stable`環境
```bash
source ~/conda_ini ncl_stable
for I in $(ls *.grib2);do ncl_convert2nc $i;done
```

## 批次腳本
整體下載、轉檔、提取近地面風等作業可以詳見[github](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/wind_models/cwbWRF_3Km/get_M-A0064.cs_txt)的腳本原始碼

## Reference
