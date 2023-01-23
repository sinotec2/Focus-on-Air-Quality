---
layout: default
title:  月曆日轉儒略日(c2j)
parent: Dates and Times
grand_parent: Utilities
last_modified_date: 2022-10-21 12:02:32
tags: datetime
---
# 月曆日轉儒略日(c2j)
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
- 有關[儒略日][儒略日]轉月曆日的轉換，可詳見[j2c][j2c]說明。此處為其反轉程式。

## date(os) and datetime(py)
- 不論是bash或者是python的datetime，都有`+%j`格式，可以輸出成[julian day][儒略日]。設若輸入月曆日值為`$ymd`(+%Y%m%d)

### bash
- date指令：`yyyyjjj=$( date -d "$ymd" +%Y%j)`
- 一般linux的date指令似乎會自行辨識輸入的日期格式(不含小時)
  - 至少可以自動辨識+%Y%m%d及+%Y-%m-%d等2種。
  - 不必(也不能)指定輸入格式。
- 如需此二者以外格式之輸入、或含有小時之日期
  - 使用+%c(locale datetime)格式，如Thu Mar 3 23:05:25 2005
  - 參考[任意格式時間的讀取](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/GFS/1.eath_gfs/#任意格式時間的讀取)。

### macOS
- date指令：`yyyyjjj=$( date -j -f "%Y%m%d" $ymd +%Y%j)`
- 輸入時間格式可以用-f 來指定

### python datetime指令
- str**p**time
  - **p**oint(ex**p**ort) the character string to datetime object
  - `ymd_dt=datetime.datetime.strptime(ymd,'%Y%m%d')`
- str**f**time
  - create **f**ormatted string **f**rom datetime
  - `yj=ymd_dt.strftime('%Y%j')`   

## fortran程式碼(cal2jul.f)
- 此副程式剪裁自UAM及CAMx程式系統，現已不再更新。如在fortran程式內需進行日期的轉換可參考使用。

```fortran
C$ cat ~/bin/cal2jul.f
        character A100*100
        call getarg(1,A100)
        read(A100,*)jjj
        call juldate(jjj)
        write(*,'(I7)')2000000+jjj
        stop
        end

        subroutine caldate(idate)
c
c-----CAMx v4.01 030625
c
c     CALDATE converts date from Julian (YYJJJ) format to calender
c     (YYMMDD) format
c
c     Copyright 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003
c     ENVIRON International Corporation
c
c     Modifications:
c        none
c
c     Input arguments:
c        idate               julian date (YYJJJ)
c
c     Output arguments:
c        idate               calender date (YYMMDD)
c
c     Routines Called:
c        none
c
c     Called by:
c        AREAPREP
c        BNDPREP
c        CNCPREP
c        DRYDEP
c        PIGPREP
c        RDPTHDR
c        READZP
c        STARTUP
c
      dimension nday(12)
      data nday/31,28,31,30,31,30,31,31,30,31,30,31/
c
c-----Entry point
c
c-----If it is already in calender date, return
c
      if (idate.gt.100000) goto 9999
      iyear = idate/1000
      jday = idate - iyear*1000
c
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29
      mday = 0
      do 10 imonth = 1,12
        mday = mday + nday(imonth)
        if (mday.ge.jday) go to 20
 10   continue
 20   iday = jday - (mday - nday(imonth))
      idate = iyear*10000 + imonth*100 + iday
c
 9999 return
      end
c-------------------------------------------------------------
      subroutine juldate(idate)
      dimension nday(12)
      data nday/31,28,31,30,31,30,31,31,30,31,30,31/
c
c-----Entry point
c
      iyear = idate/10000
      imonth = (idate - iyear*10000)/100
      iday = idate - iyear*10000 - imonth*100
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29

      IF(IDAY.GT.NDAY(IMONTH).OR.IDAY.LE.0) THEN
        IDATE=-1
        RETURN
      ENDIF
c
      mday = 0
      do 10 n = 1,imonth-1
        mday = mday + nday(n)
 10   continue
      jday = mday + iday
      idate = iyear*1000 + jday
c
      return
      end
```

[j2c]: <https://sinotec2.github.io/Focus-on-Air-Quality/utilities/DateTime/j2c/> "Julian Day to Calendar Day(j2c)"
[儒略日]: <https://en.wikipedia.org/wiki/Julian_day> "儒略日是在儒略週期內以連續的日數計算時間的計時法，主要是天文學家在使用。 儒略日數的計算是從格林威治標準時間的中午開始，包含一個整天的時間，起點的時間回溯至儒略曆的西元前4713年1月1日中午12點，這個日期是三種多年週期的共同起點，且是歷史上最接近現代的一個起點。 維基百科"