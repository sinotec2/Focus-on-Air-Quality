#!/opt/miniconda3/envs/geocat/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,
                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)
import sys, os, subprocess
from datetime import datetime, timedelta
from pyproj import Proj
from bisect import bisect

#判斷線性或對數濃度色階
def get_lev(N):
  if mxv/mnv>15:    
    dc=(np.log10(mxv)-np.log10(mnv))/15    
    level=[round(10**(dc*i+np.log10(mnv)),N) for i in range(15)]
    nm=colors.LogNorm(vmin=level[0], vmax=level[-1])
  else:
    i=int('{:e}'.format(mxv)[0])
    if i==7:i=6
    dc=i*10**int(np.log10(mxv))/nlev[i]
    level=[round(dc*i,N) for i in range(nlev[i])]
    nm=colors.Normalize(vmin=mnv, vmax=mxv)
  return level,nm
#2種線性間隔數
nlev={i:10 for i in [1,2,4,8]}
nlev.update({i:15 for i in [3,6,9]})

fname=sys.argv[1]
nc=Dataset(fname)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=nc.P_ALP, lat_2=nc.P_BET,lat_0=nc.YCENT, lon_0=nc.XCENT, x_0=0, y_0=0.0)
V=[list(filter(lambda x:nc[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
nt,nlay,nrow,ncol=nc.variables[V[3][0]].shape
yj=nc['TFLAG'][0,0,0]
t0=nc['TFLAG'][0,0,1]//10000
bdate=datetime(yj//1000,1,1,t0)+timedelta(days=int(yj%1000-1))

x1d=[nc.XORIG+nc.XCELL*i for i in range(ncol)]
y1d=[nc.YORIG+nc.YCELL*i for i in range(nrow)]
X,Y=np.meshgrid(x1d,y1d)
lons, lats= pnyc(X,Y, inverse=True)
xlab=[str(i) for i in np.arange(119.5, 123.5,0.5)]
ylab=[str(i) for i in np.arange(22, 25,0.5)]
xtics=[float(i) for i in xlab]
ytics=[float(i) for i in ylab]
im_ratio=nrow/ncol
ncfile = Dataset('wrfout_d04')
p = getvar(ncfile, "pressure",timeidx=0)
cart_proj = get_cartopy(p)
for v in V[3][:]:
  #極值只考慮正值範圍
  a=np.where(nc[v][:,0,:,:]>0,nc[v][:,0,:,:],0)  
  mxv=np.percentile(a,99.99)
  mnv=np.max([np.percentile(a,0.01),mxv/100])
  N=int(3-np.log10(mxv))
  level,nm=get_lev(N)    
  if len(level)!=len(set(level)):level,nm=get_lev(N+1)
  #格式必須在時間迴圈外設定好，避免有偏差，GIF會跳動
  fmt='%.'+str(N)+'f'     
  for t in range(nt):
    if np.max(nc[v][t,0,:,:])<mnv:continue
    fig = plt.figure(figsize=(int(10*ncol/nrow),10))
    ax = plt.axes(projection=cart_proj)
    # Download and add the states and coastlines
    states = NaturalEarthFeature(
        category="cultural", scale="10m",
        facecolor="none",
        name="admin_1_states_provinces")
    ax.add_feature(states, linewidth=0.5, edgecolor="black")
    ax.coastlines('10m', linewidth=0.8)
    contours = plt.contourf(lons, lats, nc[v][t,0,:,:] ,
                       levels=level, #colors="rainbow",#"black",
                       norm=nm,
                       cmap=get_cmap("rainbow"),
                       transform=crs.PlateCarree(),
                       extend='max')
    plt.colorbar(contours, ax=ax, orientation="vertical",pad=.05,format=fmt,fraction=0.047*im_ratio)
    ax.set_xlim(cartopy_xlim(p)+np.array([+0,-30000]))
    ax.set_ylim(cartopy_ylim(p)+np.array([+30000,-20000]))
    ax.gridlines()
    # Set the x-ticks to use latitude and longitude labels    
    ax.set_xticks(xtics,cart_proj) # Grid
#    ax.set_xticks(np.arange(118, 123.5,0.5), minor=True)
    ax.set_yticks(ytics,cart_proj) # Grid
    #    ax.set_yticks(np.arange(21.5, 25.5,0.5), minor=True)
    # Set the desired number of x ticks below

    # Set the x-axis and  y-axis labels
    ax.set_xlabel("meter", fontsize=12)
    ax.set_ylabel("meter", fontsize=12)

    sdate=(bdate+timedelta(hours=t)).strftime("%Y-%m-%d_%H:00Z")
    plt.title(fname.split('/')[-1]+" "+v+"("+nc[v].units.strip()+") @"+sdate)
    mxv=np.max(nc[v][t,0,:,:])
    N=int(3-np.log10(mxv))
    mxv=round(mxv,N)
    ax.annotate('max='+str(mxv),
            xy = (1.0, -0.1),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)
#    plt.show()
    png=v+'_'+'{:02d}'.format(t)+'.png'
    plt.savefig(png)
    plt.close()
    os.system('convert -bordercolor white -trim '+png+' tmp.png')
    os.system('convert -bordercolor white -border 5%x5% tmp.png '+png)
  if nt<6:continue #too short for GIF
  pngl=subprocess.check_output('ls -rt '+v+'*.png|tail -n1',shell=True).decode('utf8').strip('\n')
  if len(pngl)==0:continue
  size=subprocess.check_output('convert '+pngl+' -format "%wx%h" info:',shell=True).decode('utf8').strip('\n')
  os.system('convert  -dispose 2 -coalesce +repage -background none '+v+'_*.png -size '+size+' '+v+'.gif')
