#kuang@master /nas1/backup/data/NOAA/NCEP/GFS/YYYY
#$ cat fcst.cs
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
sub=~/bin/sub
DOM=( 'CWBWRF_45k' 'SECN_9k' 'TWEPA_3k' 'tw_CWBWRF_45k' 'nests3')
RES=( 45 09 03 )
GRD=( 'grid45'     'grid09'  'grid03' )
MPI=( '-f machinefile -np 200' '-f machinefile -np 196' '-f machinefile -np 140' '-f machinefile -np 120' '-f machinefile -np 120')
CMB=/nas1/cmaqruns/CMAQ_Project/POST/combine/scripts/BLD_combine_v53_gcc/combine_v53.exe
cd $gfs


# 執行gfs檔案下載
# execute ungrib and metgrid in background
for ((i=0;i <= 312; i+=3));do
  iii=$(printf "%03d" $i)
  file=gfs.t${BH}z.pgrb2.1p00.f$iii
  if [ -e $file ];then rm $file;fi
  while [ 1 ]; do
  $wget --no-check-certificate -q --retry-connrefused --waitretry=3 --random-wait \
        --read-timeout=20 --timeout=15 -t 10 --continue $root$dir$file
  if [ $? = 0 ]; then break; fi
  sleep 5
  done

  NOWD=$(date -d "$BEGD +$(( $i + 10#$BH ))hour" +%Y-%m-%d )
  hh=$(date -d "$BEGD +$(( $i + 10#$BH ))hour" +%H )
  mkdir -p ${gfs}/f$iii
  cd ${gfs}/f$iii
  ./link_grib.csh gfs*
  cp ../namelist.wps_loop namelist.wps
  for cmd in 's/BEGD/'$NOWD'/g' 's/ENDD/'$NOWD'/g' 's/HH/'$hh'/g';do sed -ie $cmd namelist.wps;done
  ~/bin/sub ../UGB2
  cd $gfs
done

#background executions of mk_emis and mk_ptse
for i in 0 1;do
  ii=$(echo ${GRD[$i]}|cut -c5-)
  cd $fcst/grid$ii/smoke
  ~/bin/sub ../../mk_emis.py $BEGD
done
~/bin/sub $gfs/em3.cs

~/bin/wait_exe metgrid #make sure all metgrid executions are finished

# real及wrf
## 起迄年 、 月 、 日B
yea1=$(echo $BEGD|cut -d'-' -f1);mon1=$(echo $BEGD|cut -d'-' -f2);day1=$(echo $BEGD|cut -d'-' -f3)
yea2=$(echo $ENDD|cut -d'-' -f1);mon2=$(echo $ENDD|cut -d'-' -f2);day2=$(echo $ENDD|cut -d'-' -f3)
dates=()
for id in {0..11};do
  dates=( ${dates[@]} $(date -d "$BEGD +${id}days" +%Y-%m-%d) )
done
for i in 3 2;do
  cd $gfs/${DOM[$i]}
  ## 置換模版中的起迄日期
  cp namelist.input_loop namelist.input
  for cmd in "s/SYEA/$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" \
             "s/EYEA/$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g" ;do
    sed -i $cmd namelist.input
  done
  if [[ $i == 3 ]];then
    rm metoa_em*
    ## 連結metoa_em檔案
    for d in 1 2;do for id in {0..11};do for j in $(ls ../met_em.d0${d}.${dates[$id]}_*);do k=${j};l=${k/..\//};m=${l/met_/metoa_};ln -s $j $m;done;done;done
    # real
    LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin:/opt/mpich/mpich-3.4.2-icc/lib /opt/mpich/mpich-3.4.2-icc/bin/mpirun ${MPI[$i]} /nas1/WRF4.0/WRFv4.3/WRFV4/main/real.exe >& /dev/null
  else
    $gfs/ndown.cs
  fi
  # wrf
  LD_LIBRARY_PATH=/opt/netcdf/netcdf4_gcc/lib /opt/mpich/mpich3_gcc/bin/mpirun ${MPI[$i]} /opt/WRF4/WRFv4.2/main/wrf.exe >& /dev/null
  # link the wrfout's and execute mcip(in the background)
  if [ $i == 3 ];then
    for d in 1 2;do
      j=$(( $d - 1))
      for f in {0..10};do
        wrfo=wrfout_d0${d}_${dates[$f]}_00:00:00
        nc1=$gfs/${DOM[$i]}/$wrfo
        if [ -e $nc1 ];then
          wrfo2=${wrfo/d0${d}/d01}
          nc2=$gfs/${DOM[$j]}/$wrfo2
          if [ -e $nc2 ];then rm $nc2;fi
          ln -sf $nc1 $nc2
        fi
      done
  #   mcip
      cd $cmaq/data/wrfout
      for f in {0..10};do nc=$gfs/${DOM[$j]}/wrfout_d01_${dates[$f]}_00:00:00;ln -sf $nc wrfout_d0${d}_$f;done
      cd $fcst;~/bin/sub csh run_mcip_DM.csh ${GRD[$j]} 10 >&/dev/null
    done
  else
  #   mcip i=2,d=3
      cd $cmaq/data/wrfout;j=$i;d=3
      for f in {0..10};do nc=$gfs/${DOM[$j]}/wrfout_d01_${dates[$f]}_00:00:00;ln -sf $nc wrfout_d0${d}_$f;done
      cd $fcst;~/bin/sub csh run_mcip_DM.csh ${GRD[$j]} 10 >&/dev/null
  fi
done

#CMAQ stream
cd $fcst
YYYYJJJ=$(date -d ${BEGD} +%Y%j)
mcip_start=$BEGD
mcip_end=$(date -d ${BEGD}+9days +%Y-%m-%d)
cp project.config_loop project.config
for cmd in 's/YYYYJJJ/'$YYYYJJJ'/g' \
           's/mcip_start/'$mcip_start'/g' \
           's/mcip_end/'$mcip_end'/g';do
  sed -ie $cmd project.config
done

datep=()
for id in {0..9};do
  datep=( ${datep[@]} $(date -d "$BEGD +${id}days" +%Y%m%d) )
done
for i in 0 1 2;do
  ii=$(echo ${GRD[$i]}|cut -c5-)
  cd $fcst
  csh ./run.cctm.${ii}.csh

  # combine PM's
  for id in {0..9};do
    nc=$fcst/${GRD[$i]}/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$i]}_${datep[$id]}.nc
    if [[ -e $nc ]];then ~/bin/sub $fcst/combine.sh $nc;fi
  done
  if [[ $i < 2 ]];then
  # nest down BCON and ICON
    j=$(( $i + 1))
    # define the resultant BCON files
    f=()
    for id in {0..9};do
      nc=$fcst/${GRD[$j]}/bcon/BCON_${datep[$id]}_${DOM[$j]}
      f=( ${f[@]} $nc )
      if [[ -e $nc ]];then rm $nc;fi
    done

    # generate bcon for next nest
    for id in {0..9};do
      nc=$fcst/${GRD[$i]}/cctm.fcst/daily/CCTM_ACONC_v532_intel_${DOM[$i]}_${datep[$id]}.nc
      csh $fcst/run_bcon_NC.csh $nc >&/dev/null
    done

    nc=$fcst/${GRD[$j]}/bcon/BCON_today_${DOM[$j]}
    /usr/bin/ncrcat -O ${f[0]} ${f[1]} ${f[2]} ${f[3]} ${f[4]} ${f[5]} ${f[6]} ${f[7]} ${f[8]} ${f[9]} $nc
    # expand the last hour to next day
    ~/bin/add_lastHr.py $nc
    cd $fcst

    target=$fcst/grid$ii/icon/ICON_yesterday_${DOM[$j]}
    if [ -e $target ];then rm $target;fi
    csh $fcst/run_icon_NC.csh $fcst/grid$ii/icon/ICON_yesterday_${DOM[$i]} >&/dev/null
  fi
  # prepare earth json files and backup to imackuang

  ~/bin/wait_exe combine #make sure all combine executions are finished

  r=${RES[$i]}
  cd /nas1/Data/javascripts/D3js/earthFcst$r/public/data/weather/current
  for id in {0..9};do ~/bin/sub ./cmaq_jsonByDay.py ${dates[$id]};done
done
