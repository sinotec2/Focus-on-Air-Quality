  #$ cat /nas2/cmaqruns/2022fcst/aconc2gifP.cs
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
datej=();for i in $(seq $bj $ej);do datej=( ${datej[@]} $i );done
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
pwd=$PWD
cd $root
#if compgen -G "${s}_*.png" > /dev/null; then rm ${s}_*.png;fi;
fnames=()
for jd in $(seq 1 $nd);do
  jd1=$(( $jd - 1))
  fname=${root}/PMs${dates[$jd1]}.nc
  jbh=0; test $bd == ${dates[$jd1]} && jbh=$bh
  jeh=23; test $ed == ${dates[$jd1]} && jeh=$eh
  for jh in $(seq $jbh $jeh);do
    jhh=$( printf "%02d" ${jh} )
    fnameo=${root}/${s}${dates[$jd1]}_$jhh
    $NCKS -O -v TFLAG,$s -d TSTEP,$jh $fname $fnameo
    if ! [ -e $fnameo ];then echo $fname fnameo; exit;fi
    STIME=${jh}0000.;if [[ $jh -eq 0 ]];then STIME=0;fi
    $NCATTED -a STIME,global,o,f,${STIME} $fnameo
    $NCATTED -a SDATE,global,o,f,${datej[$jd1]} $fnameo
    fnames=( ${fnames[@]} $fnameo )
  done
done

a='$NCRCAT -O '$(echo ${fnames[@]})' $s.nc'
eval $a
mnmx=$(~/bin/mxnNC /nas2/cmaqruns/2022fcst/grid03/cctm.fcst/daily/${s}.nc )


pngs=()
iii=0
for jd in $(seq 1 $nd);do
  jd1=$(( $jd - 1))
  jbh=0; test $bd == ${dates[$jd1]} && jbh=$bh
  jeh=23; test $ed == ${dates[$jd1]} && jeh=$eh
  for jh in $(seq $jbh $jeh);do
    jhh=$( printf "%02d" ${jh} );fnameo=${fnames[$iii]}
    i=$( printf "%03d" ${iii} );png=${s}_$i.png;
    pngs=( ${pngs[@]} $png )
    if [[ -e $png ]];then rm -f $png;fi
    ~/bin/sub ~/bin/m3nc2gifP.py $fnameo ${dates[$jd1]}${jhh} $iii $mnmx
    sleep 1
    iii=$(( $iii + 1 ))
  done
done
#if [[ $d == 1 || $d == 2 ]];then ~/bin/join_nc.py $s.nc;fi
while true;do
  n=$(ps -ef|grep m3nc2gifP.py|grep ${GRD[$d]} |wc -l)
  if [[ $n -eq 0 ]] && [[ -e ${pngs[0]} ]] && [[ -e ${pngs[$len]} ]];then
    break
  else
    sleep 1
  fi
done

#for i in $( seq 0 $len);do if [[ -e ${fnames[$i]} ]];then rm -f ${fnames[$i]};fi;done
#rm -f $root/${s}.nc
size=$( /usr/bin/convert ${s}_000.png -format "%wx%h" info: )
a='/usr/bin/convert -dispose 2 -coalesce +repage -background none '$(echo ${pngs[@]})' -size $size ${s}_${b}.gif'
eval $a

cd $pwd
echo $root/${s}_${b}.gif has been generated
