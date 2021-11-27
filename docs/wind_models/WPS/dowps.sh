#!/bin/bash
#usage: dowps.cs m (m=0~11)
PATH1=$PWD
PATH2=/airappz/WRF4.1.3/NCEP

#cp -f $PATH1/namelist.wps.loop namelist.wps
#./geogrid.exe

yyyy=2019
i=$1
  ym=$(date -ud "${yyyy}-01-01 + ${i} month" +%Y%m)
  YY=$(date -ud "${yyyy}-01-01 " +%y)
  MM=$(date -ud "${yyyy}-01-01 + ${i} month" +%m)
  YP=$(date -ud "${yyyy}-${MM}-01 - 1 month" +%y)
  YN=$(date -ud "${yyyy}-${MM}-01 + 1 month" +%y)
  MP=$(date -ud "${yyyy}-${MM}-01 - 1 month" +%m)
  MN=$(date -ud "${yyyy}-${MM}-01 + 1 month" +%m)

  for pth in FNL SST;do
    cd ${PATH2}/$pth/
    mkdir -p $ym
    cd $ym
    ln -sf ../20$YP/*$YP${MP}1[5-9]* .
    ln -sf ../20$YP/*$YP$MP[23]* .
    ln -sf ../20$YY/*$YY$MM* .
    ln -sf ../20$YN/*$YN${MN}0[123456]* .
  done

ii=$(printf "%02d" $(( $i + 1 )) )
echo "ii:"$ii
mkdir -p $PATH1/WPS$ii
cd $PATH1/WPS$ii
cp -f $PATH1/namelist.wps.loop namelist.wps
for cmd in "s/YN/"$YN/g  "s/YP/"$YP/g  "s/MN/"$MN/g  "s/MP/"$MP/g  ;do sed -i $cmd namelist.wps;done
sed -i "s/PREWD/FILE/g" namelist.wps
./link_grib.csh $PATH2/FNL/$ym/fnl* .
ln -sf ./ungrib/Variable_Tables/Vtable.GFS Vtable
./ungrib.exe

cp -f $PATH1/namelist.wps.loop namelist.wps
for cmd in "s/YN/"$YN/g  "s/YP/"$YP/g  "s/MN/"$MN/g  "s/MP/"$MP/g  ;do sed -i $cmd namelist.wps;done
sed -i "s/PREWD/SST/g" namelist.wps
./link_grib.csh  $PATH2/SST/$ym/rtg_sst* .
ln -sf $PATH1/ungrib/Variable_Tables/Vtable.SST Vtable
./ungrib.exe

./metgrid.exe

mkdir -p $PATH1/$ym/met
mkdir -p $PATH1/$ym/SST_FILE

cp met_em*nc $PATH1/$ym/met
cp  FILE:20* $PATH1/$ym/SST_FILE
cp  SST:20* $PATH1/$ym/SST_FILE
