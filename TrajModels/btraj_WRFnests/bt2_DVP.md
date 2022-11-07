---
layout: default
title: 三維反軌跡線之計算
nav_order: 2
parent: btraj_WRFnests
grand_parent: Trajectory Models
last_modified_date: 2022-11-07 09:29:13
---

# WRF三維軌跡分析
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景
- 這支反軌跡線計算程式的特殊性在於：
  1. 以wrfout 3維風場為3個方向風速之數據來源。因垂直向的網格非等間距，需要特別處理。
  1. 因為是3維軌跡線，在近地面及高空最頂層，有可能離開模擬範圍，需要讓計算迴圈可以停止。
  1. 由於多數後處理與繪圖軟體是2維架構，需要將高度結果妥善安排。＿
  1. 做為後續wrfout2維地面反軌跡計算程式(ftuv10.py)的原型，程式所定義的函數需更通用化。

## 自定義函數
### get_uvw
- 這個函數的用意在於讀取wrfout中特定時間、空間的風速數據，

```python
#get the UVW data from NC files
#z not interpolated yet
def get_uvw(ncft,t0,z,y,x):
  (ncf,t1)=ncft[:]
  t=abs(t1-t0)
  n0=locate_nest(x,y)
  #make sure the point is in d1(at least)
  if n0==-1:
    return -1
  iii=int(x//dx[4]+ncol[4]//2)
  jjj=int(y//dx[4]+nrow[4]//2)
  kkk=int(z//dz)
  idx=(t,kkk,jjj,iii)
  if idx in f: return idx,f

  #loop for every possible nest
  for n in range(n0,n0-1,-1):
    ix=int(x//dx[n]+ncol[n]//2)
    iy=int(y//dx[n]+nrow[n]//2)
#   print(ix,iy)
    iz=bisect.bisect_left(zh[n][t1,:,iy,ix],z)

    #the data are stored in the vast, sparce matrix
    for k in range(max(0,iz-1),min(iz+3,nlay[n])):
      kk=int(z//dz)
      for j in range(max(0,iy-1),min(iy+3,nrow[n])):
        jj=int((j-nrow[n]//2)*fac[n] +nrow[4]//2)
        for i in range(max(0,ix-1),min(ix+3,ncol[n])):
          ii=int((i-ncol[n]//2)*fac[n] +ncol[4]//2)
          if (t,kk,jj,ii) in withdata:continue
          #average the stagger wind to the grid_points
          uvwg[0,t,kk,jj,ii]=(ncf[n].variables['U'][t1,k,j,i]+ncf[n].variables['U'][t1,k,j,i+1])/2.
          uvwg[1,t,kk,jj,ii]=(ncf[n].variables['V'][t1,k,j,i]+ncf[n].variables['V'][t1,k,j+1,i])/2.
          uvwg[2,t,kk,jj,ii]=(ncf[n].variables['W'][t1,k,j,i]+ncf[n].variables['W'][t1,k+1,j,i])/2.
          #np.where(abs(uvwg)>0) is too slow, remember the locations directly
          withdata.append((t,kk,jj,ii))
  wd2=[i[2] for i in withdata]
  wd3=[i[3] for i in withdata]
  xx,yy=x_g[wd2,wd3], y_g[wd2,wd3]
  if n0<3:
    xx_mesh, yy_mesh=np.arange(min(xx),max(xx)+1,3000),np.arange(min(yy),max(yy)+1,3000)
    iis,jjs=x_mesh.index(min(xx)),  y_mesh.index(min(yy))
    iie,jje=x_mesh.index(max(xx))+1,y_mesh.index(max(yy))+1
    xxg, yyg = np.meshgrid(xx_mesh, yy_mesh)
    for Lv in range(3):
      points=[(i,j) for i,j in zip(xx,yy)]
      grid_z2 = griddata(points, uvwg[Lv,t,kk,wd2,wd3], (xxg, yyg),  method='cubic')      
      uvwg[Lv,t,kk,jjs:jje,iis:iie]=grid_z2
  fcn=[]
#  for Lv in range(3):
#    try:
#      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='cubic'))
#    except:
#      fcn.append(interpolate.interp2d(yy, xx, uvwg[Lv,t,kk,wd2,wd3], kind='linear'))
#  f.update({idx:fcn})
  return idx,f
```

### openNC
- 按照輸入的日期開啟wrfout的nc檔
- 一次開啟所有範圍之wrfout(d01~d04)
- 回應

```python
#open the NC's for some day (this present day, first time, or next/yesterday)
def openNC(sdate):
  ymd = sdate.strftime('%Y-%m-%d')
  fnames=['links/wrfout_d0'+str(i)+'_'+ymd+'_00:00:00' for i in range(1,5)]
  ncf,nt,nlay,nrow,ncol=[],[],[],[],[]
  for fname in fnames:
    if not os.path.isfile(fname): sys.exit('no file for '+fname)
    nc1=netCDF4.Dataset(fname,'r')
    ncf.append(nc1)
    v4=list(filter(lambda x:nc1.variables[x].ndim==4, [i for i in nc1.variables]))
    t,lay,row,col=nc1.variables['T'].shape
    for v in 't,lay,row,col'.split(','):
      exec('n'+v+'.append('+v+')')
  return ncf, nt, nlay, nrow, ncol, ymd.replace('-','')```


### locate_nest
- 這個函數用在判定(x, y)所在位置的網格系統
- 因3層網格系統均以臺灣為中心，因此判別自最內圈開始，如果符合隨即跳出
- 判定原則以座標值是否都在該系統之範圍
- 最外圈(`locate_nest=0`)~最內圈(`locate_nest=0`)之
  - `dx=[81000,27000,9000,3000,3000]`
  - 
```python
def locate_nest(x,y):
    for n in range(3,-1,-1):
        if xmin[n]<=x<xmax[n] and ymin[n]<=y<ymax[n]:
            return n
    return -1
```