#kuang@master /nas2/camxruns
#$ more ./2017/ICBC/bndextr/multBC.py
#!/cluster/miniconda/envs/py27/bin/python
import os
from PseudoNetCDF.camxfiles.lateral_boundary.Memmap import *
import argparse
ap = argparse.ArgumentParser()
#ap.add_argument("-m", "--month", required = True, type=str,help = "month#")
ap.add_argument("-s", "--spec", required = True, type=str,help = "SPEC")
ap.add_argument("-i", "--input", required = True, type=str,help = "input file")
ap.add_argument("-o", "--output", required = True, type=str,help = "output file")
ap.add_argument("-f", "--factors", required = True, type=float,help = "multiplier factor")
ap.add_argument("-l", "--lev", required = True, type=int,help = "level applied")
args = vars(ap.parse_args())
spec=args['spec']
fact=args['factors']
#mons=[args["month"]]
dirs=['NORTH','SOUTH','EAST','WEST']
#for mon in mons:
fname=args['input']
fnameO=args['output']
os.system('cp '+fname+' '+fnameO)
a=lateral_boundary(fnameO,'r+')
k=args['lev']
print fnameO
for d in dirs:
    varnam=d+'_'+spec
    a.variables[varnam][:,:,0:k]=a.variables[varnam][:,:,0:k]*fact
