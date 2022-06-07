---
layout: default
title:  NCKS空品模式應用
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date:   2021-12-10 11:31:33
---
# NCKS 在空品模式中的應用
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
## 一般
- `-O` 處理結果覆蓋(**O**verwrite)既有檔案
- `-m teds10.1612.timvar.nc` 將檔案維度、變數說明(**m**etadata)印出(類似[ncdump]() -h)
- ncks的`-a`, `--cdl`, `-F`, `--fmt_val`, `-H`, `--hdn`, `--jsn`, `-M`, `-m`, `-P`, `--prn_fl`, `-Q`, `-q`, `-s`, `--trd`, `-u`, `-V`, `--xml` 选项可以控制输出檔案的格式。

### 全域屬性(global **att**ribute)
逐一修改全域屬性是[ncatted]()的功能，但是ncks也有一次全部複製的能力，用來套用既有檔案的全域屬性。
- `ncks -A -x in.nc out.nc` 複製in.nc全域屬性到新檔案out.nc

### 變數(variable)
- ncks經常使用來增、減nc檔案的變數。可以大幅減省在python(或其他)程式的coding工作，且一般程式只能增加nc檔案的變數(指令如`result=nc.createVariable(s,"f4",("TSTEP","LAY","ROW","COL"))`)，但不能更名、刪除一既有檔的變數，必須仰賴ncks由檔案外部來進行更動。
- 減少變數的個數：刪去無關的變數，將大幅縮減檔案的大小，方便於網路傳送，使用VERDI或其他顯示軟體也較便利(VERDI對開啟大於1GB的檔案仍有困難)。以下範例將會刪除`base.grd02.1909.nc`檔案中的變數`NO2,O3`(2個以上變數名稱間以`,`隔開，最後變數之後不能再有逗號)，以形成新檔`a.nc`。

```bash
 ncks -x -v NO2,O3 base.grd02.1909.nc a.nc
```
 
- 增加變數：用以形成新的nc檔案模版。
- `ncks -v NO,TFLAG,ETFLAG base.grd02.1909.nc NO.nc`提出特定之變數、形成新檔，程式會自帶相依座標，但不會有時間標籤。如不要座標，要多加`-C`。

## 維度剪裁
類似的，如果要增加、延續維度的長度是用[ncrcat]()，如果要剪裁，則為ncks的強項。尤有進者[ncrcat]()只能針對UNLIMITED維度進行延長，如果要增加其他維度，則先要更改維度的定義，也是靠ncks才能更動。
- `-d TSTEP,0,23,3` 切割特定維度的一部分。由0開始，到底(23不像python加1)、間距(3)。(eg. [brk_day2.cs:按照日期切割m3.nc](https://boostnote.io/shared/7fd2257f-ba2b-4bd1-9e80-54be96a3bfee))
- `--mk_rec_dmn ROW` 定義「可增加」資料筆數之維度(**m**a**k**ing **rec**ord **d**i**m**e**n**sion，**記錄軸**)
  - 所謂「可增加」，在[ncdump -h]()結果會看到該維度有一長度，且是`UNLIMITED`。(範例如下，維度TSTEP的長度是UNLIMITED，目前是121，其餘維度長度則為固定的數字)
  - 須先將檔案的維度定義成可增加，才能進行[ncrcat](https://boostnote.io/shared/9bd4d899-ecd2-4891-8d50-dc0856d1c191)或使用python增加該維度之長度。
  - eg. [expand_xy.csh:擴展nc檔案的水平格點數](https://boostnote.io/shared/4450b3a4-673b-4c7f-98c7-a24368abfe67)

```bash
$ ncdump -h $nc|head
netcdf BCON_v53_1912_run9_regrid_20191217_TWN_3X3 {
dimensions:
        TSTEP = UNLIMITED ; // (121 currently)
        DATE-TIME = 2 ;
        LAY = 40 ;
        VAR = 226 ;
        PERIM = 444 ;
variables:
        int TFLAG(TSTEP, VAR, DATE-TIME) ;
                TFLAG:units = "<YYYYDDD,HHMMSS>" ;
```
- `--fix_rec_dmn TSTEP` 定義不可增加筆數之維度(**f**ix **rec**ord **d**i**m**e**n**sion)
- ncks只能增減變數，如要更改變數名稱，則必須要使用[ncrename]()，如 `ncrename -O -v PM25_TOT,DIS_INCI stroke.nc stroke1.nc`

## 序列之規則
- 維度或座標軸後接了3個數字，分別是起、迄、與間隔，以逗點隔開，如果不指定則跳過。
- 維度的索引必須是整數，座標軸的值必須是實數
- 如未指定(更改為Fortran習慣)，序號採0開始之C語言習慣。且含最後值，與python不同。
- ncks手冊作者[Zender and Mays](https://linux.die.net/man/1/ncks)提供了範例:
```bash
# Create netCDF out.nc containing all variables from file in.nc. Restrict the dimensions of these variables to a hyperslab. 
#Print (with -H) the hyperslabs to the screen for good measure. 
#The specified hyperslab is: 
#the sixth value in dimension time; 
#the half-open range lat <= 0.0 in coordinate lat; 
#the half-open range lon >= 330.0 in coordinate lon; 
#the closed interval 0.3 <= band <= 0.5 in coordinate band; 
#and cross-section closest to 1000.0 in coordinate lev. 
#Note that limits applied to coordinate values are specified with a decimal point, and limits applied to dimension indices do not have a decimal point.
ncks -H -d time,5 -d lat,,0. -d lon,330., -d band,.3,.5 -d lev,1000. in.nc out.nc
```

## 加長一個LIMITED維度
- 一般nc檔案在空間的維度是保持LIMITED的，讓檔案不會被輕易更動而亂套。
- 在準備不同網格系統模版的過程，會遇到情況需要較長的空間維度，除了可以重新用python來產生(nc.createDimension)之外，亦可以由既有較小的模版來延伸，但要先解除該維度LIMITED狀態。
- 先使用ncpdq暫時改變維度的排列順序，將第一順位設成是欲加長的維度(ROW)(其後的順序不影響結果)、並且令其為筆數維度(rec_dmn)，ROW就會變成UNLIMITED：

```bash
ncpdq -O -a ROW,TSTEP,LAY,COL $nc a
ncks -O --mk_rec_dmn ROW a $nc
```
- 再使用ncrcat或者是python程式來加長ROW的長度
- ncpdq指令的使用可以參考[百度文庫](https://wenku.baidu.com/view/c6b2686cf56527d3240c844769eae009581ba229.html?re=view)。

### 使用ncrcat
- 重複執行ncrcat，讓UNLIMITED維度**倍數**成長，直到成長到超過所需長度
- 再用ncks -d仔細修減到所需長度

### 使用python
- 先針對ROW維度進行加長(至395、CWB WRF_15Km d0之南北向網格數)

```python
import netCDF4
fname='templateD0.nc'
nc = netCDF4.Dataset(fname, 'r+')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nrow,nt,nlay,ncol=nc.variables[V[3][0]].shape
for j in range(nrow,395):
  for v in V[3]:
    nc[v][j,:,:,:]=0
nc.close()
```
- 重複此動作，改針對COL維度(至671、CWB WRF_15Km d0之東西向網格數)

```bash
ncpdq -O -a COL,TSTEP,LAY,ROW $nc a
ncks -O --mk_rec_dmn COL a $nc
```
- python(略)
- 回復正常順序、重新定義筆數維度

```bash
ncpdq -O -a TSTEP,LAY,ROW,COL $nc a
ncks -O --mk_rec_dmn TSEP --fix_rec_dmn COL --fix_rec_dmn ROW a $nc
$ ncdump -h $nc|head
netcdf templateD0 {
dimensions:
        TSTEP = UNLIMITED ; // (1 currently)
        LAY = 1 ;
        ROW = 395 ;
        COL = 671 ;
        VAR = 35 ;
        DATE-TIME = 2 ;
variables:
        float ALD2(TSTEP, LAY, ROW, COL) ;
```

## 維度刪除(ncwa)
- ncks只能將維度減到最少，但不能使維度從檔案中消失。要刪除檔案中特定的維度(delete dimension)須使用ncwa([範例](http://stackoverflow.com/questions/20215529/delete-a-dimension-in-a-netcdf-file))指令。
  - 如以下geo_em.nc檔案中的風蝕係數，其維度為[`Time`, `dust_erosion_dimension`, `south_north`, `west_east`]，其中`dust_erosion_dimension`是[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)無法辨識的，因此必須將其刪除才能檢視。

```bash
ncwa -O -a dust_erosion_dimension erod.nc a
mv a erod.nc
```
- ncwa的全名是netCDF Weighted Averager，因為針對維度進行平均，會消除該維度的變化。如果該維度長度為1，則直接將其刪除。參[Charlie Zender and Brian Mays](https://linux.die.net/man/1/ncwa)。

## 維度更名(ncrename)
- WRF-chem排放量檔案的垂直軸(emissions_zdim)並非真的垂直軸(bottom_top)，致使[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_Guide/)無法解析，需要更名

```bash
ncrename -d emissions_zdim,bottom_top $nc
```
- Charlie Zender and Brian Mays, **ncrename(1) - Linux man page**, [linux.die.net](https://linux.die.net/man/1/ncrename), 1995

## 變數+維度複合變更
m3.nc檔案中的變數本身也是一個維度(`VAR`)，其長度為全域屬性`nc.NVARS`，變數的項目也是全域屬性`nc.VAR-LIST`的內容。雖然變更變數項目只涉及到時間標籤(`TFLAG[TSTEP,VAR,DATE-TIME]`)的長度，然CMAQ對其檢驗非常仔細，必須修剪到完全正確。如下列模版的製作過程：
1. 先以`ncks -d`由CMAQ模式結果檔案取出時間、高度、與變數，縮減檔案大小：
```bash
ncks -d LAY,0,33 -d TSTEP,0,0 -v TFLAG,AALJ,ACAJ,ACLI,ACLJ,ACLK,ACORS,AECI,AECJ,AFEJ,AISO3J,AKJ,AMGJ,AMNJ,ANAI,ANAJ,ANH4I,\
ANH4J,ANH4K,ANO3I,ANO3J,ANO3K,AOLGAJ,AOLGBJ,AORGCJ,AOTHRJ,APNCOMI,APOCI,APOCJ,ASEACAT,ASIJ,ASO4I,ASO4J,ASO4K,ASOIL,ASQTJ,\
CO,ETH,FORM,HNO3,ISOP,NO,NO2,O3,OLE,PAN,PAR,PRPA,SO2,XPAR $nc templateD2.nc
```
1. 暫時改變TFLAG維度的順序，將第一順位設成是VAR(其餘順序不影響結果)、並且令其為筆數維度(rec_dmn)：
```bash
ncpdq -O -a VAR,TSTEP,DATE-TIME $nc a;ncks -O --mk_rec_dmn VAR a $nc
```
1. 取出其中的特定的某一項(名稱定義在全域變數VAR-LIST)`ncks -O -d VAR,0,0 $nc a`，如為VAR49即為`ncks -O -d VAR,0,48 $nc a`
1. 使用ncrename來更改變數的名稱。如果2個變數名稱相同，仍然可以合併(後者會增加註釋)，然後續處理將更加複雜。
1. 如有擴充的必要，要先進行ncrcat(`file1 file2 file3`)，先將結果檔file3變數的個數增加。再進行實質的Append(`ncks -A file2 file3`)
1. 改回原來的維度順序。如果不改回來後續程式就讀不到TFLAG了。同時也要打開TSTEP成為筆數維度(rec_dmn)，讓TSTEP可以增加、延長。(倒不必特別做`--fix_rec_dmn`指令，因為不能同時有2個rec_dmn)：
```bash
ncpdq -O -a TSTEP,VAR,DATE-TIME a $nc
ncks -O --mk_rec_dmn TSTEP $nc a
mv a $nc
```
1. 修改全域屬性：因為`VAR-LIST`變數的`-`在python是保留的符號，不能成為變數的一部分，所以直接用bash指令是比較方便的作法。因變數個數改了，NVARS也需修改。
```bash
ncatted -a VAR-LIST,global,o,c,"AALJ            ACAJ            ACLI            ACLJ            ACLK            ACORS           AECI            AECJ            AFEJ            AISO3J          AKJ             AMGJ            AMNJ            ANAI            ANAJ            ANH4I           ANH4J           ANH4K           ANO3I           ANO3J           ANO3K           AOLGAJ          AOLGBJ          AORGCJ          AOTHRJ          APNCOMI         APOCI           APOCJ           ASEACAT         ASIJ            ASO4I           ASO4J           ASO4K           ASOIL           ASQTJ           CO              ETH             FORM            HNO3            ISOP            NO              NO2             O3              OLE             PAN             PAR             PRPA            SO2             XPAR            " $nc
ncatted -a NVARS,global,o,i,49 $nc
```
1. 因TFLAG第1個維度是變數(`[TSTEP,VAR,DATE-TIME]`)，而VAR的維度增加了，因此也需要填入日期及時間。

- tip
NVARS及VAR-LIST是CMAQ必讀屬性，一定要修到正確。NVARS為整數、VAR-LIST為A16序列(順序倒無所謂)
  - 產生VAR-LIST的程式碼:

```python
s=''
for v in V[3]:
  s+='{:16s}'.format(v)
```

## Reference

- czender, NCO NetCDF Operators, [NCO](https://github.com/nco/nco), 14 Jun 2014
- Charlie Zender, ncks(1) - Linux man page, [ncks](https://linux.die.net/man/1/ncks), 2010.
- lucasblog, [Software installation in CentOS 7 for scientific computation](https://wolfscie.wordpress.com/2015/04/01/software-installation-in-centos-for-scientific-computation/), April 1, 2015.

---
