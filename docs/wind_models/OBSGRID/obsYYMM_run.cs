#usage: obsYYMM_run.cs 1304 5
path=/Users/WRF4.3/OBSGRID
ym=$1
if [ $ym -gt 9999 ] || [ $ym -lt 101 ];then echo 'input YYMM';exit;fi
y=`echo $ym|cut -c1-2`
n=`echo $ym|cut -c3-3`
if [ $n -eq 0 ];then m=`echo $ym|cut -c4-4`;else m=`echo $ym|cut -c3-4`;fi
p=$(( $m-1 ));test $p -lt 10 && p=0$p
ymd1=$y$p"15"
test $p == 00 && ymd1=$(( $y - 1 ))"1215"
yj0=`cal2jul $ymd1`
#rm -f met_em*
ln -sf $path/../WPS/20$ym/met/met_em* .

j=$2
#calculate the beg/end calendar dates
#yj2 may exceed 365, this will be handled in jul2cal
yj1=`echo "$yj0+4*($j-1)"|bc -l`
yj2=$(( $yj1+5 ))
ymd1=`jul2cal $yj1`
ymd2=`jul2cal $yj2`
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
mv -f metoa_em* $path/20$ym/run$j
mv -f OBS_DOMAIN* $path/20$ym/run$j
mv -f wrfsfdda* $path/20$ym/run$j

