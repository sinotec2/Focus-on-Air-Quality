#!/cluster/miniconda/envs/gribby/bin/python
import sys, pygrib, os, datetime
# in the form of M-A0064-018.grb2
fnames=[sys.argv[i] for i in [1,2]]
grbs=[pygrib.open(fname) for fname in fnames]
fcst_hrA=[i.split('-')[2].split('.')[0] for i in fnames]
fcst_hrs=[int(i) for i in fcst_hrA]
fcst_hr=(sum(fcst_hrs))//2
s='{:03d}'.format(fcst_hr)
grbout = open(fnames[0].replace(fcst_hrA[0],s),'wb')

for i in range(1,grbs[0].messages+1):
  grb=grbs[0].message(i)
  s=(grb.validDate+datetime.timedelta(hours=6)).strftime("%Y%m%d")
  grb['dataDate']=int(s)
  grb['forecastTime']=fcst_hr
  grb.values[:]=(grbs[0][i].values+grbs[1][i].values)/2.
  msg = grb.tostring()
  grbout.write(msg)
