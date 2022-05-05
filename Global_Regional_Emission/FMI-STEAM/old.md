---
layout: default
title: 船隻排放之處理_CAMx
parent:  Ship Traffic Emission Assessment Model
grand_parent: Global/Regional Emission
nav_order: 1
date: 2022-02-05 10:26:07
last_modified_date: 2022-02-05 10:26:11
---

# 全球船隻排放量之處理_CAMx
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
- 船隻排放量不單在港口局部地區對空氣品質造成影響，也在公海等空曠領域造成背景空氣品質的差異，因此不論是哪一個解析度層面，船隻排放都非常的重要。
- 有鑒於此，國際間對船隻排放多所研究。其中以芬蘭氣象研究所對全球的推估結果最具規模也最多引用，因此，本項作業乃以該資料庫為對象，進行解讀、轉檔、應用於空氣品質模擬。
- 此處應用CAMx的前處理程式：
  - nc2m3、以及
  - 後處理程式slim、cbin等，
  - 最後應用python程式加進CMAQ面排放源裏。
- mozart2camx程式中會將mozart的濃度單位(重量混合比)轉camx的濃度單位(ppm)，公式 VMR = 28.9644 / mw * 1e6 * MMR 可以參考ecmwf網站。(詳下述)

## Sources
- Data

```
https://en.ilmatieteenlaitos.fi/surveying-maritime-emissions
http://www.globemission.eu/steam/data/NOx_allHeights_2015-01-01T00_2015-12-31T00.nc (not available)
```

- 工作目錄位置

```
kuang@114-32-164-198 /Users/TEDS/MACMIP/RadioForce8.5/ships
kuang@master /nas1/TEDS/en.ilmatieteenlaitos.fi/surveying-maritime-emissions
```

- Examples

```
https://safety4sea.com/new-study-reveals-shipping-pollution-hotspots-using-ais-data/
https://ars.els-cdn.com/content/image/1-s2.0-S1352231017305563-gr4_lrg.jpg
```

- 實際上網站並未提供所有污染項目，僅有NOx，因此還需要用排放比例來轉換。

## 工作步驟
### 檔案切割準備
- 由於檔案為等間距經緯度系統，可以用ncks進行裁切。
- NOx_east_asia.nc History

```bash
/home/nco-4.6.9/src/nco/.libs/lt-ncks -O -d latitude,314,827 -d longitude,3013,3677 NOx_allHeights_2015-01-01T00_2015-12-31T00.nc 
```

### NOx_east_asia.nc History
- Wed Dec 25 17:21:14 2019: /home/nco-4.6.9/src/nco/.libs/lt-ncks -O -d latitude,314,827 -d longitude,3013,3677 - NOx_allHeights_2015-01-01T00_2015-12-31T00.nc NOx_east_asia.nc
- odel version: STEAM 3.3.0 (JAVA, edited 31.1.2017)" ;
-                 :references = "Jalkanen, J.-P. ,Johansson, L., et al. 2012. Extension of an assessment model of ship traffic - exhaust emissions for particulate matter and carbon monoxide" ;
-                 :title = "modelled shipping exhaust emissions and statistics in WorldPool_CUSTOMaccording to STEAM model" ;
-                 :info = "emission values describe emissions released at stack height between 0 and 100." ;
-                 :NCO = "4.6.9" ;

### 主程式
nox_all2.py
單位由kg/日/網格→g/hr/km^2 (CMAQ emis in second, CAMx emis in hour)
- 由於MMR轉成MMV或粒狀物時，乘上不同轉換因子(氣狀物 VMR = 28.9644 / mw * 1e6 * MMR 單位為ppm、粒狀物ug/M3=MMR* 1e9 / (g/M3_air) )，
- 在1013.25 hPa和15°C時，空氣的密度大約為1225 g/m³

```python
from pandas import *
import datetime
import netCDF4
import numpy as np
import os,sys


pi=3.14159265359
peri_x=40075.02 #Km
peri_y=40008
r_x=peri_x/2./pi
r_y=peri_y/2./pi

#讀取NOx排放量
path=''
fname=path+'NOx_east_asia.nc'
nc = netCDF4.Dataset(fname,'r')
NOx=np.array(nc.variables['NOx'][:,:,:])
lst={'lat':list(nc.variables['latitude'][:])}
lst.update({'lon':list(nc.variables['longitude'][:])})
lst.update({'time':[i for i in range(31)]})

#讀取過去各物質加總結果，與NOx的比例，將乘上NOx ship排放量，來推估其他物質的排放量
df=read_csv('shp_sum.csv')
dfs=read_csv('shp_moz.csv')
dfs.iloc[0,0]='1,3,5-trimethylbenzene'
col=['spec','moz','mw']
dfs.columns=col
spec=list(dfs.spec);moz=list(dfs.moz);mw=list(dfs.mw)
spz={i:j for i,j in zip(spec,moz)}
mws={i:j for i,j in zip(spec,mw)}
nrow,ncol=(514,665)
dlon=(max(lst['lon'])-min(lst['lon']))/(ncol-1)
dlat=(max(lst['lat'])-min(lst['lat']))/(nrow-1)
prs=np.ones (shape=(31,nrow,ncol))*101806.9
tmK=np.ones (shape=(31,nrow,ncol))*298.

#計算(LL)各網格的面積
area=np.zeros(shape=(31,nrow,ncol))
for j in range(nrow):
  rad=abs(lst['lat'][j]/90.)*pi/2.
  r=(r_x*np.cos(rad)+r_y*np.sin(pi/2.-rad))/2.
  dx=2.*pi*r * dlon/360.
  dy=dlat/180.*(peri_x*np.cos(rad)**2+peri_y*np.sin(rad)**2)/2.
  for i in range(ncol):
    area[:,j,i]=[dx*dy for t in range(31)]
#print (np.max(area))
#sys.exit('area.txt')
#with open('area.txt','w') as f:
#  for j in range(nrow):
#    for i in range(ncol):
#      f.write(str(i)+' '+str(j)+' '+str(area[j,i])+'\n')

tmp=netCDF4.Dataset('frame.nc','r')
f48={'time':'f8', 'lat':'f4', 'lon':'f4'}
fi4={'P0':'f4', 'mdt':'i4', 'mhisf':'i4'}

#寫出每個月的nc檔案
for m in range(1,13):
  mm='{:02d}'.format(m)
  fname=path+'shp_east_asia'+mm+'.nc'
  #gregoria date
  lst.update({'time':[(datetime.datetime(2015,m,1)+datetime.timedelta(days=d)).toordinal() for d in range(31)]})

  if not os.path.isfile(fname):
    f = netCDF4.Dataset(fname,'w')
    f.createDimension('lat',nrow)
    f.createDimension('lon',ncol)
    f.createDimension('time',31)
    f.createDimension('lev',1)
    f.createDimension('ilev',2)
#   constants
    for s in ['P0', 'mdt', 'mhisf']:
      f.createVariable(s,fi4[s],dimensions=())
      f.variables[s][:]=tmp.variables[s][:]
      f.variables[s].long_name=tmp.variables[s].long_name
      if s=='mdt':f.variables[s][:]=[3600]

#   one dimension
    for s in ['time', 'lat', 'lon']:
      f.createVariable(s,f48[s],( s,))
      f.variables[s][:]=lst[s][:]
      f.variables[s].long_name=tmp.variables[s].long_name
      f.variables[s].units=tmp.variables[s].units
      if s=='time': f.variables[s].calendar=tmp.variables[s].calendar
    for s in ['ilev','lev']:
      f.createVariable(s,'f4',( s,))
      f.variables[s][:]       =tmp.variables[s][:]
      f.variables[s].long_name=tmp.variables[s].long_name
      f.variables[s].units    =tmp.variables[s].units
      f.variables[s].positive =tmp.variables[s].positive
      f.variables[s].A_var    =tmp.variables[s].A_var
      f.variables[s].B_var    =tmp.variables[s].B_var
      f.variables[s].P0_var   =tmp.variables[s].P0_var
      f.variables[s].PS_var   =tmp.variables[s].PS_var
      f.variables[s].bounds   =tmp.variables[s].bounds
    for s in ['date', 'datesec']:
      f.createVariable(s,'i',( 'time',))
      f.variables[s].long_name=tmp.variables[s].long_name
      if s=='date':
        f.variables[s][:]=[int((datetime.datetime(2015,m,1)+datetime.timedelta(days=d)).strftime('%Y%m%d')) for d in range(31)]
      else:
        f.variables[s][:]=[int(0) for d in range(31)]
        f.variables[s].units    =tmp.variables[s].units

#   three dimensions
    for s in ['PS']:
      f.createVariable(s,'f4',( 'time', 'lat', 'lon', ))
      f.variables[s][:,:,:]=prs[:,:,:]
      f.variables[s].units    =tmp.variables[s].units

#   four dimensions
    for s in set(moz):
      if s=='None':continue
      f.createVariable(s,'f4',( 'time', 'lev', 'lat', 'lon', ))
      f.variables[s].units    = "g/KM^2/hr"
    s='T'
    f.createVariable(s,'f4',( 'time', 'lev', 'lat', 'lon', ))
    f.variables[s].long_name = "T               "
    f.variables[s].units = "K               "
    f.variables[s].var_desc = "temperature"
    f.variables[s][:,0,:,:]=tmK[:,:,:]
  else:
    f = netCDF4.Dataset(fname,'r+')

  for s in set(moz):
    if s=='None':continue
    f.variables[s][:,0,:,:]=np.zeros(shape=(31,nrow,ncol))

  j0=(datetime.datetime(2015,m,1)-datetime.datetime(2015,1,1)).days
  dfm=df.loc[(df.mon==m)].reset_index(drop=True)
  vNOx=list(dfm.loc[dfm.spec=='NOx','sum_file'])[0]
  if vNOx==0.:sys.exit('vNOx==0')
  for s in spec:
    if spz[s]=='None': continue
    fac=list(dfm.loc[dfm.spec==s,'sum_file'])[0]/vNOx
    if s=='NOx': fac=1.
    fac=fac*1000./24
    f.variables[spz[s]][:,0,:,:]+=NOx[j0:j0+31,:,:]/area*fac
  f.close()
```

### 改變解析度(reso.py)
- 由於mz2camx程式是採grab sample的方式，如果是線源、點源這類不連續場，倘若解析度差異很大，在切割時如果沒有被挑到，在質量上將會出現顯著的落差，因此除了原本的解析度(足夠d4)之外，還要預備給81K、27K解析度的檔案。
先執行前述nox_all2.py 產生path+'shp_east_asia'+mm+'.nc' 後，再執行本程式。將會執行12個月、逐日排放量檔fnameO=fname.replace('.nc','_'+str(xcell)+'.nc') ，xcell=3 or 9。
以目前約9Km的解析度，還要再pile-up 3倍與9倍，以供d2及d1所用。
- 準備_3與_9的經緯度座標值(line 15~23)，由於此段是每個月都相同，只需要做一次即可。因降低解析度，網格範圍的東、北界限可能會損失，因此除了正規的範圍之外，另向外擴張2格，一共增加了5格。
- 每月的迴圈line 24~先將所有5維的變數記下備用(line 30)
- _3、_9不同解析度的迴圈(line 31~)：切割出所要尺寸的模版(line 36)儲存前述預製好的經緯度座標值
- 污染項目的迴圈(line 40~)
  - 用「疊影法」方式來進行網格的相加。雖然會多計算很多不必要的網格點，但「切勿」用j,i 迴圈逐一來做，會花很多時間。
  - 最後回存時用跳島式迴圈方式即可正確取到加總結果，回存時記得預留最外圈2層是擴張層。(可能會保留模版原有的數值)因為原檔案是按細網格面積來得到單位面積結果，加總後要更新基底面積(即為原來的xcell^2倍)
- 注意nc檔案並不適用np.array的fancy indexing
  - 詳[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)
  
```python
kuang@114-32-164-198 /Users/TEDS/MACMIP/RadioForce8.5/ships
$ cat -n reso.py
     1
     2  import netCDF4
     3  import numpy as np
     4  import os
     5
     6  NCO='/cluster/netcdf/bin/'     #@master
     7  NCO='/opt/anaconda3/bin/'     #@IMac
     8  path=''
     9  fname=path+'shp_east_asia01.nc'
    10  nc = netCDF4.Dataset(fname,'r')
    11  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    12  nv=len(V[3])
    13  nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
    14  var=np.zeros(shape=(nv,nt,nrow,ncol))
    15  lat,lon={},{}
    16  for xcell in [3,9]:
    17    i3=ncol//xcell+1
    18    j3=nrow//xcell+1
    19    dx=nc.variables['lon'][xcell]-nc.variables['lon'][0]
    20    dy=nc.variables['lat'][xcell]-nc.variables['lat'][0]
    21    xorg,yorg=nc.variables['lon'][0]-dx*2,nc.variables['lat'][0]-dy*2
    22    lon.update({xcell:np.array([xorg+dx*i  for i in range(i3+4)])})
    23    lat.update({xcell:np.array([yorg+dy*j  for j in range(j3+4)])})
    24  for m in range(1,13):
    25    mm='{:02d}'.format(m)
    26    fname=path+'shp_east_asia'+mm+'.nc'
    27    nc = netCDF4.Dataset(fname,'r')
    28    for iv in range(nv):
    29      v=V[3][iv]
    30      var[iv,:,:,:]=nc.variables[v][:,0,:,:]
    31    for xcell in [3,9]:
    32      i3=ncol//xcell+5
    33      j3=nrow//xcell+5
    34      a3,b3=str(i3),str(j3)
    35      fnameO=fname.replace('.nc','_'+str(xcell)+'.nc')
    36      os.system(NCO+'ncks -O -d lat,1,'+b3+' -d lon,1,'+a3+' '+fname+' '+fnameO)
    37      nc1= netCDF4.Dataset(fnameO,'r+')
    38      nc1.variables['lat'][:]=lat[xcell]
    39      nc1.variables['lon'][:]=lon[xcell]
    40      for iv in range(nv):
    41        zz=var[iv,:,:,:]
    42        zz[:,1:-1,1:-1]=0.
    43        for j in range(1,xcell+1):
    44          for i in range(1,xcell+1):
    45            zz[:,:-j,:-i]+=var[iv,:,j:,i:]
    46        nc1.variables[v][:,0,2:-2,2:-2]=zz[:,:nrow:xcell,:ncol:xcell]/xcell/xcell
    47      nc1.close()
    48
```

## 後處理
- (nc->m3->uamiv->cmaq_emis)
- nc:等間距經緯度座標系統
- m3:model3 IOAPI直角座標系統
- uamiv: for CAMx simulation
- cmaq_emis: for CMAQ simulation

### nc2m3.cs
- 此步驟將等間距經緯度座標系統，轉換成m3io之直角座標系統
- 「shp_east_asia*.nc」會將所有檔案進行轉換，如果只要_3或_9檔案，可以予以明確化：
  - _3:     shp_east_asia*_3.nc
  - _9:     shp_east_asia*_9.nc

```bash
kuang@114-32-164-198 /Users/TEDS/MACMIP/RadioForce8.5/ships
$ cat nc2m3.cs
export EXECUTION_ID=mz2camx.job
export PROMPTFLAG=N
export IOAPI_ISPH=20

EXE=/Users/camxruns/src/mozart2camx_v3.2.1/ncf2ioapi_mozart/NCF2IOAPI
for res in 3 9;do
for i in $(ls shp_east_asia*_${res}.nc|cut -d'.' -f1) ;do
  export INFILE=${i}.nc
  export OUTFILE3D=${i}.m3.nc
  echo $i
  $EXE|tail -n5
done
done
```

### par.cs
- performed the nz2camx.job(切割domain)+(改成直角座標系統)
- 由於mz2camx.job進行過程的輸入、輸出檔案名稱是固定的，一次只能進行一個月檔案的計算，因此如果要平行運作，必須開12個月的目錄分別進行計算。
- 同理、d1~d4也不能同一目錄進行計算，必須分開計算，
- 同時也必須限定最多同時執行的個數否則電腦CPU也不夠這麼多job同時計算
- d1搭配_9(約81k)、d2搭配_3(約27k)、d3、d4則為原解析度
- mz2camx.job的內容另外說明如下
- mozart2camx 會將輸入內容按成分進行MMR->VMR(ppm)轉換

```bash
kuang@114-32-164-198 /Users/TEDS/MACMIP/RadioForce8.5/ships
$ cat par.cs
EXE=mz2camx
for d in 1 2;do for i in 0{1..9} 1{0..2};do mkdir -p ships${i}_$d;done;done
for d in 1 2;do for i in 0{1..9} 1{0..2};do cd ships${i}_$d;ln -sf ../output .;cd ..;done;done
for d in 1 2;do
  s=9
  test $d == 2 && s=3
  for i in 0{1..9} 1{0..2};do
      while true;do
        n=$(psg ${EXE}|wc -l)
        if [ $n -lt 12 ];then
          cd ships${i}_$d;sub ../mz2camx.job 15$i d$d ../shp_east_asia${i}_${s}.m3.nc >&mz2camx.log ;cd ..
          break
        else
          sleep 1s
        fi
      done
  done
done
```

### mz2camx.job
```bash
#!/bin/csh -f
#$1->yymm
#$2->m3.nc
setenv PROMPTFLAG N
setenv IOAPI_ISPH 20
set EXE = /Users/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6_CF__NCEP

set YYMM = $1
set d = $2
set OU = `echo $3|cut -d'.' -f1`
set MM = `echo $YYMM|cut -c 3-4`
set YY = `echo $YYMM|cut -c 1-2`
if ( $MM == 12) then
        @ YN   = $YY + 1
        @ YYMN = $YN * 100 + 1
else
        @ YYMN = $YYMM + 1
endif
if ( $MM == 01 ) then
        @ YP = $YY - 1
        @ YYMP = $YP * 100 + 12
else
        @ YYMP = $YYMM - 1
endif

set MET = /Users/WRF4.1/WRFv3/201909/wrfout/1909U$d

# DEFINE OUTPUT FILE NAMES
setenv EXECUTION_ID mz2camx.job
setenv OUTFILEBC  $YYMM$d".bc."$OU
mkdir -p ./output
foreach i ( 0 1 2 3 )
foreach j ( 0 1 2 3 4 5 6 7 8 9 )
if ( $i == '3' && $j > '1' ) goto BYPASS
set k = $i$j
if ( $k == '00' ) goto BYPASS
set DATE = "20"$YYMM$k
#set DATE = "0912"$k

# DEFINE INPUT MOZART FILES
# IF MORE THAN 1 MOZART FILE IS NEEDED, ADD setenv INFILE2
set NINFILE = 1
foreach t ( 00 )
foreach INFILE ($3)
setenv INFILE1 $INFILE
#if ( -e $OUTFILEIC ) goto BYPASS2

echo $DATE$t
set YYYYMMDD = $DATE
setenv OUTFILEIC  output/$YYYYMMDD$d"."$OU
echo $OUTFILEIC
rm -f $OUTFILEBC $OUTFILEIC
$EXE << IEOF
CAMx5,CAMx6,CMAQ   |CAMx 6
ProcessDateYYYYMMDD|$YYYYMMDD
Output BC file?    |.false.
Output IC file?    |.true.
If IC, starting hr |$t
Output TC file?    |.false.
Max num MZRT files |$NINFILE
CAMx 3D met file   |$MET.3d
CAMx 2D met file   |$MET.2d
IEOF
mv OUTFILEIC $OUTFILEIC
echo $INFILE1
BYPASS2:
      end
      end
BYPASS:
end
end
exit 0
```

### mz2camx_node03.job
- (only diff in $EXE and $MET locations, seems not used)
```bash
$ diff mz2camx_node03.job mz2camx.job
8c8
< set EXE = ~/mac/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6_CF__NCEP_node03
---
> set EXE = /Users/camxruns/src/mozart2camx_v3.2.1/src/mozart2camx_CB6_CF__NCEP
29c29
< set MET = ~/mac/WRF4.1/WRFv3/201909/wrfout/1909U$d
---
> set MET = /Users/WRF4.1/WRFv3/201909/wrfout/1909U$d
```

### slm.cs
- 運用pncgen 來修改uamiv檔案mz2camx結果會仿照WRF2CAMx結果的空間設定，因為是3維的，檔案過大必須縮減。uamiv格式可以使用pncgen切割維度(高度LAY)因為mozart基本上是處理空氣品質，在NAME的屬性是"AIRQUALITY"，必須改成"EMISSIONS "，否則CAMx會跳出來。
- 可以在同一目錄下平行運作

```bash
EXE=pncgen
for D in d{1..4};do
  for da in 0{1..9} {10..31};
    do for mn in 0{1..9} 1{0..2};do
      while true;do
        n=$(psg ${EXE}|wc -l)
        if [ $n -lt 12 ];then
          fname=2015${mn}${da}${D}.
          fnameo=${fname}L
          sub ${EXE} --format=uamiv -O --out-format=uamiv --slice=LAY,0 -a NAME,global,o,c,'EMISSIONS ' $fname $fnameo>&/dev/null
#         sleep 1s
          break
        else
          sleep 1s
        fi
      done
    done
  done
done
```

### cbl.cs
- 將逐日、地面檔案組合成月檔案。結果會是2015${m}.emis.grd0${d}，uamiv檔案，可以直接加入CAMx模擬、或經camx2cmaq轉換後加到CMAQ排放量檔案裏。
- 有暫存檔，「不能」在同一目錄平行運作

```bash
for d in 1 2 3 4;do
  for m in 0{1..9} 1{0..2};do
    cbin_all "2015${m}??d${d}.L" "2015${m}.emis.grd0${d}">&/dev/null
  done
done
```
cbin_all 為傳統uamiv檔案的連接程式，功能與ncrcat之基本功能相同，詳見 https://github.com/sinotec2/CAMx_utility/blob/master/cbin_avrg.par.f

### add_Ship.py
- 加入既有的area.nc 檔案
  - 執行範例：add_SO20.py 01 02(1601月第2層網格)
  - 逐月檔案之單位尚未轉換成正確單位，仍為mz2camx之結果(PPM)，除了分子量外，其餘皆需還原。(fac, line35)
  - 由於mar_path+'2015'+mo+'.emis.grd'+gd 為d0範圍(59*59)，與d1(53*53)差了6格，分別由四個方向的外圈扣除。(line66~68、78、80)
  - 結果檔案名稱為'fortBE.'+gd[1]+'13.teds10.base'+mo+'S.nc'，S for Ship(line 54)
  - NO<sub>2</sub>佔NOx重量的1/10、NO佔NOx重量的9/10
  - 因資料庫涵括了內陸水運的排放，對臺灣地區而言，似為干擾而非貼近實況，需要去除，因此導入gridmask中對海域之定義(line 41~51)只在d04中反映，其他範圍解析度不考慮d04會有頭尾時間不足的問題，在此一併檢查處理。

```python
kuang@master /nas1/cmaqruns/2016base/data/emis
$ cat -n /home/kuang/mac/cmaqruns/2016base/data/emis/add_Ship.py
     1  #!/cluster/miniconda/envs/py37/bin/python
     2  import numpy as np
     3  import netCDF4
     4  import os,sys,subprocess
     5  from PseudoNetCDF.camxfiles.Memmaps import uamiv
     6  import datetime
     7
     8  def dt2jul(dt):
     9    yr=dt.year
    10    deltaT=dt-datetime.datetime(yr,1,1)
    11    deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
    12    return (yr*1000+deltaT.days+1,deltaH*10000)
    13
    14  def jul2dt(jultm):
    15    jul,tm=jultm[:]
    16    yr=int(jul/1000)
    17    ih=int(tm/10000.)
    18    return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)
    19
    20
    21  root=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    22  mar_path='/'+root+'/TEDS/en.ilmatieteenlaitos.fi/surveying-maritime-emissions/output/'
    23  km2={'01':81*81,'02':27*27,'04':3*3}
    24  mo=sys.argv[1];gd=sys.argv[2]
    25  fname=mar_path+'2015'+mo+'.emis.grd'+gd
    26  marf = uamiv(fname,'r')
    27  V=[list(filter(lambda x:marf.variables[x].ndim==j, [i for i in marf.variables])) for j in [1,2,3,4]]
    28  Vm=[]
    29  for x in V[3]:
    30    if x in ['SO2','NO2','NO']:continue
    31    if np.sum(marf.variables[x][:])==0.:continue
    32    Vm.append(x)
    33  ntm,nlaym,nrowm,ncolm=marf.variables['SO2'].shape
    34  #yjhm=[i*100+int(j/10000) for i,j in zip(marf.variables['TFLAG'][:,0,0],marf.variables['TFLAG'][:,0,1])]
    35  fac=28.9644*10**6/km2[gd]# (gmole/hour)
    36  SO2=np.array(marf.variables['SO2'][:,:,:,:])/fac
    37  NO2=np.array(marf.variables['NO2'][:,:,:,:])/fac *0.1
    38  NO=np.array(marf.variables['NO2'][:,:,:,:])/fac *0.9
    39  
    40  marine=np.ones(shape=(nrowm,ncolm))
    41  if gd=='04':
    42    fnameL='/'+root+'/cmaqruns/2016base/data/land/epic_festc1.4_20180516/gridmask/TWN_CNTY_3X3.nc'
    43    ncL = netCDF4.Dataset(fnameL,'r+')
    44    V=[list(filter(lambda x:ncL.variables[x].ndim==j, [i for i in ncL.variables])) for j in [1,2,3,4]]
    45    marine=marine*0.
    46    for v in V[3]:
    47      if len(v)==2:
    48        marine[:,:]+=ncL.variables[v][0,0,:,:]
    49    idx=np.where(marine==0.) #take the marine indices
    50    marine=marine*0.         #reset the matrix
    51    marine[idx[0],idx[1]]=1. #only marine grids are one's
    52
    53  fname='fortBE.'+gd[1]+'13.teds10.base'+mo+'.nc'
    54 fnamO='fortBE.'+gd[1]+'13.teds10.base'+mo+'S.nc'
    55  os.system('cp '+fname+' '+fnamO)
    56  nc = netCDF4.Dataset(fnamO,'r+')
    57  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    58  nt,nlay,nrow,ncol=nc.variables['SO2'].shape
    59  nv=len(V[3])
    60  ib,jb=0,0
    61  if nlay!=nlaym or ncol!=ncolm or nrow!=nrowm:
    62    if nlay!=nlaym:sys.exit('shape not right')
    63    if nrowm>nrow:jb=int((nrowm-nrow)/2)
    64    if ncolm>ncol:ib=int((ncolm-ncol)/2)
    65    SO2=SO2[:,:,jb:-jb,ib:-ib]
    66    NO2=NO2[:,:,jb:-jb,ib:-ib]
    67    NO =NO [:,:,jb:-jb,ib:-ib]
    68    marine=marine[jb:-jb,ib:-ib]
    69  #yjh=[i*100+int(j/10000) for i,j in zip(nc.variables['TFLAG'][:,0,0],nc.variables['TFLAG'][:,0,1])]
    70  for t in range(nt):
    71    it=int(t/24)%ntm
    72    nc.variables['SO2'][t,:,:,:]+=SO2[it,:,:,:]*marine[:,:]
    73    nc.variables['NO' ][t,:,:,:]+=NO [it,:,:,:]*marine[:,:]
    74    nc.variables['NO2'][t,:,:,:]+=NO2[it,:,:,:]*marine[:,:]
    75    for v in Vm:
    76      if v not in V[3]:continue
    77      if ib+jb==0:
    78        nc.variables[v][t,:,:,:]+=np.array(marf.variables[v][it,:,:,:]*marine[:,:])/fac
    79      else:
    80        nc.variables[v][t,:,:,:]+=np.array(marf.variables[v][it,:,jb:-jb,ib:-ib]*marine[:,:])/fac          
    81  #checking the beginning STIME, must begion at 0 UTC
    82 dend=jul2dt(list(nc.variables['TFLAG'][nt-1,0,:]))
    83  tb=int(nc.STIME/10000)
    84  if tb!=0:
    85    nc.STIME=0.
    86    var=np.zeros(shape=(nv,nt,nrow,ncol))
    87    for iv in range(nv):
    88      var[iv,:,:,:]=nc.variables[V[3][iv]][:,0,:,:]
    89    tflag=nc.variables['TFLAG'][:,0,:]
    90    for t in range(0,tb):
    91      nc.variables['TFLAG'][t,:,0]=[nc.SDATE for i in range(nv)]
    92      nc.variables['TFLAG'][t,:,1]=[t*10000. for i in range(nv)]
    93      tt=t-tb+24
    94      for iv in range(nv):
    95        nc.variables[V[3][iv]][t,0,:,:]=var[iv,tt,:,:]
    96
    97    for t in range(tb,tb+nt):
    98      tt=t-tb
    99      nc.variables['TFLAG'][t,:,0]=[tflag[tt,0] for i in range(nv)]
   100      nc.variables['TFLAG'][t,:,1]=[tflag[tt,1] for i in range(nv)]
   101      for iv in range(nv):
   102        nc.variables[V[3][iv]][t,0,:,:]=var[iv,tt,:,:]
   103
   104  #check the last day or run12
   105  mo=int(mo)
   106  lastYr=(datetime.datetime(2016,mo,1)+datetime.timedelta(days=-1)).year
   107  lastMo=(datetime.datetime(2016,mo,1)+datetime.timedelta(days=-1)).month
   108  begd=datetime.datetime(lastYr,lastMo,15)
   109  endd=begd+datetime.timedelta(days=48)
   110  if endd<=dend:          #in case of more than 48 days(run12)
   111    nc.close()
   112    sys.exit('endj check ok')
   113  else:                   #duplicating the last day
   114    delH=int((endd-dend).total_seconds()/3600.)+1
   115    for h in range(delH):
   116      SDATE=dt2jul(dend+datetime.timedelta(days=+(h+1)/24.))
   117      t=nt+h+tb
   118      for j in range(2):
   119        nc.variables['TFLAG'][t,:,j]=[SDATE[j]  for i in range(nv)]
   120      tt=t-24
   121      for k in range(5):  #prevention greater than nt
   122        if tt>=nt:tt=tt-24
   123      for iv in range(nv):
   124        nc.variables[V[3][iv]][t,0,:,:]=var[iv,tt,:,:]
   125    nc.close()
```

## 排放量之調整
- 船舶排放量除NO<sub>2</sub>之外，其餘污染項目為NO<sub>2</sub>之一定比例來估算，因此不確定性很高，調整時可以用python進行一次性之乘除，如下：
  - d1、d2模擬結果比對，SO2的GE約是1.8~2.8，表示原排放量需除2.8~3.8。

```python
from PseudoNetCDF.camxfiles.Memmaps import uamiv
fname='fortBE.113_STEAM.base01_S1.8'
nc= uamiv(fname,'r+')
nc.variables['SO2'][:]=nc.variables['SO2'][:]/2.8
nc.close()
fname='fortBE.213_STEAM.base01_S2.8'
nc.variables['SO2'][:]=nc.variables['SO2'][:]/3.8
nc.close()
```

### 檢視成果
1月份平均NOx排放量及run5平均SO2空品模擬結果。



## Reference
- Lasse Johansson, Jukka-Pekka Jalkanen, Jaakko Kukkonen, **Global assessment of shipping emissions in 2015 on a high spatial and temporal resolution**, [Atmospheric Environment](https://www.sciencedirect.com/science/article/pii/S1352231017305563)
- CAMx(UAM)的檔案格式, Yungchuan Kuang edited this page on 12 Jul 2016 · 2 revision, shttps://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式
- 發表文獻[STEAM_reference_list_update_22012018](https://en.ilmatieteenlaitos.fi/documents/30106/42382/STEAM_reference_list_22012018.pdf/a340344c-8b05-4d10-be6f-287b54c53b3e)

## Appendix
- Convert mass mixing ratio (MMR) to mass concentration or to volume mixing ratio (VMR) [confluence.ecmwf](https://confluence.ecmwf.int/pages/viewpage.action?pageId=153391710)
Ship Traffic Emission Assessment Model ([STEAM](http://www.temis.nl/globemission/docs/workshop_2015/STEAM-GlobEmissions_Connection.pdf))

```bash
For O<sub>3</sub>, the formula is: VMR = 28.9644 / 47.9982 * 1e6 * MMR
For CO the formula is: VMR = 28.9644 / 28.0101 * 1e6 * MMR
For NO2 the formula is: VMR = 28.9644 / 46.0055 * 1e6 * MMR
For SO2 the formula is: VMR = 28.9644 / 64.0638 * 1e6 * MMR
For CO2 the formula is: VMR = 28.9644 / 44.0095 * 1e6 * MMR
For CH4 the formula is: VMR = 28.9644 / 16.0425 * 1e6 * MMR
```

- mz2camx會將檔案內容乘上10^6(粒狀物乘上10^9)，因此必須在某個時間點將其除回來。
- 理論上CDO可以達成作業要求，但似力有未逮。最後仍然適用python程式完成此項作業。

```bash
CDO=/usr/local/bin/cdo
YY=15
for MM in 0{1..2};do # 151{0..2};do
  nc=shp_east_asia$MM.m3.nc
  $CDO -O selvar,OC1,BC1 $nc tmp1.nc
  $CDO -O divc,1000000000 tmp1.nc tmp2.nc
  $CDO -O replace $nc tmp2.nc tmp3.nc

  $CDO -O selvar,BIGENE,C3H8,BENZ,C2H6,C2H4,CH4,C3H6,BIGALK,CO,TOLUENE,XYL,NO2,BIGALD,SO2,C4H10 $nc tmp1.nc
  $CDO -O divc,1000000 tmp1.nc tmp2.nc
  $CDO -O replace tmp3.nc tmp2.nc tmp4.nc

  for D in d1 d2;do
    YYMM=$YY$MM
    mz2camx.job $YYMM $D tmp4.nc
  done
done
```
