if [ $HOSTNAME == '114-32-164-198.HINET-IP.hinet.net' ];then NCO='/opt/anaconda3/bin'
  elif [ $HOSTNAME == 'master' ];then NCO='/cluster/netcdf/bin'
  elif [ $HOSTNAME == 'centos8' ];then NCO='/opt/anaconda3/envs/py37/bin'
  elif [ $HOSTNAME == 'node03' ];then NCO='/opt/miniconda3/bin'
  else NCO='/usr/bin'
fi
NCKS=${NCO}/ncks
NCATTED=${NCO}/ncatted
fn=$1
yrmn=$(echo $fn|cut -d'.' -f2)
mkdir -p $yrmn
last=$(date -d "20${yrmn}01 -1days" +%Y%m%d)
y=$(date -d $last +%Y)
m=$(date -d $last +%m)
begd=$(date -d "${y}-${m}-15 +16days" +%Y%m%d)
begj=$(date -d "${begd}" +%Y%j)
SDATE=$(ncdump -h $fn|grep SDATE|awkk 3)
if [ $begj != $SDATE ]; then 
  echo $begj $SDATE 'not ok in SDATE'; 
  jj=$(( $SDATE - 2016001 ))
  begd=$(date -d "2016-01-01 +${jj}days" +%Y%m%d)
fi
nt=$(ncdump -h $fn|head -n3|tail -n1|cut -d'(' -f2|awkk 1)
nd=$(echo $nt/24|bc)
for ((d=1;d<=$nd;d+=1));do
  dd=$(( $d - 1 ))
  yrj=$(date -d "${begd} +${dd}days" +%Y%j)
  ymd=$(date -d "${begd} +${dd}days" +%Y%m%d)
  t1=$(( $dd * 24 )) 
  t2=$(( $d  * 24 )) 
  newfn=${fn/$yrmn/$ymd}
  $NCKS -O -d TSTEP,$t1,$t2 $fn $yrmn/$newfn
  $NCATTED -O  -a SDATE,global,o,i,$yrj $yrmn/$newfn
  echo $yrmn/$newfn 
done