---
layout: default
title: Rotate KML
parent: SO Pathways
grand_parent: Plume Models
nav_order: 4
last_modified_date: 2022-03-08 10:16:34
---
# 煙囪及建築物座標系統之旋轉計算
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
- [地圖數位板](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/digitizer)作業的結果是經緯度座標、而作為煙流模式前處理[BPIP](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP)的輸入檔，必須是沒有歪斜的XY直角座標系統，需要進一步轉換。
- 尤有進者，實際個案的工廠北或多或少都會與背景地圖的真北有所偏差(**夾角D**)，因此都必須進行平移及旋轉，才能適用該前處理程式，並且不會發生疊圖誤差。
- 煙流模式對於風向是非常敏感的，風向的0度是真北，因此**夾角D**對煙流地面濃度的走向、建築物的影響等等，都有絕對的影響。經由數位板與此處的計算，可以降低量測與計算造成誤差的可能性。
- 除此之外，程式還提供由背景資料中找到個案所在地的**煙囪基地高程E**([步驟5](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容))、煙囪頂的**離地高度H**([步驟6](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP/#設定步驟與內容))等功能，以便進行計算。

## 輸入檔
- 此處設定為[KML格式](https://zh.wikipedia.org/wiki/KML)檔案，範例如[example.kml](http://114.32.164.198/isc_results/example.kml)
- 使用KML格式的理由詳見[討論](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/RemoteSystem/aermods/#以kml檔案做為輸入座標介面的理由)

### 輸入檔說明
- 必須資訊
  - 煙囪位置(點)：將做為模擬個案之中心座標
  - 囪煙名稱：此名稱將做為下述應用的個案名稱，  
    - 污染源名稱、
    - 模式輸出檔案名稱
    - 氣象檔案名稱（適用於同一3Km網格範圍的其他個案）
- 輔助資訊
  - 建築物頂點位置(多邊形)：方向不拘
  - 建築物名稱(含高度、名稱高度間可以空格、逗號、分號、斜槓等區格)
  - 煙囪如有高度跟在名稱之後，將會優先使用，否則會從TEDS資料庫中選取位置最接近的煙囪。
- 可以使用數位板點取座標值（詳見[地圖數位板](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/digitizer/)、另存成KML檔案）。
- 檢核：
  - rotate_kml→旋轉角度，輸出成bpip輸入檔格式
  - [iscParser](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)→解讀bpip輸入檔，輸出成kml格式(反解)
- KML內之順序：(不限)
- 高度附掛單位（m or M)不影響計算，一律設定是m

## CGI_Python程式設計
### 旋轉平移
- 對某一點旋轉座標：參考[網友](https://math.stackexchange.com/questions/384186/calculate-new-positon-of-rectangle-corners-based-on-angle)之程式碼
  - 同一副程式應用在[isc_parser.py](https://github.com/sinotec2/CGI_Pythons/blob/main/drawings/isc_parser/isc_parser.py)系列、[rd_kmlFull.py]()系列。

```python
    10    def rotate_about_a_point(target_point,center_point,angle_rs):
    11      cp=np.subtract(target_point,center_point)
    12      px=cp[0]*math.cos(math.radians(angle_rs))+cp[1]*-math.sin(math.radians(angle_rs))
    13      py=cp[0]*math.sin(math.radians(angle_rs))+cp[1]*math.cos(math.radians(angle_rs))
    14      return(np.add([px,py],center_point))
```
- 先審視是否太過偏斜：
  - 絕大工廠的廠房都是矩形，此處設定偏斜的標準為各建築物4面之角度的標準偏差>10度 (第75行)

```python
    69  dir=np.zeros(shape=(nplgs,4)) 
    70  for i in range(nplgs): 
    71    diri=[90-math.atan2((y[i,j+1]-y[i,j]),(x[i,j+1]-x[i,j]))*180/math.pi for j in range(4)] 
    72    diri.sort() 
    73  #  from North and clockwise 
    74    dir[i,:]=np.array(diri) 
    75  if max( [np.std(dir[:,j]) for j in range(4)])>10: 
    76    print ('wrong direction or skewed!</br>') 
    77    for i in range(nplgs): 
    78      print (('dir for building# {:d} is: {:f} {:f} {:f} {:f}</br>').format(i,*dir[i,:])) 
    79    print ('</body></html>') 
    80    sys.exit('wrong direction or skewed!') 
```      
- 找到最小旋轉角度
- 針對原點(KML輸入檔案的第1點，第85行)、做旋轉(第86行)、再做平移(89\~90行)

```python
    82  P=[(i,j) for i,j in zip(x[:,:4].flatten(),y[:,:4].flatten())]
    83  angl= min([np.mean(dir[:,j]) for j in range(4)])
    84  if angl<0:angl+=360.
    85  orig=P[0]
    86  Pn=[rotate_about_a_point(pnt,orig,angl) for pnt in P]
    87  Pn=np.array(Pn).flatten().reshape(nplgs,4,2)
    88  #mnx, mny=(np.min(Pn[:,:,i]) for i in range(2))
    89  Pn[:,:,0]+=-orig[0] #-mnx
    90  Pn[:,:,1]+=-orig[1] #-mny
```

### 重整點位順序
- 校正數位化造成的不準度
- 讓bpip.inp內建築物的頂點為西南開始，逆時針順序輸入
- 找到最接近0點的頂點，做為原點，並補足每一點的不準度偏差(dx,dy)
- 煙囪點也同樣旋轉、平移(但沒有校正不準度)

```python
    92  for i in range(nplgs):
    93    xm,ym=np.mean(Pn[i,:,0]),np.mean(Pn[i,:,1])
    94    x1=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] < xm])/2
    95    x2=sum([Pn[i,j,0] for j in range(4) if Pn[i,j,0] > xm])/2
    96    y1=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] < ym])/2
    97    y2=sum([Pn[i,j,1] for j in range(4) if Pn[i,j,1] > ym])/2
    98    Pn[i,0,0],Pn[i,3,0]=x1,x1
    99    Pn[i,1,0],Pn[i,2,0]=x2,x2
  100    Pn[i,0,1],Pn[i,1,1]=y1,y1
  101    Pn[i,2,1],Pn[i,3,1]=y2,y2
  102    if i==0:
  103      dist=(Pn[i,:,0])**2+(Pn[i,:,1])**2
  104      idx=np.where(dist==np.min(dist))
  105      dx,dy=-Pn[i,idx[0],0],-Pn[i,idx[0],1]
  106  Pn[:,:,0]=Pn[:,:,0]+dx
  107  Pn[:,:,1]=Pn[:,:,1]+dy
...
  122  x,y=pnyc(lonp,latp, inverse=False)
  123  x+=Xcent
  124  y+=Ycent
  125  P=[(i,j) for i,j in zip(x,y)]
  126  Pp=[rotate_about_a_point(pnt,orig,angl) for pnt in P]
  127  Pp=np.array(Pp).flatten().reshape(npnts,2)
  128  Pp[:,0]+=-orig[0] #-mnx
  129  Pp[:,1]+=-orig[1] #-mny
```

### 從既有資料庫中找到需要的數據
- 基地高程：使用UCAR 333M解析度檔案(WPS之geo_em格式)

```python
  36  geo_name='/Users/WRF4.1/WPS/geo_em.d04_333m.nc'
...
  108  nc = netCDF4.Dataset(geo_name, 'r')
  109  v='HGT_M'
  110  c=np.array(nc.variables[v][0,:,:])
  111  for v in ['CLAT','CLONG']:
  112      exec(v+'=nc.variables[v][0,:,:]')
  113  xg,yg=pnyc(CLONG,CLAT, inverse=False)
  114  xg+=Xcent
  115  yg+=Ycent
  116  base=[]
  117  for ii in range(nplgs):
  118    i=ii*4
  119    d=(xg-P[i][0])*(xg-P[i][0])+(yg-P[i][1])*(yg-P[i][1])
  120    idx=np.where(d==np.min(d))
  121    base.append(c[idx[0][0],idx[1][0]])
```  
- 從TEDS資料庫中找到煙囪高度

```python
    37  tedsp_name=WEB+'isc_results/point_QC.csv'
...
  131  #the stack heights are read from TEDS database IF that hgts are not contained in the name strings
  132  df=read_csv(tedsp_name)
  133  df.UTM_E+=Xcent
  134  df.UTM_N+=Ycent
  135  a=[]
  136  for ll in range(1,6):
  137    L=ll*1000
  138    a=df.loc[df.UTM_E.map(lambda s:abs(s-P[0][0])<L) & df.UTM_N.map(lambda s:abs(s-P[0][1])<L)]
  139    if len(a)>0:
  140      df=a
  141      break
  142  if len(a)==0:
  143    print ('the point source seems not existing in database. </body></html>')
  144    sys.exit('fail')
  145  cole=['CO_EMI', 'NMHC_EMI', 'NOX_EMI', 'PM25_EMI', 'PM_EMI', 'SOX_EMI']
  146  c2m={'SOX':64,'NOX':46,'CO':28,'PM25':24.5,'PM':24.5,'NMHC':12*4+10}
  147  unit={i:'ppb' for i in c2m if 'PM' not in i}
  148  unit.update({i:'ug/m3' for i in c2m if 'PM' in i})
  149  hdtv=[ 'HEI', 'DIA', 'TEMP', 'VEL']
  150  tims=[ 'DY1', 'HD1', 'HY1']
  151  for v in cole+hdtv+tims:
  152    exec(v+'=[]')
  153  for k in range(npnts):
  154    df['dist']=[np.sqrt((i-P[k][0])**2+(j-P[k][1])**2) for i,j in zip(list(df.UTM_E),list(df.UTM_N))]
  155    idx=df.loc[df.dist==min(df.dist)].index
  156    if len(idx)>1:
  157      idx=df.loc[idx].sort_values('HEI',ascending=False).head(1).index
  158    for v in cole+hdtv+tims:
  159      exec(v+'.append(list(df.'+v+'[idx])[0])')
  160    if len(hgts)<nplgs+npnts:
  161      hgts.append(list(df.HEI[idx])[0])
  162  for v in cole:
  163    exec(v+'=['+v+'[i]/HY1[i]/3.6*1000. for i in range(npnts)]')
  164  TEMP=[i+273 for i in TEMP]
```  
### 輸出到bpip.inp檔案
- 命名為**fort.10**，以符合[BPIP](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/BPIP)程式的約定。以隨機產生的目錄名稱做為使用者個案間的辨識。

```python
  172  with open(pth+'fort.10','w') as f:
  173    f.write(("'BPIP input file with "+'{:2d}'+' bldg and '+'{:2d}'+" stacks,originated at [{:.1f},{:.1f}](TWD97m).'\n")
  174    .format(nplgs,npnts,orig[0],orig[1]))
  175    f.write(("'P'\n"+"'METERS' 1.00\n'UTMN',"+'{:5.0f}\n').format(angl))
  176    f.write(('{:2d}\n').format(nplgs))
  177    for i in range(nplgs):
  178      f.write(("'"+names[i]+"' 1"+'{:6.1f}\n').format(base[i]))
  179      f.write(('4 '+'{:5.0f}\n').format(hgts[i]))
  180      for j in range(4):
  181        f.write(('{:5.1f}  {:5.1f}\n').format(Pn[i,j,0],Pn[i,j,1]))
  182    f.write(('{:2d}\n').format(npnts))
  183    for i in range(npnts):
  184      ii=i+nplgs
  185      f.write(("'"+names[ii]+"' "+'{:6.1f} {:6.1f} {:6.1f} {:6.1f} \n').format(base[ii],hgts[ii],Pp[i,0],Pp[i,1]))
```  
### CGI_Python下載
- [rotate_kml.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/rotate_kml.py)

## RESULTS
### CaaS
- [Rotate a KML file](http://114.32.164.198/rotate_kml.html)

### 結果檢視
- 檢討由KML產生bpip.inp，再由[iscParser](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/SO_pathways/iscParser)檢查，結果如下([TSMC.kml](http://114.32.164.198/isc_results/TSMC/TSMC.kml))
  - 並無系統性之錯誤
  - 仍然存在描圖的不準度，然誤差已在可接受範圍。
  - 建築物輪廓線尚可保持方向之一致性

| ![rotate_KML.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/rotate_KML.png)|
|:--:|
| <b>數位化、且經旋轉、歪斜修正後的廠房位置圖</b>|


## Reference
- Mathematics Stack Exchange, [calculate new positon of rectangle corners based on angle](https://math.stackexchange.com/questions/384186/calculate-new-positon-of-rectangle-corners-based-on-angle)



