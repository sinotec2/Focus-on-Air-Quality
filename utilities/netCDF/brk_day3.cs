#kuang@node03 /nas2/cmaqruns/2022fcst/grid45/bcon
#$ cat ~/bin/brk_day3.cs
#!/bin/bash
HOSTs=( '125-229-149-182.hinet-ip.hinet.net' 'master' 'centos8' 'node03' )
NCOs=( '/opt/anaconda3/bin' '/cluster/netcdf/bin' '/opt/anaconda3/envs/py37/bin' '/opt/miniconda3/bin' )
NCO='/usr/bin'
for i in {0..3};do test $HOSTNAME == ${HOSTs[$i]} && NCO=${NCOs[$i]};done
NCKS=${NCO}/ncks
NCATTED=${NCO}/ncatted
NCRCAT=${NCO}/ncrcat

fn=$1

f=();for i in $(python ~/bin/pr_tflag.py $fn);do j=${i/[/};k=${j/]/};f=( ${f[@]} $k); done
nt=$(echo ${#f[@]})
yjs=();ymd=();hrs=();yms=()
for ((h=0;h < $nt; h+=2));do
  yj=$(echo ${f[$h]})
  ymdi=$(~/bin/j2c $yj)
  yrmn=$(echo ${ymdi}|cut -c 3-6)
  hh=$(echo ${f[$(( $h + 1 ))]});hh=$(( 10#$hh / 10000 ));hh=$(printf "%02d" ${hh})
  yjs=( ${yjs[@]} $yj )
  ymd=( ${ymd[@]} $ymdi )
  hrs=( ${hrs[@]} $hh )
  yms=( ${yms[@]} $yrmn )
  mkdir -p $yrmn
done
nt=$(echo ${#ymd[@]});nt1=$(( $nt - 1 ))
ymdold=${ymd[0]};yrmn=${yms[0]}
for ((h=0;h < $nt; h+=1));do
  newfn=${fn}_${ymd[$h]}${hrs[$h]}
  $NCKS -O -d TSTEP,$h $fn ${yms[$h]}/$newfn
  $NCATTED -O  -a SDATE,global,o,i,${yjs[$h]} ${yms[$h]}/$newfn
  if [[ ${ymd[$h]} != $ymdold ]] || [[ $h == $nt1 ]];then
    if [[ $h == $nt1 ]];then ymdold=${ymd[$h]};yrmn=${yms[$h]};fi
    $NCRCAT -O $yrmn/${fn}_${ymdold}?? $yrmn/${fn}_$ymdold
    rm -f $yrmn/${fn}_${ymdold}??
    ymdold=${ymd[$h]};yrmn=${yms[$h]}
  fi
done