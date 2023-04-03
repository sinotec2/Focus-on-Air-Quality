GIT=/usr/bin/git
gtd=~/GitHub/sinotec2.github.io
TOKEN=$(cat ~/bin/git.token)
WGET=/opt/local/bin/wget
CVRT=/usr/local/bin/convert

bh=2
test $(date +%H) -gt 21 && bh=14
eh=$(( $bh + 72))
today=$(date +%Y%m%d)
today=$(echo ${today}00)
BEGD=$(date  -v+0d -j -f "%Y%m%d%H"  "${today}" +%Y-%m-%d)
BEGH=$(date  -v+${bh}H -j -f "%Y%m%d%H"  "${today}" +%Y%m%d%H)
YM=$(date -j -f "%Y-%m-%d" "$BEGD" +%Y%m)

cd $gtd
$GIT pull

for r in 03 09;do
D=03
test $r -eq '09' && D=02

cd /Users/cmaqruns/2022fcst/grid$r/cctm.fcst/daily/jfy
rm -f *.png
for ((i=$bh;i<$eh; i+=1));do
  ymdh=$(date  -v+${i}H -j -f "%Y-%m-%d"  "${BEGD}" +%Y%m%d%H)
  $WGET -q https://watch.ncdr.nat.gov.tw/00_Wxmap/8F4_CMAQ/${YM}/${BEGH}/ncdr-PM25_d${D}_$ymdh.png
done
$CVRT -delay 30 -dispose 2 -coalesce +repage -background none *.png jfy${BEGH}.gif
cp jfy${BEGH}.gif $gtd/cmaq_forecast/grid$r/jfy.gif

cd $gtd
$GIT add cmaq_forecast/grid$r/jfy.gif
$GIT commit -m "update jfy${BEGH}.gif for grid$r"
~/bin/sh $GIT push https://sinotec2:$TOKEN@github.com/sinotec2/sinotec2.github.io.git >> ~/bat.log
done