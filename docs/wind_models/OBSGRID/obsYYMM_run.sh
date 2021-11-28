#!/usr/local/bin/bash
#usage: obsYYMM_run.cs 1304 5
path=/Users/WRF4.3/OBSGRID
ym=$1
j=$2
ln -sf $path/../WPS/20$ym/met/met_em* .
begd=$(date -v-1m -j -f "%Y%m%d" "20${ym}15" +%Y%m%d)
dd=`echo "4*($j-1)"|bc -l`
ymd1=$(date -v+${dd}d -j -f "%Y%m%d" "${begd}" +%Y%m%d)
ymd2=$(date -v+5d     -j -f "%Y%m%d" "${ymd1}" +%Y%m%d)
yea1=`echo $ymd1|cut -c1-2`;mon1=`echo $ymd1|cut -c3-4`;day1=`echo $ymd1|cut -c5-6`
yea2=`echo $ymd2|cut -c1-2`;mon2=`echo $ymd2|cut -c3-4`;day2=`echo $ymd2|cut -c5-6`

for d in {1..4};do #domain
#copy the template and change the beg/end dates by sed
  cp -f $path/namelist.oa.loop namelist.oa
  for cmd in   "s/SYEA/20$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" \
    "s/GID/$d/g" "s/EYEA/20$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g";do
    sed -ie $cmd namelist.oa
  done

#execution the programs
  $path/src/obsgrid$d.exe
  $path/run_cat_obs_files.csh $d
  $path/../FILTER/filter_p $d
done

#store the results
mkdir -p $path/20$ym/run$j
mv -f metoa_em* OBS_DOMAIN* wrfsfdda* $path/20$ym/run$j

