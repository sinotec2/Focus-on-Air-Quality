#$ cat ~/GitHubRepos/cp_timebar.cs
GIT=/usr/bin/git
GH=/usr/bin/gh
gtd=~/GitHubRepos
TOKEN=$(cat ~/bin/git.token)
export GH_TOKEN=$TOKEN
today=$(date +%Y%m%d)
rundate=$(date -d "$today +0day" +%Y%m%d)
BEGD=$(date -d "$today -1day" +%Y-%m-%d)
dates=();datep=()
for id in {0..11};do
  dates=( ${dates[@]} $(date -d "$BEGD +${id}days" +%Y-%m-%d) )
  datep=( ${datep[@]} $(date -d "$BEGD +${id}days" +%Y%m%d) )
done


GRD=( 'grid45'     'grid09'  'grid03' )


repo=cmaq_$rundate
mkdir -p ${gtd}/${repo}
cd ${gtd}/${repo}
cp /nas3/cmaqruns/2022fcst/grid45/cctm.fcst/daily/png1_${BEGD}.tar.gz .
cp /nas2/cmaqruns/2022fcst/grid09/cctm.fcst/daily/png2_${BEGD}.tar.gz .
cp /nas3/cmaqruns/2022fcst/grid03/cctm.fcst/daily/png3_${BEGD}.tar.gz .
for id in {0..11};do
cp /nas2/backup/data/NOAA/NCEP/GFS/YYYY/TWEPA_3k/U10V10_d03_${dates[$id]}_00:00:00 .
cp /nas2/backup/data/NOAA/NCEP/GFS/YYYY/tw_CWBWRF_45k/U10V10_d0?_${dates[$id]}_00:00:00 .
done


cmd="/home/anaconda3/bin/curl -u sinotec2:$TOKEN https://api.github.com/user/repos -d '{\"name\":\"${repo}\"}'"
eval $cmd

$GIT init
$GIT add .
cmd="$GIT commit -m 'create $repo'"
eval $cmd
$GIT push -f https://sinotec2:$TOKEN@github.com/sinotec2/${repo}.git master


last4d=$(date -d "$today -4day" +%Y%m%d)
repo=cmaq_$last4d
$GH repo delete https://github.com/sinotec2/${repo}.git --yes
rm -fr ${gtd}/${repo}