$ cat /nas2/cmaqruns/2022fcst/aconc2gif.cs
NCKS=/usr/bin/ncks
NCRCAT=/usr/bin/ncrcat
NCATTED=/usr/bin/ncatted
fcst=/nas2/cmaqruns/2022fcst
echo 'please input begin/end YYYYMMDDHH(UTC), species_name, and domain1/2/3'
echo 'species_name must be: PM10/PM1_TOT/PM25_TOT/PMC_TOT/VOC/SO2/NO2... in upper case'
b=$1 #begin YYYYMMDDHH
e=$2 #end YYYYMMDDHH
s=$3 #species name
d=$4 #domain 1~3
if [[ $d == "d"* ]];then d=$(echo $d|rev|cut -c1);fi
PM_s=( "PM10" "PM1_TOT" "PM25_TOT" "PMC_TOT" "VOC" )
GRD=( 'grid45'  'grid09'  'grid03' )
DOM=( 'CWBWRF_45k' 'SECN_9k' 'TWEPA_3k')

echo $b $e $s $d
if [[ $b -gt $e ]];then echo $b > $e;fi
test $b -gt $e && exit 0

bd=$(echo $b|cut -c 1-8)
bj=$(date -d "$bd" +%Y%j)
bh=$(echo $b|cut -c 9-10)
bh=$(( 10#$bh ))

ed=$(echo $e|cut -c 1-8)
ej=$(date -d "$ed" +%Y%j)
eh=$(echo $e|cut -c 9-10)
eh=$(( 10#$eh ))

dates=();for i in $(seq $bj $ej);do dates=( ${dates[@]} $(~/bin/j2c $i) );done
nd=${#dates[@]}

len=$(( ( $ej - $bj ) * 24 + $eh - $bh ))

js=-1
for i in {0..4};do
  if [ $s == ${PM_s[$i]} ];then
    js=$i
  fi
done
d=$(( $d - 1 ))
if [ $js -ge 0 ];then
  FN=PMs
else
  FN=CCTM_ACONC_v532_intel_${DOM[$d]}_
fi

root=${fcst}/${GRD[$d]}/cctm.fcst/daily
fnames=()
for jd in $(seq 1 $nd);do
  jd1=$(( $jd - 1))
  fname=${root}/PMs${dates[$jd1]}.nc
  jbh=0; test $bd == ${dates[$jd1]} && jbh=$bh
  jeh=23; test $ed == ${dates[$jd1]} && jeh=$eh
  for jh in $(seq $jbh $jeh);do
    fnameo=${root}/${s}${dates[$jd1]}_$jh
    $NCKS -O -v TFLAG,$s -d TSTEP,$jh $fname $fnameo
    fnames=( ${fnames[@]} $fnameo )
  done
done
pwd=$PWD
cd $root
a='$NCRCAT -O '$(echo ${fnames[@]})' $s.nc'
eval $a
test $bh -gt 0 && $NCATTED -a STIME,global,o,f,${bh}0000. $s.nc
if compgen -G "${s}_*.png" > /dev/null; then rm ${s}_*.png;fi;for i in $( seq 0 $len);do if [[ -e ${fnames[$i]} ]];then rm ${fnames[$i]};fi;done
#if [[ $d == 1 || $d == 2 ]];then ~/bin/join_nc.py $s.nc;fi
~/bin/m3nc2gif.py $s.nc
mv $s.gif ${s}_${b}.gif
cd $pwd
echo $root/${s}_${b}.gif has been generated
