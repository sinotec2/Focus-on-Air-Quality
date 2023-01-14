---
layout: default
title:  ncdump應用範例
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-07-18 15:23:00
tags: netCDF
---
# ncdump應用範例
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
- netCDF是地球科學領域重要的檔案格式。然而因其二進位檔案格式的限制，不方便以文字檔案方式檢閱，[官網](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/utilities/Ncdump.html)提供了ncdump讓使用者可以輕鬆讀取其內容。
- 由於netCDF檔案使用了階層的資訊技術，除了ncdump，使用python或其他高階的軟體(或程式庫)，可以直接讀取其內容，不必再以文字檔模式循序讀取。
- 以下以[ioapi][ioapi]協定之內容說明CDL(common data format language)的內容順序如下表所示。

### CDL的內容順序

項次|名稱|內容|說明
-|-|-|-
1|dimensions|所有變數應用到的維度名稱、長度、是否受限|與檔案結構有關，為表頭的第一組內容
2|variables|按照英文字母的順序將所有變數名稱列表，包括其維度、數據類別(整數、實數、字串、邏輯布林等)、個別屬性如長名稱、內容敘述、單位等等，使用者可以自由增加變數的屬性|表頭的第二組內容，如檔案含有眾多變數(VAR維度的長度很長)，ncdump結果會很長
3|global attributes|全域屬性，有關整體檔案的性質，使用者也可以ncatted來增減修改其內容。|其中history的內容是nco程式庫自動產生的，可以從中找到檔案處理的過程，如果是fortran或是python所產生的新檔，則不會記錄在其history。
4|data|數據內容，會按前述排序依次印出變數的內容，顯示的維度順序如未指定，為C語言協定方式|內容會非常長，如未妥善引導將會佔據顯示器記憶體。一般會以ncdump -h選項只列出表頭(--head)，以避免出現data部分節省顯示器記憶內容。

### ncdump的應用原則
- 將表頭顯示於螢幕或檔案進行確認
  - 使用`ncdump -h $nc`指令
- 將整個檔案連data數據內容輸出成CDL文字檔案進行後續處理，再以[ncgen](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pncgen/#ncgen)轉成nc檔案。
  - 範例可以詳見鳥哥為公版模式所寫的[run.ocean.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/run.ocean.sh.TXT)

## 應用範例
- nc檔案的維度：`ncdump -h $nc|head`
- [ioapi][ioapi]檔案的起始日期時間：`ncdump -h $nc|grep SDATE;ncdump -h $nc|grep STIME;`
- 特定條件之實數變數名稱：`ncdump -h $nc|grep float|grep DUST`
- 尋找特定全域變數的內容：`ncdump -h $nc|grep NAME_CAMx`
- 列印表頭及特定變數的內容：`ncdump -v CP_NO $nc|M`
- 從nc檔案的歷史紀錄中找到含有ncks的特定文字(見[nc檔案更名](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/NCAR_ACOM/MOZART/#nc檔案更名))：`ncdump -h $nc|grep ncks|cut -d/ -f10|cut -d . -f11|cut -c -10`
- 從變數的個數來判斷是什麼模式產生的結果
  - `v=$(ncdump -h $nc|grep PM25|wc -l);a=$(ncdump -h $nc|grep AVERAGE|wc -l)`
  - 參見[shk.cs](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/do_shk/#shkcs)

## pncdump
- [pseudonetcdf][pseudonetcdf]套件中也有類似ncdump的程式pncdump，提供更多輸入/輸出格式的選項。有關pncdump支援的格式，可以參考[pncgen][pncgen]。
- 此處著眼ncdump及pncdump程式的差異說明。


項次|功能|ncdump|pncdump|說明
-|-|:-:|:-:|-
1|只看表頭|-h, -c|-H, \-\-head|-h在後者是help
2|部分變數|-v|-v|(same)
3|dump與gen功能|互斥|互用|pncdump也可用於修改檔案
4|指定IO格式|只有nc to text|可以接受-f \-\-out-format|後者非常多樣化

## Reference
- unidata.ucar(2011), [ncdump](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/utilities/Ncdump.html)
- 國家實驗研究院台灣颱風洪水研究中心(2016), NCAR command language workshop, [NetCDF格式介紹](http://u.camdemy.com/media/8487)

[ioapi]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ioapi/> "I/O API(Input/Output Applications Programming Interface)是美國環保署發展Models-3/EDSS時順帶產生的程式庫(cmascenter, I/O API concept)，用來快速存取NetCDF格式檔案，尤其對Fortran等高階語言而言，是非常必須之簡化程序。"
[pseudonetcdf]: <https://github.com/barronh/pseudonetcdf/blob/master/scripts/pncgen> "PseudoNetCDF provides read, plot, and sometimes write capabilities for atmospheric science data formats including: CAMx (www.camx.org), RACM2 box-model outputs, Kinetic Pre-Processor outputs, ICARTT Data files (ffi1001), CMAQ Files, GEOS-Chem Binary Punch/NetCDF files, etc. visit  barronh /pseudonetcdf @GitHub."
[pncgen]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/pncgen/#pncgenpncdump-所有可接受的格式> "FAQ -> Utilitie -> NetCDF Relatives -> ncgen & pncgen -> pncgen/pncdump 所有可接受的格式"