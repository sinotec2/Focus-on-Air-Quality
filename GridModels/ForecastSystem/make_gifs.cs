sinotec2@lgn301 /work/sinotec2/WRF4/WRF4.2.1
$ cat make_gifs.cs 
fcst=/work/sinotec2/cmaqruns/forecast
DOM=( 'CWBWRF_45k' 'SECN_9k' 'TWEPA_3k' 'tw_CWBWRF_45k' 'nests3')
RES=( 45 09 03 )
GRD=( 'grid45'     'grid09'  'grid03' )
ITs=( 3 2 1 )
bin=/work/sinotec2/opt/cmaq_recommend/bin
pyt=~/.conda/envs/ncl_stable/bin/python

i=$1
it=${ITs[$i]}
dt=$(( 10#$it * 10000 ))
  cd $fcst/${GRD[$i]}/cctm.fcst/daily
  for fn in $(ls PMs20*|tail -n10);do
    nt=$(( $($bin/pr_tflag.py $fn|wc -l) - 1 ))
    j=$(echo $fn|cut -c4-11)
    for s in PM25_TOT PM10;do
      p=$s;test $p == "PM25_TOT" && p="PM2.5"
      $bin/ncks -O -d VAR,0 -d TSTEP,0,${nt},$it -v TFLAG,$s $fn ${p}_$j.nc
      $bin/ncatted -a TSTEP,global,o,i,$dt ${p}_$j.nc;done;done
  for s in SO2 CO O3 NO2;do for fn in $(ls CCTM_ACONC*|tail -n10);do
    j=$(echo $fn|cut -d'_' -f7)
    $bin/ncks -O -d LAY,0 -d VAR,0 -d TSTEP,0,${nt},$it -v TFLAG,$s $fn ${s}_$j
    $bin/ncatted -a TSTEP,global,o,i,$dt ${s}_$j;done;done
  for s in PM2.5 PM10 SO2 CO O3 NO2;do
    $bin/ncrcat -O ${s}_2*.nc ${s}.nc;rm ${s}_2*.nc;done
  for s in PM2.5 PM10 SO2 CO O3 NO2;do
    $bin/sub $pyt $bin/m3nc2gif.py $s.nc;done
  $bin/wait_exe m3nc2gif.py  #make sure all executions are finished

y=$(date -d -0day +%Y)
m=$(date -d -0day +%m)
d=$(date -d -0day +%d)

cd $fcst/${GRD[$i]}/cctm.fcst/daily
for s in PM25_TOT PM10 SO2 CO O3 NO2;do
  cp $s.gif pngs/$y/$m/$d;done

DEV=~/GitHubRepos/sinotec2.github.io/cmaq_forecast/${GRD[$i]}
s=PM25_TOT
/usr/bin/tar cvfz png.tar.gz ${s}_[012]*.png
cp $fcst/${GRD[$i]}/cctm.fcst/daily/$s.gif $DEV
cp $fcst/${GRD[$i]}/cctm.fcst/daily/png.tar.gz $DEV
if [[ $i -eq 2 ]];then
  cd $DEV
  f=D2_PM25.gif
  if [[ -e $f ]];then rm -f $f;fi
  /usr/bin/wget -q https://rcec.sinica.edu.tw/aqrc_webimg/$f
fi
cp $fcst/${GRD[$i]}/cctm.fcst/daily/$s.gif $DEV
cp $fcst/${GRD[$i]}/cctm.fcst/daily/png.tar.gz $DEV
if [[ $i -eq 2 ]];then
  cd $DEV
  f=D2_PM25.gif
  if [[ -e $f ]];then rm -f $f;fi
  /usr/bin/wget -q https://rcec.sinica.edu.tw/aqrc_webimg/$f
fi
daily=$fcst/${GRD[$i]}/cctm.fcst/daily
mac=~/GitHub/sinotec2.github.io/cmaq_forecast/{GRD[$i]}
/usr/bin/sshpass -f ~/bin/PW scp -r $daily/$s.gif kuang@imackuang:$mac
/usr/bin/sshpass -f ~/bin/PW scp -r $daily/png.tar.gz kuang@imackuang:$mac
n=$(~/bin/psg sleep|grep 3600|wc -l)
test $n -gt 0 && exit
while true;do
  H=10#$(date +%H)
  if [[ $H -ge 8 && $H -le 17 ]];then break;fi
  sleep 3600
done

cd $gtd
$GIT pull
$GIT add cmaq_forecast/${GRD[$i]}/*.g*
$GIT commit -m "revised PMF.gif $rundate"
$GIT push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git master >> ~/bat.log

exit 0
#if [[ $HOSTNAME == "dev2" ]];then
#MAC=/Users/Data/javascripts/NASA_GMAO_classic_geos_cf/classic_geos_cf/express-locallibrary-tutorial/public/latest/latest
#reg=( "eastern_asia" "se_china" "taiwan" )
#  p=$s;test $p == "PM25_TOT" && p="PM2.5"
