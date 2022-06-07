#!/opt/anaconda3/bin/python
import numpy as np
from pykml import parser
import fortranformat as ff
import sys, os
from pyproj import Proj
import twd97

def rd_kmlLL(fname):
  kml_file = os.path.join(fname)
  with open(kml_file) as f:
      doc = parser.parse(f).getroot()

#tags for Placemark, Polygon and Point
  plms=doc.findall('.//{http://www.opengis.net/kml/2.2}Placemark')
  try:
    names=[str(i.ExtendedData.Data.value) for i in plms]
  except:
    print ('names must contain building/stack height(m) for objects.')
    sys.exit('names must contain building/stack height(m) for objects.')
  lnks=doc.findall('.//{http://www.opengis.net/kml/2.2}LineString')
  pnts=doc.findall('.//{http://www.opengis.net/kml/2.2}Point')

  plm_tag=[str(i.xpath).split()[-1][:-2] for i in plms]
  #seq of polygon or point
  lnk_prt=[str(i.getparent().values).split()[-1][:-2] for i in lnks]
  pnt_prt=[str(i.getparent().values).split()[-1][:-2] for i in pnts]
  idx_lnk=[plm_tag.index(i) for i in lnk_prt]
  idx_pnt=[plm_tag.index(i) for i in pnt_prt]
  nplms=len(plms)
  nlnks=len(lnks)
  npnts=len(pnts)
#TYP,VPH,EMF,HGT,WID for the link segment must labelled FOLLOWING the name strings
  delim=',;_/ |-('
  nms,TYP,VPH,EMF,HGT,WID=[],[],[],[],[],[]
  for ii in range(nlnks):
    i=idx_lnk[ii]  
    ipas=0
    for d in delim:
      names[i]=names[i].strip(d)	
      if d in names[i]:
        if d=='(':names[i].replace(')')
        while d+d in names[i]:
          names[i]=names[i].replace(d+d,d)
        nms.append(names[i].split(d)[0])
        TYP.append(names[i].split(d)[1])
        VPH.append(float(names[i].split(d)[2].replace('veh/hr','').replace('VEH/HR','')))
        EMF.append(float(names[i].split(d)[3].replace('g/mile','').replace('G/MILE','')))
        HGT.append(float(names[i].split(d)[4].replace('m','').replace('M','')))
        WID.append(float(names[i].split(d)[5].replace('m','').replace('M','')))
        ipas=1
        break
    if ipas==0:
      print ('name must contain building/stack height(m) for object:'+names[i])
      sys.exit('name must contain building/stack height(m) for object:'+names[i])


  #collect lon/lat for polylines
  lon=np.zeros(shape=(nlnks,50))
  lat=np.zeros(shape=(nlnks,50))
  for lnk in lnks:
    ilnk=lnks.index(lnk)
    coord=lnk.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    c=coord[0].pyval.split()
    n=0
    for ln in c:
      lon[ilnk,n]=ln.split(',')[0]
      lat[ilnk,n]=ln.split(',')[1]
      n+=1
      
  #collect lon/lat for points
  lonp=np.zeros(shape=(npnts))
  latp=np.zeros(shape=(npnts))
  hgts=np.zeros(shape=(npnts))
  for pnt in pnts:
    ipnt=pnts.index(pnt)
    coord=pnt.findall('.//{http://www.opengis.net/kml/2.2}coordinates')
    ln=coord[0].pyval.split()[0]
    lonp[ipnt]=ln.split(',')[0]
    latp[ipnt]=ln.split(',')[1]
  for k in range(npnts):
    ipas=0
    i=idx_pnt[k]
    for d in delim:
      names[i]=names[i].strip(d)
      if d in names[i]:
        while d+d in names[i]:
          names[i]=names[i].replace(d+d,d)
        hgts[k]=float(names[i].split(d)[1].replace('m','').replace('M',''))
        nms.append(names[i].split(d)[0])
        ipas=1
        break
    if ipas==0:nms.append(names[i])
  hgts=HGT+list(hgts)
  return nlnks,npnts,nms,hgts,lon,lat,lonp,latp,TYP,VPH,EMF,WID

fname=sys.argv[1]
NS,NR,nms,hgts,lon,lat,lonp,latp,TYPs,VPHs,EMFs,WIDs=rd_kmlLL(fname)
Longitude_Pole=np.mean([i for i in lon.flatten() if i!=0.]+list(lonp)) 
Latitude_Pole=np.mean([i for i in lat.flatten() if i!=0.]+list(latp))  
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40, lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)

job=fname.replace('.kml','')
ATIM,z0,vs,vd,SCAL=60,100,0,0,1
run=job+'_By_KML2INP'
NM=8
parm={'U':1.0,'CLAS':6,'MIXH':100,'AMB':1.0}
for var in 'U CLAS MIXH AMB'.split():
  exec(var+'=[parm["'+var+'"] for i in range(NM)]')
BRG=[45*i for i in range(NM)]
#receptors
recp,zr=nms[NS:],hgts[NS:]
xr,yr=pnyc(lonp, latp, inverse=False)
xr=[int(i+Xcent) for i in xr]
yr=[int(i+Ycent) for i in yr]
  
#links
NL,(lnks,X1,Y1,X2,Y2,TYP,VPH,EMF,H,W)=0,([] for i in range(10))
for l in range(NS):
  llt=[i for i in lat[l,:] if i !=0]
  lln=[i for i in lon[l,:] if i !=0]
  x,y=pnyc(lln, llt, inverse=False)
  x=[int(i+Xcent) for i in x]
  y=[int(i+Ycent) for i in y]
  X1+=x[:-1]
  Y1+=y[:-1]
  X2+=x[1:]
  Y2+=y[1:]
  ms=len(llt)-1
  lnks+=[nms[l]+'_'+str(i) for i in range(ms)]
  TYP+=[TYPs[l] for i in range(ms)]
  VPH+=[VPHs[l] for i in range(ms)]
  EMF+=[EMFs[l] for i in range(ms)]
  H+=[hgts[l] for i in range(ms)]
  W+=[WIDs[l] for i in range(ms)]
  NL+=ms
    
#1:SITE VARIABLES, 2:RECEPTOR LOCATIONS, 3:RUN CASE, 4:LINK VARIABLES, 5:MET CONDITIONS
fmt=['A40,2F4.0,2F5.0,I2,F10.0','A20,3F10.0',  'A40,2I3',  'A20,A2,4I7,F8.0,3F4.0',      'F3.0,F4.0,I1,F6.0,F4.0']
var=[(job,ATIM,z0,vs,vd,NR,SCAL),(recp,xr,yr,zr),(run,NL,NM),(lnks,TYP,X1,Y1,X2,Y2,VPH,EMF,H,W),(U,BRG,CLAS,MIXH,AMB)]
nln=[1,NR,1,NL,NM]
lns=[]
for ig in range(5):
  w_line = ff.FortranRecordWriter(fmt[ig])
  if ig in [0,2]:
    lns.append(w_line.write([v for v in var[ig]])+'\n')
  else:
    for l in range(nln[ig]):
      lns.append(w_line.write([v[l] for v in var[ig]])+'\n')
fnameO=fname.replace('.kml','.inp')
with open(fnameO,'w') as f:
  for l in lns:
    f.write(l)

