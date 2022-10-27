#$ cat ~/bin/pr_GrbTime.py
#!/opt/anaconda3/envs/gribby/bin/python
import sys
import pygrib
fname=sys.argv[1]
grbs = pygrib.open(fname)
m=grbs.messages
if m <=100:
  dates=list(set([grbs[i].validDate for i in range(1,m+1)]))
else:
  dates=list(set([grbs[i].validDate for i in [1,m]]))n=len(dates)
if n>1:
  dates.sort()
for i in range(n):
  print(i,dates[i])