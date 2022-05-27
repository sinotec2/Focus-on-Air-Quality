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
iso=850
d=sys.argv[1] #domain
t=int(sys.argv[2]) #iobaric value
n=2	#frequency of wind bars
if d=='4':n=4
mt='03'
dt='29'
dt2='31'
ncfile = Dataset("wrfout_d0"+d+"_2019-"+mt+"-"+dt+"-"+dt2)
# Extract the pressure, geopotential height, and wind variables
shp = [7]+list(getvar(ncfile, "pressure").shape)
p0=np.zeros(shape=shp)
T=np.zeros(shape=shp)
W=np.zeros(shape=shp)
tlst=[i for i in range(4,41,6)]
for it in tlst:
  i=tlst.index(it)
  p0[i,:,:,:] = getvar(ncfile, "pressure",timeidx=it)
  T[i,:,:,:] = getvar(ncfile, "eth",units="K",timeidx=it)
  W[i,:,:,:] = getvar(ncfile, "omg",timeidx=it)*3600./100.
lvls=[500,700,850,1000]
for lvl in lvls:
  ilvl=lvls.index(lvl)
  slvl=str(lvl)
  exec("T"+slvl+" = interplevel(T, p0, "+slvl+")")
#  check eth at mountain region, if nan, let equal to upper layer THE(adiabatic condition)
  if lvl>500:
    uplvl=str(lvls[ilvl-1])
    exec("T"+slvl+" = np.where(np.isnan(T"+slvl+"),T"+uplvl+",T"+slvl+")")
KO0 = ((T700 + T500) - (T850 + T1000))/2.
mx,mn=np.round(np.max(W)*1.2,0),np.round(np.min(W),0)
mn,mx=-54,1
levels = list(range(mn,-22,8))+list(range(-22,mx,2))
i=tlst.index(t)
p = getvar(ncfile, "pressure",timeidx=t)
z = getvar(ncfile, "z", units="dm",timeidx=t)
ua = getvar(ncfile, "ua", units="kt",timeidx=t)
va = getvar(ncfile, "va", units="kt",timeidx=t)
omg = getvar(ncfile, "omg",timeidx=t)*3600/100 #Pa/s -> hPa/Hr

# Interpolate geopotential height, u, and v winds to 500 hPa
KO = KO0[i,:,:]
u_iso = interplevel(ua, p, iso)
v_iso = interplevel(va, p, iso)
omg_iso = interplevel(omg, p, 500)
field=to_np(omg_iso)
field=np.where(field<mn,mn,field)


# Get the lat/lon coordinates
lats, lons = latlon_coords(u_iso)

# Get the map projection information
cart_proj = get_cartopy(u_iso)

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
contours = plt.contourf(to_np(lons), to_np(lats), field,
                       levels=levels, #colors="rainbow",#"black",
                       cmap=get_cmap("plasma"),
                       transform=crs.PlateCarree())
plt.colorbar(contours, ax=ax, orientation="vertical",pad=.05) #"horizontal", pad=.05)

# Add the KO index contour lines
levels = range(-25,30,5)
contours = plt.contour(to_np(lons), to_np(lats), to_np(KO),
                             levels=levels,
                             linewidths=1.,
                             cmap=get_cmap("winter_r"), #colors="black",
                             transform=crs.PlateCarree())
plt.clabel(contours, inline=1, fontsize=10, fmt="%i")

# Add the KO index contour line for KO=0
contours = plt.contour(to_np(lons), to_np(lats), to_np(KO),
                             levels=[0.],
                             colors="black",
                             transform=crs.PlateCarree())
plt.clabel(contours, inline=1, fontsize=10, fmt="%i")

# Add the 500 hPa wind barbs, only plotting every 125th data point.
plt.barbs(to_np(lons[::n,::n]), to_np(lats[::n,::n]),
          to_np(u_iso[::n, ::n]), to_np(v_iso[::n, ::n]),
          transform=crs.PlateCarree(), length=5)

# Set the map bounds
ax.set_xlim(cartopy_xlim(u_iso))
ax.set_ylim(cartopy_ylim(u_iso))

ax.gridlines()

bdate=datetime(2019,int(mt),int(dt),8)
sdate=(bdate+timedelta(hours=t)).strftime("%Y-%m-%d_%H:00L")
plt.title('KO index(lines), 500Pa Omega (hPa/Hr) and '+str(iso)+" hPa Barbs (kt)@"+sdate)

#plt.show()
plt.savefig(str(iso)+'_'+'{:02d}'.format(t)+'D'+d+'.png')
