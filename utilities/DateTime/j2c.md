---
layout: default
title:  Julian Day to Calendar Day(j2c)
parent: Dates and Times
grand_parent: Utilities
last_modified_date: 2022-08-29 14:28:00
tags: datetime
---

# Julian Day to Calendar Day
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

- Julian Day([儒略日][儒略日])因其具有連續性，不會因跨月、潤年等因素而發生錯誤，是時間計算過程中很重要的一種方式。
- 過去在Fortran程式的領域，是以一簡單的副程式計算。移轉到python平台上時，從datetime模組即能直接進行加減及轉換處理。而在bash平台上，則還需要整合一些技巧。
- 作為平台上計算的小工具，前述作法都有一些困難：
  1. python程式需要啟動複雜的模組、
  1. Fortran程式在每次跨平、跨fc版本就需要重新編譯
- 相較而言還是以bash指令能解決最好，bash腳本具有高度的相容性，即使跨越到macOS，date指令可以直接讀取Julian Day，更容易使用。
- bash腳本需處理的問題：
  - 辨識年代及Julain Day。應用時有時輸入4碼年、有時輸入2碼年
  - 計算日數：bash內設環境變數是個字串，字串需要轉成數字才能計算
  - 以date指令呈現出結果月曆日(Calendar Day)
- 月曆日轉儒略日([cal2jul][], c2j)
  - 直接以date指令指定輸出格式是%Y%j或(7碼)%y%j(5碼)即可。

## j2c腳本說明
### 年與日值之切割
- 年代值(`$y`)
  - 辨識4碼或2碼年代：使用${#var}來讀取環境變數的長度
  - 切割年值
    - 使用cut指令。
    - 因不論4碼或2碼年代，年代值不可能以0為首，因此字串即為以10為底之整數，不需轉換。
- 日值(`$y`)
  - 字串需轉成(10進位的)整數，以利比較與計算
    - 文字：$j，其值為001 ~ 366
    - 數字：10#$j，其值為 1 ~ 366

### 跨年問題
- 雖然Julian day具有連續特徵，但跨年非為連續，腳本需設有檢查點，以判斷輸入值是否在合理正確範圍。
- 判斷依據是全年總日數(`$jm`值)
  - 大於總日數之輸入值：直接跳出程式
  - 小或等於總日數：進入日期的計算
- 總日數(`$jm`值)按一般年及潤年而有差異
  - 一般年，`$jm`值為365、潤年此值為366，
  - 使用test判斷，年值除4如能整除為潤年。

```bash
jm=365
test $(( $y % 4 )) == 0 && jm=366
j=$(( 10#$j ))
test $j -gt $jm && exit 0
```

### 月曆日之計算
- 使用date指令。此指令在大多數unix_like作業系統都能通用，僅macOS略有差異
- linux/unix版本：使用date -d 計算
  - Julian Day([儒略日][儒略日])的起始日是該年度的1月1日，因此只需要將Julian Day日數減1，加在該年度的1月1日，即可計算出Julian Day的月曆日。
  - `date -d "${y}-01-01 +$(( $j - 1))days" +%Y%m%d`
  - 數字的四則運算：$(( ... ))
- macOS：直接以date -j -f 讀取與轉換，無需計算
  - 4碼年：`date -j -f "%Y%j" $yj +%Y%m%d`
  - 2碼年：`date -j -f "%y%j" $yj +%y%m%d`

### bash腳本內容

```bash
yj=$1
if [ ${#yj} -eq 7 ];then
  y=$(echo $yj|cut -c-4)
  j=$(echo $yj|cut -c5-)
elif [ ${#yj} -eq 5 ];then
  y=20$(echo $yj|cut -c-2)
  j=$(echo $yj|cut -c3-)
else
  echo 'input YYJJJ or YYYYJJJ'
  exit  0
fi

jm=365
test $(( $y % 4 )) == 0 && jm=366
j=$(( 10#$j ))
test $j -gt $jm && exit 0

j=$(( $j - 1 ))
echo $(date -d "${y}-01-01 +$(( $j - 1))days" +%Y%m%d)
```

### macOS腳本內容

```bash
yj=$1
if [ ${#yj} -eq 7 ];then
  echo $(date -j -f "%Y%j" $yj +%Y%m%d)
elif [ ${#yj} -eq 5 ];then
  echo $(date -j -f "%y%j" $yj +%Y%m%d)
else
  echo 'input YYJJJ or YYYYJJJ'
  exit  0
fi
```

## Fortran版本
- 此副程式剪裁自UAM及CAMx程式系統，現已不再更新。如在fortran程式內需進行日期的轉換可參考使用。

```fortran
kuang@node03 ~/bin
$ cat jul2cal.f
        character A100*100,nam0(100)*100
        narg=iARGc ()
        if(narg.ne.1)stop  'jul2cal yyjjj'
        call getarg(1,A100)
        read(A100,*)jjj
        iy=jjj/1000
        jul=mod(jul,1000)
        julend=365
        if(jul.gt.julend)then
          if(mod(iy,4).eq.0)julend=366
          if(jul.gt.julend) jjj=(iy+1)*1000+(jul-julend)
        endif
        call caldate(jjj)
        write(*,'(I6)')jjj
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
      if (idate.gt.100000) goto 9998
      iyear = idate/1000
      jday = idate - iyear*1000
c
      mday = 0
      do 11 iiy=1,3
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29
      do 10 imonth = 1,12
        mday = mday + nday(imonth)
        if (mday.ge.jday) go to 20
 10   continue
      !mday=mday-sum(nday)
      iyear=iyear+1
 11   continue
 20   iday = jday - (mday - nday(imonth))
      idate = iyear*10000 + imonth*100 + iday
c
 9999 return
 9998 idate=-1
      return
      end
```

[儒略日]: <https://en.wikipedia.org/wiki/Julian_day> "儒略日是在儒略週期內以連續的日數計算時間的計時法，主要是天文學家在使用。 儒略日數的計算是從格林威治標準時間的中午開始，包含一個整天的時間，起點的時間回溯至儒略曆的西元前4713年1月1日中午12點，這個日期是三種多年週期的共同起點，且是歷史上最接近現代的一個起點。 維基百科"