#kuang@master /nas1/backup/data/NOAA/NCEP/GFS/YYYY
#$ cat fcst_dev2.cs
wget=/usr/bin/wget
curl=/opt/anaconda3/bin/curl
root=https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.
today=$(date -d -0day +%Y%m%d)
yestd=$(date -d -1day +%Y%m%d)
yesty=$(date -d -1day +%Y)
BH=06
dir=$yestd/$BH/atmos/
gfs=/nas1/backup/data/NOAA/NCEP/GFS/YYYY
cmaq=/home/cmaqruns/2022fcst
fcst=/nas2/cmaqruns/2022fcst
BEGD=$(date -d "$today -0days" +%Y-%m-%d)
ENDD=$(date -d "$BEGD  +11days" +%Y-%m-%d)
dates=();datep=()
for id in {0..11};do
  dates=( ${dates[@]} $(date -d "$BEGD +${id}days" +%Y-%m-%d) )
  datep=( ${datep[@]} $(date -d "$BEGD +${id}days" +%Y%m%d) )
done
sub=~/bin/sub
DOM=( 'CWBWRF_45k' 'SECN_9k' 'TWEPA_3k' 'tw_CWBWRF_45k' 'nests3')
RES=( 45 09 03 )
GRD=( 'grid45'     'grid09'  'grid03' )

#CMAQ stream

for i in 2;do
  p=$(( $i - 1 ))
  nc=/nas2/cmaqruns/2022fcst/${GRD[$i]}/bcon/BCON_today_${DOM[$i]}
  cd $fcst
  while true;do
    if [[ -e $nc ]];then
      ~/bin/pr_tflag.py $nc >& tmp.txt
      bc_begd=$( cat tmp.txt|head -n1|awk '{print $3}' )
      if [[ $bc_begd == ${dates[0]} ]];then break;fi
    fi
    sleep 62
  done

  cd $fcst
  YYYYJJJ=$(date -d ${BEGD} +%Y%j)
  mcip_start=$BEGD
  mcip_end=$(date -d ${BEGD}+9days +%Y-%m-%d)
  cp project.config_loop project.config
  for cmd in 's/YYYYJJJ/'$YYYYJJJ'/g' \
           's/mcip_start/'$mcip_start'/g' \
           's/mcip_end/'$mcip_end'/g'; do
#          's/2400000/1200000/g';do
    sed -ie $cmd project.config
  done

  ii=$(echo ${GRD[$i]}|cut -c5-)
  cd $fcst
#  icon=$fcst/${GRD[$i]}/icon/ICON_yesterday_${DOM[$i]}
#  cgrd=$fcst/${GRD[$i]}/cctm.fcst/daily/CCTM_CGRID_v532_intel_${DOM[$i]}_${yestd}.nc
#  ymd=$(~/bin/j2c $(ncdump -h $icon|grep SDATE|awk '{print $3}'))
#  if [[ $ymd -ne ${datep[0]} ]];then
#    if [[ -e $cgrd ]];then
#      cp $cgrd $icon
#    else
#      exit 0
#    fi
#  fi

  csh ./run.cctm.${ii}.csh

  # combine PM's
  for id in {0..9};do
    nc=$fcst/${GRD[$i]}/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$i]}_${datep[$id]}.nc
    if [[ -e $nc ]];then ~/bin/sub $fcst/combine.sh $nc;fi
  done

  # cmaq to json
  r=${RES[$i]}
  cd /nas1/Data/javascripts/D3js/earthFcst$r/public/data/weather/current
  for id in {0..9};do ~/bin/sub ./cmaq_jsonByDay.py ${dates[$id]};done
  cd $fcst
done

i=2;p=1
f=()
for id in {0..9};do
  nc=$fcst/${GRD[$i]}/bcon/BCON_${datep[$id]}_${DOM[$i]}
  f=( ${f[@]} $nc )
done
#final date of grid09 results
#  fnl=$(ls -rt $fcst/${GRD[$p]}/cctm.fcst/daily/CCTM_CG*|tail -n1|rev|cut -d'_' -f1|rev|cut -c1-8)

for ((id=0;id <= 9; id+=1));do

  # wait grid09 running results at DEVP
  cgrd=$fcst/${GRD[$p]}/cctm.fcst/daily/CCTM_CGRID_v532_intel_${DOM[$p]}_${datep[$id]}.nc
  while true;do
    cdate=$(~/bin/j2c $(ncdump -h $cgrd|grep CDATE|awk '{print $3}'))
    if [[ $cdate -eq ${datep[0]} ]];then break;fi
    sleep 64
  done

  # re-do the boundaries from grid09 results (regardless end-run or not)
  nc=/nas2/cmaqruns/2022fcst/${GRD[$i]}/bcon/BCON_today_${DOM[$i]}
  rm -f $nc #prevent re-run with same BCON file

  nc=$fcst/${GRD[$p]}/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$p]}_${datep[$id]}.nc
  rm -f ${f[$id]}
  csh $fcst/run_bcon_NC.csh $nc >&/dev/null
  cmd='/usr/bin/ncrcat -O '$(echo ${f[@]})' '$nc
  eval $cmd

  idp=$(( 10#$id - 1 ))
  if [[ $id -eq 0 ]];then
    yes=$yestd
  else
    yes=${datep[$idp]}
  fi
  cgrd=$fcst/${GRD[$i]}/cctm.fcst/daily/CCTM_CGRID_v532_intel_${DOM[$i]}_${yes}.nc
  icon=$fcst/${GRD[$i]}/icon/ICON_yesterday_${DOM[$i]}
  cp $cgrd $icon

  YYYYJJJ=$(date -d ${dates[$id]} +%Y%j)
  mcip_start=$BEGD
  mcip_end=$(date -d ${dates[$id]}+0days +%Y-%m-%d)
  cp project.config_loop project.config
  for cmd in 's/YYYYJJJ/'$YYYYJJJ'/g' \
           's/mcip_start/'$mcip_start'/g' \
           's/mcip_end/'$mcip_end'/g' \
           's/2400000/ 240000/g';do
    sed -ie $cmd project.config
  done

  cd $fcst
  csh ./run.cctm.${ii}.csh

done
