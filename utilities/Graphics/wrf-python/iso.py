from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature
import sys
from datetime import datetime, timedelta
from wrf import (getvar, interplevel, to_np, latlon_coords, get_cartopy,
                 cartopy_xlim, cartopy_ylim)

# Open the NetCDF file
d=sys.argv[1] #domain
t=int(sys.argv[2]) #iobaric value
mt='03'
dt='29'
dt2='31'
ncfile = Dataset("wrfout_d0"+d+"_2019-"+mt+"-"+dt+"-"+dt2)

iso=500 #int(sys.argv[2]) #iobaric value
# Extract the pressure, geopotential height, and wind variables
shp = [7]+list(getvar(ncfile, "pressure").shape)
p0=np.zeros(shape=shp)
z0=np.zeros(shape=shp)
tlst=[i for i in range(4,41,6)]
for it in tlst:
  i=tlst.index(it)
  p0[i,:,:,:] = getvar(ncfile, "pressure",timeidx=it)
  z0[i,:,:,:] = getvar(ncfile, "z", units="dm",timeidx=it)
ht_iso0 = interplevel(z0, p0, iso)
fac=1.01
n=2     #frequency of wind bars
if d=='4':
  n=5
  fac=1.0007
elif d=='3':
  fac=1.002
mx,mn=10**(np.max(ht_iso0)*fac/100.),10**(np.min(ht_iso0)/100)

levels0= np.arange(mn, mx, (mx-mn)/10)
levels = [np.log10(i)*100 for i in levels0]

p = getvar(ncfile, "pressure",timeidx=t)
z = getvar(ncfile, "z", units="dm",timeidx=t)
ua = getvar(ncfile, "ua", units="kt",timeidx=t)
va = getvar(ncfile, "va", units="kt",timeidx=t)
wspd = getvar(ncfile, "wspd_wdir", units="kts",timeidx=t)[0,:]

# Interpolate geopotential height, u, and v winds to 500 hPa
ht_iso = interplevel(z, p, iso)
u_iso = interplevel(ua, p, iso)
v_iso = interplevel(va, p, iso)
wspd_iso = interplevel(wspd, p, iso)

# Get the lat/lon coordinates
lats, lons = latlon_coords(ht_iso)

# Get the map projection information
cart_proj = get_cartopy(ht_iso)

# Create the figure
fig = plt.figure(figsize=(12,9))
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="10m",
                             facecolor="none",
                             name="admin_1_states_provinces")
ax.add_feature(states, linewidth=0.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)

# Add the 500 hPa geopotential height contours
contours = plt.contourf(to_np(lons), to_np(lats), to_np(ht_iso),
                       levels=levels, #colors="rainbow",#"black",
                       cmap=get_cmap("rainbow"),
                       transform=crs.PlateCarree())
plt.colorbar(contours, ax=ax, orientation="vertical",pad=.05) #"horizontal", pad=.05)

# Add the wind speed contours
#levels = [2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
#wspd_contours = plt.contourf(to_np(lons), to_np(lats), to_np(wspd_iso),
#                             levels=levels,
#                             cmap=get_cmap("rainbow"),
#                             transform=crs.PlateCarree())
#plt.clabel(contours, inline=1, fontsize=10, fmt="%i")

# Add the 500 hPa wind barbs, only plotting every 125th data point.
plt.barbs(to_np(lons[::n,::n]), to_np(lats[::n,::n]),
          to_np(u_iso[::n, ::n]), to_np(v_iso[::n, ::n]),
          transform=crs.PlateCarree(), length=5)

# Set the map bounds
ax.set_xlim(cartopy_xlim(ht_iso))
ax.set_ylim(cartopy_ylim(ht_iso))

ax.gridlines()

bdate=datetime(2019,int(mt),int(dt),8)
sdate=(bdate+timedelta(hours=t)).strftime("%Y-%m-%d_%H:00L")
plt.title(str(iso)+" hPa Height (m), Barbs (kt)@"+sdate)

#plt.show()
plt.savefig(str(iso)+'_'+'{:02d}'.format(t)+'D'+d+'.png')
