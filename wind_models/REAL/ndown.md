---
layout: default
title: ndown
parent: REAL & WRF
grand_parent: WRF
nav_order: 3
date: 2022-02-19 17:56:16               
last_modified_date: 2022-12-01 14:34:15
---

# ndown

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

- 除了雙向巢狀網格的模擬方式，[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)當然也可以接受循序、單向之巢狀網格模擬，亦即將上層母網格結果，作為下層子網格的初始即邊界條件，所使用的讀取程式，即為[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)。
- 適合單向巢狀網格模擬方式的條件狀況
	- 次網格範圍較小、獨立、不會造成上次網格明顯的差異
	- 開啟FDDA，模擬不會與觀測有太大的偏差
	- 雙向巢狀網格太過耗費計算資源，無法進行
	- 需要時間間距較密的wrfbdy檔案
- 中文筆記可以參考[博客園](https://www.cnblogs.com/jiangleads/articles/12825970.html)
- 注意事項
	1. coarse-to-fine grid ratio is only restricted to be an integer. An integer less than or equal to 5 is recommended
	1. 一次只能讀一層的wrfout，產生下一層domain所需的IC/BC

## namelist.input 修改重點

- 執行雙向巢狀網格的[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)、上層單層的[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)之後。將namelist.input進行備份、修改。
- &time_control下
	1. interval_seconds = 21600 → 3600。這個值是邊界檔的時間間距，原來最外層的邊界檔只有每6小時1筆(配合FNL)。如果沒有FDDA則是按照wrfout的結果：每小時1筆。
	1. 新增io_form_auxinput2 = 2
- &domains
	- max_dom=1 → 2。執行2層網格，上層為剛剛結束[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)的母網格、下層為則需要wrfbdy的子網格
	- e_we、e_sn、dx、dy、(不動)保持母、子網格的設定與執行[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)時一樣
	- time_step = 240  → 80 。時間步階適度調整(保持dt/dx<6)，以方便子網格wrf之執行。

### 當[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)同時run了超過2層

- [ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)一次只能執行一層，只能將上層移轉第下層，namelist.input只能接受d01及d02，不能接受d03、d04...
- 因此原本的namelist.input必須修改只留存2層，如果要[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)第三層到第四層，必須將第三層命名為**d01**，第四層即為**d02**
- 注意除了網格起始點位置、網格點數之外，也要修改網格間距、time_step等。

## 執行

### 檔案目錄之安排

- 由於每層網格分別執行，檔案名稱將會重疊，為區別其意義，需要另建目錄以資識別。
- 根目錄：
	- 維持以時間、WRF版本等資訊為主。如`/nas1/WRF4.0/WRFv4.2/202208`
	- 執行所有網格系統之real.exe
	- *不*執行wrf.exe，以避免混淆
- 各網格目錄
 	- 以domain name識別。如CWBWRF_45k/、SECN_9k/、TWEPA_3k/
	- 在各網格目錄連結正確的起始與邊界檔執行單層real.exe、wrf.exe、產生新的namelist.input、執行ndown.exe
	- 更換下一層網格目錄疊代執行。

### 執行步驟

- 準備wrfndi_d02：Rename(`mv`) the wrfinput_d02 file to wrfndi_d02
	- wrfinput_d02必須是執行[real.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/doreal_4Nests.sh/)所產生下一層子網格的初始條件。(不能是單層[real]()的wrfinput_d01)
	- 會另外產生一個新的wrfinput_d02，如在同一目錄、原檔會被覆蓋，因此不能用連結。如果原wrfinput_d02(real結果)仍要保留，需另外備份。
- 將母網格wrfout檔案，連結成wrfout_d01檔案(時間標籤必須保持一樣)
- 執行[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)
	- 將產生wrfinput_d02 and wrfbdy_d02 file.
	- 將wrfinput_d02重新命名為wrfinput_d01（準備執行子網格[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/))
		- 將wrfbdy_d02命名為wrfbdy_d01
		- [ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)之後要執行子網格的wrf，也要修改namelist.input。(~.nest4only)注意其他檔案順序，如wrffdda_d04與wrfsfdda_d04等，也必須改成d01
- 執行子網格[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)

## ndown執行腳本範例

- 這個範例是在東南中國(SECN_9k)與台灣本島(TWEPA_3k)之間使用ndown，將前者的逐時模擬結果作為後者的邊界條件。
- 個案時間長度為10天
  - nests3：3個網格系統雙向模擬，每一天會需要電腦時間68分鐘，10天會需要10小時(不可行)。
	- SECN_9k：系東亞及東南中國2層雙向網格(tw_CWBWRF_45k)模擬結果的第2層
  - 3者之met_em在$gfs目錄中完成
- 腳本見於[ndown.cs](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/wind_models/REAL/ndown.cs),分段說明如下

### real之執行

- 參與執行ndown的2層網格，必須先執行雙層的real
  - 使用特殊的模板(namelist.input23_loop)
  - 置換起訖時間
  - 使用met_em檔案也必須置換網格編號
  - 此處的real版本為mpich版本

```bash
i=2
cd $gfs/${DOM[$i]}/ndown
cp namelist.input23_loop namelist.input
  for cmd in "s/SYEA/$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" \
             "s/EYEA/$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g" ;do
    sed -i $cmd namelist.input
  done
for hd in metoa_em wrf;do if compgen -G "${hd}*" > /dev/null; then rm -f ${hd}*;fi;done
for d in 2 3;do
  dd=$(( $d - 1 ))
  for id in {0..10};do
    for j in $(ls ../../met_em.d0${d}.${dates[$id]}_*);do
      k=${j/d0${d}/d0${dd}}
      l=${k/..\/..\//}
      m=${l/met_/metoa_};ln -s $j $m;done;done;done
LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin:/opt/mpich/mpich-3.4.2-icc/lib /opt/mpich/mpich-3.4.2-icc/bin/mpirun ${MPI[$i]} /nas1/WRF4.0/WRFv4.3/WRFV4/main/real.exe >& /dev/null
```

- 注意：
	1. 使用[compgen][compgen]判斷符合特定規則的檔案是否存在，如果有任何符合條件的檔案，將會被刪除。
	2. met_em必須先行準備好

### wrfndi_d02與wrfout之連結

- 前者為real的結果，更名為wrfndi_d02。(原本的wrfinput_d02會被覆蓋)
- 後者為tw_CWBWRF_45k的第2層模擬結果。此處更名為第1層，為ndown的輸入檔案。

```bash
mv wrfinput_d02 wrfndi_d02

for id in {0..10};do ln -sf $gfs/${DOM[3]}/wrfout_d02_${dates[$id]}_00:00:00 wrfout_d01_${dates[$id]}_00:00:00;done
```

### 置換namelist中的時間間距

- 邊界檔(逐時)和FDDA檔(逐3小時)不同，似乎不構成問題
- 逐時值邊界檔顯然對模擬會有較顯著的控制

```bash
sed -i 's/interval_seconds                    = 10800/interval_seconds                    = 3600/g' namelist.input
```

### 執行ndown

```bash
#ndown.exe is intel version
LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/lib/release:/opt/intel/compilers_and_libraries_2020.0.166/linux/mpi/intel64/libfabric/lib /opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/bin/mpirun -np 10 /nas1/WRF4.0/WRFv4.3/WRFV4/main/ndown.exe >& /dev/null
```

### ndown結果應用

- 取代TWEPA_3k範圍的real
- 更新namelist.input後即可執行單層的wrf模擬

```bash
## restore the real and ndown results
cd $gfs/${DOM[$i]}
for f in wrfinput wrfbdy wrffdda wrflowinp;do
  mv ndown/${f}_d02 ${f}_d01
done
```

### 電腦時間檢討

- tw_CWBWRF_45k雙向： ~ 10min computer time/day simulation
- TWEPA_3k單層：~ 9min computer time/day simulation
- 合計：19 min/day << 68 min/day

## ndown and OBS_domain 的比較

- 初期和三天後模擬結果都還算蠻接近的
- ndown結果的規則性與系統性較高，OBSdomain在局部則較為紛亂，
- avrgvsobss-k結果
	- ndown 62.4%,OBSdomain73.0% 
	- 主要因為風速高估比較嚴重。可能原因: 
		1. 缺乏domain外作用力的牽制，sfdda比fdda更差，OBS_DOMAIN又較sfdda更差，d4only又更差，
		1. 調整機制是否有錯!可否直接用EPAst之obs_domain
- Attainment Comparison
 
|Case|Overall Attainment|OB_TMP|GE_TMP| OB_WS|GE_WS|OB_WD|GE_WD|
|-|-|-|-|-|-|-|-|
|obs_domain|73.0%  | 46.6% |  89.7% |  34.5% |  81.0%  | 89.7%  | 96.6%|
|ndown|62.4%  |   48.3%  |  89.7% | 13.8%  | 46.6%  |   79.3%  |   96.6%|

- only nest 4 所需時間(2013/10/08~10共72hr)
	- Oct  6 21:23 namelist.output
	- Oct  8 10:13 wrfout_d01_2013-10-08_00_00_00
- 原4層雙向共37hr50min
- 約2:1。可見約一半的時間在d4的計算

## Reference
- chinagod, **WRF学习之 ch5 WRF模式（三）运行WRF（d, e）：（双向嵌套，单向嵌套）**, [博客园](https://www.cnblogs.com/jiangleads/articles/12825970.html)posted @ 2020-05-04 23:39 

[compgen]: <https://www.linuxcool.com/compgen> "列出所有Linux命令，显示所有可用的命令，别名和函数。"
