#kuang@eng06 /nas1/TEDS/teds11/to_karen
$ cat grep_ncks.py
import netCDF4
import os, sys, subprocess

pth='area biog line ptse ship'.split()
ext={i:[i] for i in pth}
ext.update({'ship':['51Ab'],'ptse':['ptsG','ptsE']})
home='/nas1/TEDS/teds11'
addOn={i:5002 for i in 'AB'}
addOn.update({i:5001 for i in 'CD'})
begd=["02-12","02-25","03-11","03-25"]
endd=["02-16","02-28","03-14","03-28"]
mmss=['02','02','03','03']
abcd=[i for i in 'ABCD']
begT={i:j for i,j in zip(abcd,begd)}
endT={i:j for i,j in zip(abcd,endd)}
mmsT={i:j for i,j in zip(abcd,mmss)}
for ipth in [0,1,2,4]: #range(3,4):
  for p in pth[ipth:ipth+1]:
    for c in 'B':
      mm=mmsT[c]
      for e in ext[p]:
        fname=home+'/'+p+'/'+'fortBE.413_teds11.'+e+mm+'.nc'
        fnameO=p+c+'.nc'
        if p=='ptse':fnameO=e+c+'.nc'
        os.system('/home/anaconda3/bin/python ~/bin/pr_tflag.py '+fname+' > pr.txt')
        cmd="grep -n '2019-"+begT[c]+" 00:00:00' pr.txt|cut -d':' -f1"
        i=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n')
        i=str(int(i)-1)+','
        cmd="grep -n '2019-"+endT[c]+" 00:00:00' pr.txt|cut -d':' -f1"
        j=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n')
        os.system('/usr/bin/ncks -O -d TSTEP,'+i+j+' '+fname+' '+fnameO)
        nc = netCDF4.Dataset(fnameO, 'r+')
        nc.SDATE+=addOn[c]
        nc['TFLAG'][:,:,0]+=addOn[c]
