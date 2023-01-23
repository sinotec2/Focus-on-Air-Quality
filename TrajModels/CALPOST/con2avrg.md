---
layout: default
title: CALPUFF模擬結果之轉檔
nav_order: 2
parent: CALPOST
grand_parent: Trajectory Models
last_modified_date: 2022-06-07 11:56:20
tags: cpuff cpost uamiv
---

# CALPUFF模擬結果轉uamiv檔案
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
- [uamiv][uamiv]格式可以適用CAMx、UAM等模式之IO與處理軟體([如VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/))
- [con2avrg.f](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/TrajModels/CALPOST/con2avrg.f)基本上就是CALPOST.FOR加上CAMx的寫出副程式(`wrtcamx`)


[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"

## 程式修改
### 開啟輸出檔案
- 檔名內設為calpuff.con **.S.grd02**

```fortran
 1374       open( 91,file=trim(moddat)//'.S.grd02',
 1375      &status='new', !kuang
 1376      &convert='big_endian',form='unformatted',iostat=io91) !kuang
 1377
 1378 c
```
### 轉接時間相關變數
- JB,JE為起迄Julian dates (*YYYYJJJ*)
- TB,TE為起迄小時(00~23)

```fortran
 1379 c  Loop over averaging periods --------------------------
 1380 10    iper=iper+1
 1381 c
 1382 c --- Read modeled data
 1383 c
 1384 c  Process every "NREP" period of data
 1385       JB=mod(int(idathrbx/100),100*1000)              !kuang
 1386       JE=mod(int(idathrex/100),100*1000)              !kuang
 1387       TB=mod(idathrbx,100)+ibscx/3600.  !kuang.
 1388       TE=mod(idathrex,100)+iescx/3600.  !kuang.
```
### 呼叫輸出副程式
- 在nrep迴圈的最後呼叫CAMx的副程式`wrtcamx`
- 將前述時間變數以引數方式傳到副程式

```fortran
 1389       do iev=1,nrep
...
 1401          if(io91.eq.0)call wrtcamx(JB,TB,JE,TE,idimx,idimy) !kuang
 1402       enddo
```

### wrtcamx副程式
- CALPUFF系統的座標長度為Km，需轉成m
- CAPOLST的污染項目不被VERDI所接受，需借用其他既有的污染物名稱。對照關係如下表

|calpuff.con|calpuff.con.S.grd02.nc|phase|
|-|-|-|
|SO2|SO2|gas|
|PM25|PM25|particulate|
|NOx|NOx|gas|
|SO4|CO|particulate|
|NO3|NO2|gas|
|HNO3|O3|gas|

- 小時數加8，以轉成LST
- 濃度乘上10<sup>6</sup>，轉成&mu;g/M<sup>3</sup>。

```fortran
23659       !kuang
23660       subroutine wrtcamx(JB,TB,JE,TE,ncol,nrow)
23661       INCLUDE 'params.pst'
23662       include 'arrays.pst'
23663       include 'head.pst'
23664       include 'specout.pst'
23665       INCLUDE 'conc.pst'
23666       character*4 SPNAME(10,mxspec),fname(10),note(60)
23667       dimension MSPEC(10,mxspec)
23668       character airq*10,titl*100,tmp*4
23669       data airq/'AVERAGE   '/
23670       data iout/0/ISEG/0/
23671       jend=365
23672       if(mod(JB/1000,4).eq.0)jend=366
23673       TB=TB-xbtz+8
23674       if(TB.ge.24)then
23675         JB=JB+1
23676         if(mod(JB,1000).gt.jend) JB=(JB+1000)-jend
23677         TB=TB-24
23678       endif
23679       Jo=JB+32
23680       if(mod(Jo,1000).gt.jend) Jo=(Jo+1000)-jend
23681       if(iout.eq.0)then
23682         titl='CAMx from ...'//atitle(1)
23683           do j=1,10
23684             fname(j)(1:1)=airq(j:j)
23685           enddo
23686           do j=1,60
23687             note(j)(1:1)=titl(j:j)
23688           enddo
23689         SPNAME='    '
23690         do k=1,NOSPEC
23691           tmp=osplst(k)(1:4)
23692           if(tmp(1:3).eq.'SO4')tmp='CO '
23693           if(tmp(1:3).eq.'NO3')tmp='NO2'
23694           if(tmp(1:3).eq.'HNO')tmp='O3 '
23695           do j=1,4
23696             SPNAME(j,k)(1:1)=tmp(j:j)
23697           enddo
23698 !        print*,osplst(k)
23699 !        print*,(SPNAME(I,k),I=1,10)
23700         enddo
23701       data  noz/1/NVLOW, NVUP,DZMINU/2,0.,0./
23702       write(91) fname, note, 1, NOSPEC, JB, TB, Jo, TB
23703       write(91) relon0, rnlat0,NZONE,xorigkm*1000.,yorigkm*1000.,
23704      $ delx*1000.,dely*1000.,
23705      $ ncol , nrow, noz, NVLOW, NVUP, 10., 40., DZMINU
23706       write(91)1,1,ncol,nrow
23707       write(91)((SPNAME(I,k),I=1,10),k=1,NOSPEC)
23708         iout=1
23709       endif
23710 C      print*,'base time zone=', xbtz
23711       TE=TE-xbtz+8
23712       if(TE.ge.24)then
23713         JE=JE+1
23714         TE=TE-24
23715         if(mod(JE,1000).gt.jend) JE=(JE+1000)-jend
23716       endif
23717       write(91)JB,TB,JE,TE
23718       do L=1,NOSPEC
23719        do K=1,noz
23720         write(91)ISEG,(SPNAME(I,L),I=1,10),((aconcg(i,j,L)*1.E6,i=1,ncol),j=1,nrow)
23721 !     print*,maxval(aconcg(1:ncol,1:nrow,k))
23722 !     print*,JB,TB,JE,TE,ncol,nrow
23723       enddo
23724       enddo
23725       return
23726       end
```

## 執行方式
### 需要檔案
- calpuff.con
- calpost.inp
### 輸出檔案
- calpost.inp所指定輸出檔案(eg. *grd)
- calpuff.con.S.grd02 ([uamiv](https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式) format)

