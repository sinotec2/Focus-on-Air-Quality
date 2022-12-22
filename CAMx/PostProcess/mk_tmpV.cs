kuang@DEVP /nas1/camxruns/2019/outputs/con10
$ cat mk_tmpV.cs
#before execution, make sure the NCO command can be executed

#basic definition
lis='CO              NO2             O3              SO2             NMHC            PM10            PM25            '
blk=( "              " "             " "              " "             " "            " "            " "            " )
new=()
for i in {0..6};do ii=$(( $i + 1 ));new=( ${new[@]} $(echo ${lis}|cut -d' ' -f$ii ));done

nc=$1

var=$(ncdump -h $nc|grep VAR-LIST|head -n1)

# make sure the number of species of incoming nc file is right
nvar1=$(ncdump -h $nc|grep NVARS|head -n1|awk '{print $3}')
var2=$(echo $var|sed 's/ /_/g')
var3=$(echo $var2|sed 's/_//g')
nvar2=$(( ${#var2} - ${#var3} - 3 ))
if [[ $nvar1 -ne $nvar2 ]];then echo $nvar1 -ne $nvar2;exit;fi

#check existence of species
a=()
for ((i=1;i<=$nvar1;i+=1));do ii=$(( $i + 2 ));vv=$(echo $var|cut -d' ' -f$ii);vv=${vv/\"};a=( ${a[@]} $vv);done
ipas=();lis_new='';nvar=7
for isp in {0..3};do
  ipas_isp=1
  for ((i=0;i<$nvar1;i+=1));do if [[ ${a[$i]} == ${new[$isp]} ]];then ipas_isp=0;fi;done
  ipas=( ${ipas[@]} $ipas_isp )
  if [[ ipas_isp -eq 0 ]];then
    lis_new=${lis_new}${new[$isp]}${blk[$isp]}
  else
    nvar=$(( $nvar - 1 ))
  fi
done
for isp in {4..6};do lis_new=${lis_new}${new[$isp]}${blk[$isp]};ipas=( ${ipas[@]} 0 );done

#store the first $nvar specises for ncrenaming
v=()
for ((i=1;i<=$nvar;i+=1));do ii=$(( $i + 2 )); vv=$(echo $var|cut -d' ' -f$ii);vv=${vv/\"};v=( ${v[@]} $vv);done

#streaming these specise for ncks command
vv='';nvm1=$(( $nvar - 1 ))
for ((i=0;i<$nvar;i+=1));do vv=$(echo ${vv},${v[i]});done
ncks -O -d TSTEP,0 -d VAR,0,$nvm1 -v TFLAG$vv $nc template.nc
ncatted -a VAR-LIST,global,o,c,"${lis_new}" template.nc
ncatted -a NVARS,global,o,i,$nvar template.nc

#rename the first $nvar specises
new2=();intr=();ii=1
for ((i=0;i<7;i+=1));do test ${ipas[$i]} -eq 1 && continue;new2=( ${new2[@]} $(echo ${lis_new}|cut -d' ' -f$ii ));ii=$(( $ii + 1 ));done
for ((i=0;i<$nvar;i+=1));do for ((j=0;j<$nvar;j+=1));do if [[ ${v[$j]} == ${new2[$i]} ]];then intr=( ${intr[@]} ${v[$j]} );continue;fi;done;done

nv=$(echo ${#v[@]})
ni=$(echo ${#intr[@]})
for ((i=0;i < $nv; i+=1));do
  n=${new2[$i]}
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
