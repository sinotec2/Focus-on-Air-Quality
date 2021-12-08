#!/usr/local/bin/bash
PATH1=/Users/WRF4.3
PATH2=/Users/WRF4.3/OBSGRID
# working directory path name contains YYYYMM in the fourth section
ym=`echo $PWD|cut -d'/' -f4|cut -c3-6`
begd=$(date -v-1m -j -f "%Y%m%d" "20${ym}15" +%Y%m%d)
for j in {1..12};do
  dd=`echo "4*($j-1)"|bc -l`
  ymd1=$(date -v+${dd}d -j -f "%Y%m%d" "${begd}" +%Y%m%d)
  ymd2=$(date -v+5d     -j -f "%Y%m%d" "${ymd1}" +%Y%m%d)
  yea1=`echo $ymd1|cut -c1-2`;mon1=`echo $ymd1|cut -c3-4`;day1=`echo $ymd1|cut -c5-6`
  yea2=`echo $ymd2|cut -c1-2`;mon2=`echo $ymd2|cut -c3-4`;day2=`echo $ymd2|cut -c5-6`
  mkdir -p $PATH1/20$ym/run$j
  ln $PATH1/run/* $PATH1/20$ym/run$j
  cd $PATH1/20$ym/run$j
  ln -sf $PATH2/20$ym/run$j/metoa_em* .
  ln -sf $PATH2/20$ym/run$j/wrfsfdda* .
  for d in {1..4};do #domain
    ln -sf $PATH2/20$ym/run$j/OBS_DOMAIN$d"01p" OBS_DOMAIN$d"01"
  done
  cp -f $PATH1/20$ym/namelist.input.loop namelist.input
  for cmd in "s/SYEA/20$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" "s/SHOU/00/g"\
    "s/EYEA/20$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g" "s/EHOU/00/g";do
    sed -ie $cmd namelist.input
  done
  nohup ./real.exe&
done
