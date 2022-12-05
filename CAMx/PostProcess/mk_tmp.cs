#kuang@master /nas1/camxruns/2019/outputs/con10
#$ cat mk_tmp.cs

nc=$1

#make sure the NCO command can be executed
var=$(ncdump -h $nc|grep VAR-LIST)

#store the first 7 specises
v=()
for i in {3..9};do vv=$(echo $var|awkk $i);vv=${vv/\"};v=( ${v[@]} $vv);done

#string these specise for ncks command
vv=''
for i in {0..6};do vv=$(echo ${vv},${v[i]});done
lis='CO              NO2             O3              SO2             NMHC            PM10            PM25            '
ncks -O -d TSTEP,0 -v VAR,0,6 -v TFLAG$vv $nc template.nc
ncatted -a VAR-LIST,global,o,c,"${lis}" template.nc
ncatted -a NVARS,global,o,i,7 template.nc

#rename the first 7 specises
new=();intr=()
for i in {0..6};do new=( ${new[@]} $(echo ${lis}|awkk $i ));done
for i in {0..6};do for j in {0..6};do if [[ ${v[$j]} == ${new[$i]} ]];then intr=( ${intr[@]} ${v[$j]} );continue;fi;done;done

nv=$(echo ${#v[@]})
ni=$(echo ${#intr[@]})
for ((i=0;i < $nv; i+=1));do
  n=${new[$i]}
  iskip=0;for ((j=0;j < $ni; j+=1));do c=${intr[$j]}; test $c == $n && iskip=1;done; if [[ $iskip == 1 ]];then continue;fi
  for ((k=0;k < $nv; k+=1));do
    o=${v[$k]}
    iskip=0;for ((j=0;j < $ni; j+=1));do c=${intr[$j]}; test $c == $o && iskip=1;done; if [[ $iskip == 1 ]];then continue;fi
    break
  done
  ncrename -O -v ${o},${n} template.nc
  ncatted -a long_name,${n},o,c,"${n}" template.nc
  ni=$(( $ni + 1 ))
  intr=( ${intr[@]} $o )
done
