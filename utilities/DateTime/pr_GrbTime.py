#$ cat ~/bin/pr_GrbTime.py
#!/opt/anaconda3/bin/python
import sys
import netCDF4
import datetime
fname=sys.argv[1]
nc = netCDF4.Dataset(fname, 'r')
V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nchr=(nc.variables[V[1][0]].shape[i] for i in range(2))
SDATE=[datetime.datetime.strptime(''.join([str(i, encoding='utf-8') for i in list(nc.variables[V[1][0]][t, :])]),\
 '%m/%d/%Y (%H:%M)') for t in range(nt)]
for t in range(nt):
  print(t,SDATE[t])
