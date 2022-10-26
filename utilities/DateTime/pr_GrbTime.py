#$ cat ~/bin/pr_GrbTime.py
#!/opt/anaconda3/envs/gribby/bin/python
import sys
import pygrib
fname=sys.argv[1]
grbs = pygrib.open(fname)
dates=list(set([grbs[i].validDate for i in [1,grbs.messages]]))
n=len(dates)
if n>1:
  dates.sort()
for i in range(n):
  print(i,dates[i])