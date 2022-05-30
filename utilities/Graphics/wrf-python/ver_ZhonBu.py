#!/opt/miniconda3/envs/geocat/bin/python
import numpy as np
from matplotlib import pyplot
from matplotlib.cm import get_cmap
from matplotlib.colors import from_levels_and_colors
from cartopy import crs
from cartopy.feature import NaturalEarthFeature, COLORS
from netCDF4 import Dataset
from wrf import (getvar, to_np, get_cartopy, latlon_coords, vertcross,
                 cartopy_xlim, cartopy_ylim, interpline, CoordPair)
import sys
from datetime import datetime, timedelta
from pyproj import Proj

wrf_file = Dataset("wrfout_d04_2019-01-29-31")
fname='BASE3_K24.nc' #24 levels run of EPA recommeded CMAQ system
nc=Dataset('K24TZ.nc') #BASE3_K24 without Taizhong PP grid emis
nc=Dataset('K24aTZ.nc') # BASE3_K24_w/o TZPP grids + TZPP pt_srce files(const and timvar)
nc=Dataset(fname)
t=int(sys.argv[1])
vn='O3'
unitd={'PM25_TOT':'ug/M3','O3':'ppb'}
pm=nc[vn][t,:,:,:]
nc=Dataset('METDOT3D_Taiwan.nc')
t0=35*24+t
UWIND=nc["UWIND"][t0,:,:-1,:-1]
VWIND=nc["VWIND"][t0,:,:-1,:-1]

# Define the cross section start and end points
cross_start = CoordPair(lat=24.453917871182558, lon=120.225062233815342)
cross_end = CoordPair(lat=23.41214780981217, lon=121.79586963982419)
cross_end = CoordPair(lat=22.915269693622275, lon=121.76321645608697) #Newpt

# calculate the angle cosine and sine values for correcting the U and V wind vectors
Latitude_Pole, Longitude_Pole = (cross_start.lat+cross_end.lat)/2,(cross_start.lon+cross_end.lon)/2
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
x0,y0=pnyc(cross_start.lon,cross_start.lat, inverse=False)
x1,y1=pnyc(cross_end.lon,cross_end.lat, inverse=False)
lent=np.sqrt((x1-x0)**2+(y1-y0)**2)
cost=(x1-x0)/lent
sint=(y1-y0)/lent

# Get the WRF variables
ht = getvar(wrf_file, "z", timeidx=t)
ter = getvar(wrf_file, "ter", timeidx=-1)
u = getvar(wrf_file, "ua", timeidx=t)
v = getvar(wrf_file, "va", timeidx=t)
#UV from mcip results
#u[:24,8:8+131,:92-12] = UWIND[:,:,12:]
#v[:24,8:8+131,:92-12] = VWIND[:,:,12:]
w = getvar(wrf_file, "wa", timeidx=t)
#U,W= 0.1**(u*cost+v*sint),0.1**(w*34)
U,W= u*cost+v*sint,w*34
Z=np.zeros(shape=U.shape)
Z[:11,8:8+131,:92-12] = pm[:,:,12:]

# Compute the vertical cross-section interpolation.  Also, include the
# lat/lon points along the cross-section in the metadata by setting latlon
# to True.
z_cross = vertcross(Z, ht, wrfin=wrf_file,start_point=cross_start,end_point=cross_end,latlon=True, meta=True)
u_cross = vertcross(U, ht, wrfin=wrf_file,start_point=cross_start,end_point=cross_end,latlon=True, meta=True)
w_cross = vertcross(W, ht, wrfin=wrf_file,start_point=cross_start,end_point=cross_end,latlon=True, meta=True)

# Convert back to dBz after interpolation
dbz_cross =z_cross
#u_cross=-np.log10(u_cross)
#w_cross=-np.log10(w_cross)

# Add back the attributes that xarray dropped from the operations above
dbz_cross.attrs.update(z_cross.attrs)
dbz_cross.attrs["description"] = "baseline "+vn
dbz_cross.attrs["units"] = "ug/m3"
w_cross.attrs.update(w_cross.attrs)
w_cross.attrs["description"] = "destaggered w-wind component"
w_cross.attrs["units"] = "m s-1"
u_cross.attrs.update(u_cross.attrs)
u_cross.attrs["description"] = "destaggered u-wind component"
u_cross.attrs["units"] = "m s-1"

# To remove the slight gap between the dbz contours and terrain due to the
# contouring of gridded data, a new vertical grid spacing, and model grid
# staggering, fill in the lower grid cells with the first non-missing value
# for each column.

# Make a copy of the z cross data. Let's use regular numpy arrays for this.
dbz_cross_filled = np.ma.copy(to_np(dbz_cross))
w_cross_filled = np.ma.copy(to_np(w_cross))
u_cross_filled = np.ma.copy(to_np(u_cross))

# For each cross section column, find the first index with non-missing
# values and copy these to the missing elements below.
for i in range(dbz_cross_filled.shape[-1]):
    column_vals = dbz_cross_filled[:,i]
    # Let's find the lowest index that isn't filled. The nonzero function
    # finds all unmasked values greater than 0. Since 0 is a valid value
    # for dBZ, let's change that threshold to be -200 dBZ instead.
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    dbz_cross_filled[0:first_idx, i] = dbz_cross_filled[first_idx, i]
for i in range(w_cross_filled.shape[-1]):
    column_vals = w_cross_filled[:,i]
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    w_cross_filled[0:first_idx, i] = w_cross_filled[first_idx, i]
for i in range(u_cross_filled.shape[-1]):
    column_vals = u_cross_filled[:,i]
    first_idx = int(np.transpose((column_vals > -200).nonzero())[0])
    u_cross_filled[0:first_idx, i] = u_cross_filled[first_idx, i]    

# Get the terrain heights along the cross section line
ter_line = interpline(ter, wrfin=wrf_file, start_point=cross_start,end_point=cross_end)

# Get the lat/lon points
lats, lons = latlon_coords(dbz)

# Get the cartopy projection object
cart_proj = get_cartopy(dbz)

# Create the figure
fig = pyplot.figure(figsize=(8,6))
ax_cross = pyplot.axes()

dbz_levels = np.arange(5., 75., 5.)
if 'BASE' in fname:
  dbz_levels = np.arange(5.,65.,5)
  if v=='O3':
    dbz_levels = np.arange(10.,120,10)
else:
  dbz_levels = np.arange(0.2,2,0.2)

# Create the color table found on NWS pages.
dbz_rgb = np.array([[4,233,231],
                    [1,159,244], [3,0,244],
                    [2,253,2], [1,197,1],
                    [0,142,0], [253,248,2],
                    [229,188,0], [253,149,0],
                    [253,0,0], [212,0,0],
                    [188,0,0],[248,0,253],
                    [152,84,198]], np.float32) / 255.0
# Make the cross section plot for dbz
xs = np.arange(0, dbz_cross.shape[-1], 1)
ys = to_np(dbz_cross.coords["vertical"])
dbz_contours = ax_cross.contourf(xs,
                                 ys[:-80],
                                 to_np(dbz_cross_filled)[:-80,:],
                                 levels=dbz_levels,
                                 cmap=get_cmap("rainbow"), #cmap=dbz_map,
                                 #norm=dbz_norm,
                                 extend="max")
# Add the color bar
cb_dbz = fig.colorbar(dbz_contours, ax=ax_cross)
cb_dbz.ax.tick_params(labelsize=8)
ax_cross.quiver(xs[::2], ys[:-80],
          to_np(u_cross_filled[:-80, ::2]), to_np(w_cross_filled[:-80, ::2]))

# Fill in the mountain area
ht_fill = ax_cross.fill_between(xs, 0, to_np(ter_line),
                                facecolor="saddlebrown")

# Set the x-ticks to use latitude and longitude labels
coord_pairs = to_np(dbz_cross.coords["xy_loc"])
x_ticks = np.arange(coord_pairs.shape[0])
x_labels = [pair.latlon_str() for pair in to_np(coord_pairs)]
lab=[[round(float(i),2) for i in j.split(',')] for j in x_labels[:]]
x_labels=[str(i[0])+','+str(i[1]) for i in lab]

# Set the desired number of x ticks below
num_ticks = 5
thin = int((len(x_ticks) / num_ticks) + .5)
ax_cross.set_xticks(x_ticks[::thin])
ax_cross.set_xticklabels(x_labels[::thin], rotation=45, fontsize=8)

# Set the x-axis and  y-axis labels
ax_cross.set_xlabel("Latitude, Longitude", fontsize=12)
ax_cross.set_ylabel("Height (m)", fontsize=12)

# Add a title
bdate=datetime(2019,1,29,8)
sdate=(bdate+timedelta(hours=t)).strftime("%Y-%m-%d_%H:00")
ax_cross.set_title("Cross-Section of "+vn+' '+unitd[vn]+'_'+sdate, {"fontsize" : 14})

#pyplot.show()
pyplot.savefig(vn+'_'+'{:02d}'.format(t)+'.png')


