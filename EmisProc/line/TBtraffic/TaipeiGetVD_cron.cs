cd /home/backup/data/ETC/TaipeiVD
if [ -f latest ];then rm latest;fi
if [ -f GetVDDATA* ];then rm GetVDDATA*;fi
A=`date +%M`
M=$(( $A % 5 ))
if [ $M = 0 ] ;then
ymd=`date  --rfc-3339='date'`
Y=`date +%Y`
mkdir -p $Y

wget https://tcgbusfs.blob.core.windows.net/blobtisv/GetVDDATA.xml.gz
gzip -d GetVDDATA.xml.gz 
mv GetVDDATA.xml GetVDDATA

/cluster/miniconda/bin/python getVD.py
cat latest>>$Y/$ymd
rm latest
rm GetVDDATA*
date>>nohup.out
fi
