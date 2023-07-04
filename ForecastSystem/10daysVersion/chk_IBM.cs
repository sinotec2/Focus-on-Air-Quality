if [[ ${#} -eq 0 ]];then
 echo 'input domain #';exit 0;fi

if [[ $BEGD == "" ]];then
  today=$(date -d -0day +%Y%m%d)
  export BEGD=$(date -d "$today -0days" +%Y-%m-%d)
  HR=10#$(date +%H)
  if [[ $HR -ge 7 && $HR -lt 16 ]];then export BEGD=$(date -d "$today -1days" +%Y-%m-%d);fi
fi

BEGJ=$(date -d $BEGD +%Y%j)
dates=();datep=()
for id in {0..11};do
  dates=( ${dates[@]} $(date -d "$BEGD +${id}days" +%Y-%m-%d) )
  datep=( ${datep[@]} $(date -d "$BEGD +${id}days" +%Y%m%d) )
done


fcst=/u01/cmaqruns/2022fcst
DOM=( 'CWBWRF_45k' 'SECN_9k' 'TWEPA_3k' 'tw_CWBWRF_45k' 'nests3')
RES=( 45 09 03 )
GRD=( 'grid45'     'grid09'  'grid03' )

i=$1

  nc=$fcst/${GRD[$i]}/mcip/SOI_CRO.nc
  echo 'MCIP ck'
  while true;do
    if [[ -e $nc ]];then
      n1=$(~/bin/pr_tflag.py $nc|grep ${dates[0]}|wc -l)
      n2=$(~/bin/pr_tflag.py $nc|grep ${dates[10]}|wc -l)
      jj=$(/usr/bin/ncdump -h $nc|grep SDATE|cut -d' ' -f3)
      if [[ $n1 -eq 24  &&  $n2 -ge 1 && $jj -eq $BEGJ ]];then
        break
      fi
    fi
    sleep 59
  done
  echo 'MCIP ok'

  nc=$fcst/${GRD[$i]}/icon/ICON_yesterday_${DOM[$i]}
  lg=/u01/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022/get_all.log
  echo 'ICON ck'
  first=1
  while true;do
    test $first -ne 1 && sleep 58
    first=0
    if [[ -e $nc && -e $lg ]];then
      d=$(ls -lh --time-style=long-iso $nc|~/bin/awkk 6)
      echo $d ${BEGD}
#      test $d != ${BEGD} && continue
      n=$(grep aermr20 $lg|wc -l)
      echo $n
      test $n -ne 2 && continue
      jj=$(/usr/bin/ncdump -h $nc|grep SDATE|cut -d' ' -f3)
      echo $jj $BEGJ
      if [[ $jj -eq $BEGJ ]];then
        break
      fi
    fi
  done
  echo 'ICON ok'

  nc=$fcst/${GRD[$i]}/bcon/BCON_yesterday_${DOM[$i]}
  nt=24
  test $i -eq 0 && nt=4
  echo 'BCON ck'
  while true;do
    if [[ -e $nc ]];then
      n1=$(~/bin/pr_tflag.py $nc|grep ${dates[0]}|wc -l)
      n2=$(~/bin/pr_tflag.py $nc|grep ${dates[10]}|wc -l)
      jj=$(/usr/bin/ncdump -h $nc|grep SDATE|cut -d' ' -f3)
      echo $n1 $n2 $jj $BEGJ
      if [[ $n1 -eq $nt  &&  $n2 -ge 1 && $jj -le $BEGJ ]];then
        break
      fi
    fi
    sleep 57
  done
  echo 'BCON ok'
