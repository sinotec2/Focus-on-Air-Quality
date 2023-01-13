---
layout: default
title: ISC/AERMOD程式之執行
parent: CO Pathways and Compilation
grand_parent: Plume Models
nav_order: 1
last_modified_date: 2022-03-21 11:38:50
tags: plume_model
---
# ISC/AERMOD程式下載、編譯、與執行、作業環境
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
### ISC3模式
- ISC3 目前為我國環保署認可的煙流模式之一，其程式可以由USEAP [Air Quality Dispersion Modeling - Alternative Models](https://www.epa.gov/scram/air-quality-dispersion-modeling-alternative-models)下載取得。
- ISC3 已經不會有任何官方的更新計畫。
- 有關ISC3的介紹可以參考環保署[高斯類擴散模式的簡要描述](https://aqmc.epa.gov.tw/airquality_1.php)

### AERMOD 模式
- AERMOD 雖然還不在我國認可使用模式範圍，然為未來公告對象，程式碼與PC版本執行檔可由USEPA [preferred-and-recommended-models](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models#aermod)取得。該網站將不時更新版本，目前版本為04-22-2021。

### 編譯挑戰
- 由於個人電腦在記憶體、多工作業、繪圖系統、遠端作業等面向限制頗多，移到Mac或Linux系統似為一較佳選項。
- 除了個人電腦平台之外的作業系統，USEPA並不直接提供執行檔，需由使用者自行編譯。
- ISC3程式碼較為老舊，編譯無太大困難。AERMOD系統程式應用較多新的Fortran語法，且因新的編譯軟體對Fortran的嚴格程式有加嚴的趨勢，因此造成編譯上的挑戰。

### wget下載注意事項
- 需加註選項`--no-check-certificate`，避免無法通過資格確認

## Linux Solutions
### isc3
- ISCST3內設是LF90或LF95程式進行編譯，其他編譯程式則需針對部分程式碼進行修改。
- 由於沒有較新編譯器選項可供參考，此處按照aermod之選項進行編譯

#### gfortran
- 以gfortran而言，並沒有**CARRIAGECONTROL**跳行指令。gfortran的文字檔IO自動會有CARRIAGECONTROL，因此將此設定去掉，並不會影響結果。

```fortran
CLF90 The CARRIAGECONTROL specifier in the following statement is a
CLF90 non-standard Lahey language extension (also supported by DEC VF),
CLF90 and may need to be removed for portability of the code.
      OPEN (UNIT=IOUNIT,FILE=OUTFIL,CARRIAGECONTROL='FORTRAN',
     &      ERR=99,STATUS='UNKNOWN')
```
- GETCOM(由命令列獲取引數)
  - 該副程式有2種Fortran版本，Lahey及DEC Visual Fortran(DVF)，沒有近年來較常見的ifort或gfortran
- 選擇較接近的DVF。在gfortran(ifort亦然)，與DVF的比較如下表

|項目|DEC Visual Fortran(DVF)|gfortran|  
|-|-|-|
|引數個數|NARGS()|iARGc()|
|獲取引數|CALL GETARG(IARG,OUTFIL,ISTAT)|CALL GETARG(IARG,OUTFIL)|

- 更正後的GETCOM
```fortran
      SUBROUTINE GETCOM (MODEL,LENGTH,INPFIL,OUTFIL)
      IMPLICIT NONE

      INTEGER LENGTH
      CHARACTER (LEN=LENGTH) :: INPFIL, OUTFIL
      CHARACTER (LEN=8)      :: MODEL
CDVF!DEC$ IF DEFINED (DVF)
CDVFC     Declare 2-Byte Integer for Field Number of Command Line Argument
      INTEGER*2 IARG, IFCNT, ISTAT
CDVF!DEC$ IF DEFINED (DVF)
CDVFC************************************************************DVF START
CDVFC     Use Microsoft/DEC Functions NARGS and GETARG To Retrieve
CDVFC     Contents of Command Line
      IFCNT = iARGc()
CDVFC     IFCNT Is The Number Of Arguments on Command Line Including Program
      IF (IFCNT .NE. 2) THEN
CDVFC        Error on Command Line.  Write Error Message and STOP
         WRITE(*,660) MODEL
         STOP
      ELSE
CDVFC        Retrieve First Argument as Input File Name
         IARG = 1
         CALL GETARG(IARG,INPFIL)
CDVFC        Retrieve Second Argument as Output File Name
         IARG = 2
         CALL GETARG(IARG,OUTFIL)
      END IF
CDVFC************************************************************DVF STOP
CDVF

CDVF!DEC$ ENDIF

  660 FORMAT (' COMMAND LINE ERROR: ',A8,' input_file output_file')

      RETURN
      END
```
- 編譯批次檔gfortranISCS.BAT
  - 程式間的編譯順序是有意義的。
  - 因程式會連結到.mod檔案，需先針對.mod進行編譯，產生mod檔後方便後面副程式的編譯。

```bash
COMPILE_FLAGS=' -fbounds-check -Wuninitialized -O2 -static'
LINK_FLAGS=' -static -O2'
for f in \
 MODULES ISCST3 SETUP COSET SOSET RESET MESET\
 TGSET OUSET INPSUM METEXT CALC1 CALC2 PRISE\
 SIGMAS DEPFLUX PITAREA OUTPUT EVSET EVCALC EVOUTPUT;do
    gfortran -c $COMPILE_FLAGS $f.FOR
done
gfortran -o iscst3.exe $LINK_FLAGS *.o
```
#### ifort
- 由於ifort與gfortran對前述程式碼修改完全一樣，僅編譯(選項)方式有些不同。
- 編譯選項參考aermod的ifort批次檔

```bash
COMPILE_FLAGS=' -O2 -check format -ipo -prec-div -axSSE2 -traceback -diag-disable=8291'
LINK_FLAGS='-O2 -check format -ipo -prec-div -axSSE2'
for f in \
 MODULES ISCST3 SETUP COSET SOSET RESET MESET\
 TGSET OUSET INPSUM METEXT CALC1 CALC2 PRISE\
 SIGMAS DEPFLUX PITAREA OUTPUT EVSET EVCALC EVOUTPUT;do
    ifort -c $COMPILE_FLAGS $f.FOR
done
ifort -o iscst3.exe $LINK_FLAGS *.o
```
### aermod
#### gfortran
- USEPA提供pc版本的編譯批次檔
```bash
$ head gfortran-aermod.bat
rem @echo off
setlocal
set COMPILE_FLAGS= -fbounds-check -Wuninitialized -O2 -static
set LINK_FLAGS= -static -O2

gfortran -c %COMPILE_FLAGS% modules.f
...
gfortran -o aermod.exe %LINK_FLAGS% MODULES.o GRSM.o AERMOD.o SETUP.o COSET.o SOSET.o RESET.o MESET.o OUSET.o INPSUM.o METEXT.o IBLVAL.o SIGGRID.o TEMPGRID.o WINDGRID.o CALC1.o CALC2.o PRISE.o PRIME.o SIGMAS.o PITAREA.o UNINAM.o OUTPUT.o EVSET.o EVCALC.o EVOUTPUT.o RLINE.o BLINE.o

del *.o
del *.mod
```
- 由於gfortran的選項在不同平台有很高的一致性，只需將DOS環境變數習慣改成linux即可

```
COMPILE_FLAGS=' -fbounds-check -Wuninitialized -O2 -static'
LINK_FLAGS=' -static -O2'
gfortran -c $COMPILE_FLAGS modules.f
...
gfortran -o aermod.exe $LINK_FLAGS *.o
```
#### ifort
- 參考USEPA提供的編譯批次檔(intel-aermod.bat<sup>*</sup>)內容，以及ifort[編譯選項](https://www.intel.com/content/www/us/en/develop/documentation/fortran-compiler-oneapi-dev-guide-and-reference/top/compiler-reference/compiler-options/alphabetical-list-of-compiler-options.html)

|選項|意義|pc_bat<sup>*</sup>|linux|MacOS|
|-|-|-|-|-|
|O2|最佳化|/O2|-O2|(same)|
|check|編譯時檢核特定項目|/check:format|-check format|(same)|
|ipo|啟動檔案之間的程序間最佳化(interprocedural optimization between files)|/Qipo|-ipo|(same)|
|prec|增進除法浮點運算的精度|/Qprec-div-|-prec-div|(same)|
|ax|如有執行上的優勢ifort將會產生多項、特殊項目程式碼的自動修補的功能|/QaxSSE2(舊) /QaxcodeSSE2|-axcodeSSE2|(無)|
|traceback|開啟執行失敗之回溯|/trace(舊) /traceback|-traceback|(same)|
|diag|關閉編號8291錯誤之診斷|/Qdiag-disable:8291|-diag-disable=8291|(same)|

- 原pc版本編譯批次檔intel-aermod.bat

```bash
$ head intel-aermod.bat
@REM                                                                    + + +
@echo off

setlocal

set COMPILE_FLAGS=/O2 /check:format /Qipo /Qprec-div- /QaxSSE2 /trace  /Qdiag-disable:8291
set LINK_FLAGS=/O2 /Qipo /check:format /Qprec-div- /QaxSSE2

ifort /compile_only %COMPILE_FLAGS% modules.f
...
ifort /exe:aermod.exe %LINK_FLAGS% MODULES.obj GRSM.obj AERMOD.obj SETUP.obj COSET.obj SOSET.obj RESET.obj MESET.obj OUSET.obj INPSUM.obj METEXT.obj IBLVAL.obj SIGGRID.obj TEMPGRID.obj WINDGRID.obj CALC1.obj CALC2.obj PRISE.obj PRIME.obj SIGMAS.obj PITAREA.obj UNINAM.obj OUTPUT.obj EVSET.obj EVCALC.obj EVOUTPUT.obj RLINE.obj bline.obj

del *.obj
del *.mod
```
- 對應在linux則為

```bash
COMPILE_FLAGS='-O2 -check format -ipo -prec-div -axSSE2 -traceback -diag-disable=8291'
LINK_FLAGS='-O2 -check format -ipo -prec-div -axSSE2'
for f in modules grsm aermod setup coset soset reset meset ouset\
 inpsum metext iblval siggrid tempgrid windgrid calc1 calc2 prise\
 prime sigmas pitarea uninam output evset evcalc evoutput rline\
 bline;do
  ifort -c $COMPILE_FLAGS $f.f
done
ifort -o aermod.exe $LINK_FLAGS *.o

rm *.o
rm *.mod
```

## MacOS Solutions

- Mac的特性就是系統的更新速度很快，對Fortran程式碼檢查也較為嚴苛
- 目前MacOS上只有gfortran經驗。可以參考[mmif的編譯](/Focus-on-Air-Quality/PlumeModels/ME_pathways/mmif/#準備及編譯)
### isc3編譯
- -fbounds-check：會太嚴格，編譯會失敗，予以取消不執行。
- 無法static link，會找不到crt0.o
- 針對CARRIAGECONTROL問題，需設定-fdec
- -std=legacy有助呼叫副程式引數的格式確認

```bash
kuang@114-32-164-198 /Users/1.PlumeModels/ISC/short_term/src
$ cat cpl.sh
COMPILE_FLAGS=' -Wuninitialized -O2 -fdec -std=legacy -Wmaybe-uninitialized'
LINK_FLAGS=' -O2'
for f in \
 MODULES ISCST3 SETUP COSET SOSET RESET MESET\
 TGSET OUSET INPSUM METEXT CALC1 CALC2 PRISE\
 SIGMAS DEPFLUX PITAREA OUTPUT EVSET EVCALC EVOUTPUT;do
    gfortran -c $COMPILE_FLAGS $f.FOR
done
gfortran -o iscst3.exe $LINK_FLAGS *.o
```
### aermod編譯
- 使用前述ISC3的編譯設定，針對aermod各程式進行編譯

```bash
COMPILE_FLAGS=' -Wuninitialized -O2 -fdec -std=legacy -Wmaybe-uninitialized'
LINK_FLAGS=' -O2'
for f in modules grsm aermod setup coset soset reset meset ouset\
 inpsum metext iblval siggrid tempgrid windgrid calc1 calc2 prise\
 prime sigmas pitarea uninam output evset evcalc evoutput rline\
 bline;do
    gfortran -c $COMPILE_FLAGS $f.FOR
done
gfortran -o iscst3.exe $LINK_FLAGS *.o
```

## Reference
- 白曛綾教授、交通大學開放式課程[空氣品質影響之預測](http://ocw.nctu.edu.tw/course/arm071/Chapter%207.pdf)