head=OMI-Aura_L3-OMSO2e_
ndays=( 366 365 365 365 )
for y in {05..22};do n=$(nfile "${head}20${y}m*");if [[ $n != ${ndays[$(( 10#$y % 4 ))]} ]] && [[ $n != 0 ]];then echo $y $n;fi;done
y=22;for j in {01..12};do n=$(nfile "${head}20${y}m${j}*");test $n != $(days_of_month $y $j) && echo $y $j  $n;done
y=22;m=04;for k in {0..3};do echo $y $m $k $(nfile "${head}20${y}m${j}${k}*");done

## days_of_month
MM=$2
test $MM -eq 1 && MON="31"
test $MM -eq 3 && MON="31"
test $MM -eq 4 && MON="30"
test $MM -eq 5 && MON="31"
test $MM -eq 6 && MON="30"
test $MM -eq 7 && MON="31"
test $MM -eq 8 && MON="31"
test $MM -eq 9 && MON="30"
test $MM -eq 10 && MON="31"
test $MM -eq 11 && MON="30"
test $MM -eq 12 && MON="31"
if [ $MM -eq 2 ]; then
if [ $(( $1 % 4 )) -eq 0 ]; then
 MON="29"
else
 MON="28"
fi
fi
echo $MON

## nfile
f=$1
if compgen -G "${f}" > /dev/null;then
  n=$(ls $f|wc -l)
else
  n=0
fi
echo $n
