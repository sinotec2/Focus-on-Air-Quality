---
layout: default
title:  VERDI圖面解析度之改善
parent: VERDI
grand_parent: Graphics
last_modified_date: 2022-03-18 14:02:50
---

# VERDI圖面解析度之改善

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

## 前言
### VERDI解析度不足的困難 
VERDI是模式模擬過程中常用、好用的顯示軟體，也是美國環保署提供給網格模擬社群的公開軟體。詳細說明可以參考VERDI官網或筆記。

一般來說VERDI的等值圖只有一種，就是方塊圖(Tile、或稱為raster、色階圖)，並沒有等值線(contour)、等值色塊(shade)。為了忠實呈現輸入數據的數值與解析度，VERDI並不會進行空間與時間的內、外插，這對模擬過程中能確實檢討很有幫助。然而也有不方便的時候：

- 做簡報、呈現結果的時候。就必須另外用別的軟體重做一遍。
- 與其他不同來源數據進行比較的時候。彼此的解析度差異太大，視覺上無法做出直覺判斷。

### 解決方案
面對VERDI強烈的階梯狀的圖面，為了改善此一情況，使用者可以：
- 提高模式的解析度。然而此舉增加電腦的負荷、輸出入資料的處理量、也涉及資料本身的解析度問題。
- 提高色階數。此舉雖然可以有些遮掩，看起來似有連續的效果，但也模糊模擬結果的數量感。太多階層、太多資訊等於沒有資訊。
- 將數據進行空間的內插。圖面色階仍然維持既定數量級，然而網格之間進行內插，以保持原數據的空間合理性。

### 潛在困難與最終方案
空間內插會遇到的問題：
- 極值的消失：一般內插即為平緩均勻化(smothing)，會將模式模擬的極大、極低值抹去。
- 趨勢的消失：傳統的修邊程式是針對圖面上的鋸齒狀進行重新計算，是軟體層面的計算，並不考慮圖面的物理量，也可能造成趨勢的改變。
此處之解決方案：
- 採水平空間的 
  三次仿樣函數，數值方法詳細可以參考網頁說明。可以避免極值或趨勢被改變
- python的
  三次仿樣函數範例，可以參考官網說明。

## 程式設計重點
## 讀取d01數據檔案 
- 大多數模式輸出檔案都是5維的數據，然而也可能有4維的情形，如METCRO2D，沒有垂直項，因此需要做不同方式處理(line10~32)。
- 為減省程式計算的時間，如果數據全為0(sum==0)，不進行內插計算。(line13\~17、23\~27 )
- 讀取後，計算格點的座標值(直角座標系統、以臺灣為中心)(line33\~35)

## 模版之準備 
- netCDF雖然方便，但因為屬性細節太多，最好還是由既有模版來改就好了。
- 在此須事先準備好一IOAPI(model3 m3)格式、d01範圍、解析度為9Km的模版檔案(tmplateD1_9km.nc, line36\~37 )。
- hmp(home path為每個機器根目錄下第一層的定義，即為硬碟的目錄名稱，
  - master、DEVP、node01~node03為/nas1、
  - IMacKuang為/Users、
  - centos8為/data
  - (dev2為/nas3)
  - 每個機器設計的目錄名稱皆相同，可以減省系統平移時的困難。
- 讀取後，計算新格點(nc1)的座標值(直角座標系統、以臺灣為中心)(line43\~45)，此一程式的重點即在將(x,y)的值，內插到(x1, y1)系統上。

### 新網格nc1 範圍數據之篩選
- 確保選取到正確的點位進行內插，須先判斷點位是在新網格nc1的範圍內還是範圍外，先判斷x值、再進行y值的篩選。
- xyc即為在nc1範圍內的(x, y)配對的序列(line 49\~53)，對應到各點的濃度，即可進行cubic spline內插。
- 因新舊網格點位的對照(idxx, idxy, xyc...等)關係不會因為時間或污染物變數而有差異，因此必須先在迴圈外處理好，以減省時間。

### 時間與物理量項目之迴圈
- 每一時間、物理量項目的趨勢、極值分布都不相同，必須逐一進行內插。(line 64\~69)
- 內插使用griddata來進行，方式採cubic，即為三次仿樣函數。

```python
(py37)
kuang@master /nas1/ecmwf/near_real_time/gribs
$ cat -n D1_9km.py
     1  import netCDF4
     2  import numpy as np
     3  from scipy.interpolate import griddata
     4  
     5  import sys, os, subprocess
     6
     7  fname=sys.argv[1]
     8  nc = netCDF4.Dataset(fname,'r')
     9  V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
    10  if len(V[3])!=0:
    11    nt, nlay, nrow, ncol=nc.variables[V[3][0]].shape
    12    if nlay>1:sys.exit('not a vertical slice, please reduce LAY dim. by ncks "-d LAY,0,0" ')
    13    Vp=[]
    14    for v in V[3]:
    15      if np.sum(nc.variables[v][:])==0:continue
    16      Vp.append(v)
    17    nv=len(Vp)
    18    var=np.zeros(shape=(nv, nt, nrow, ncol))
    19    for iv in range(nv):
    20      var[iv,:,:,:]=nc.variables[Vp[iv]][:,0,:,:]
    21  elif len(V[2])!=0:
    22    nt, nrow, ncol=nc.variables[V[2][0]].shape
    23    Vp=[]
    24    for v in V[2]:
    25      if np.sum(nc.variables[v][:])==0:continue
    26      Vp.append(v)
    27    nv=len(Vp)
    28    var=np.zeros(shape=(nv, nt, nrow, ncol))
    29    for iv in range(nv):
    30      var[iv,:,:,:]=nc.variables[Vp[iv]][:,:,:]
    31  else:
    32    sys.exit('wrong matrix shapes')
    33  x_mesh=np.array([nc.XORIG+i*nc.XCELL for i in range(ncol)])
    34  y_mesh=np.array([nc.YORIG+j*nc.YCELL for j in range(nrow)])
    35  x, y = np.meshgrid(x_mesh, y_mesh)
    36  hmp=subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    37  tempf='/'+hmp+'/ecmwf/near_real_time/tmplateD1_9km.nc'
    38  fnameO=fname+'9'
    39  os.system('cp '+tempf+' '+fnameO)
    40  nc1= netCDF4.Dataset(fnameO,'r+')
    41  V1=[list(filter(lambda x:nc1.variables[x].ndim==j, [i for i in nc1.variables])) for j in [1,2,3,4]]
    42  nt1,nlay1,nrow1,ncol1=nc1.variables[V1[3][0]].shape
    43  x1d=[nc1.XORIG+nc1.XCELL*i for i in range(ncol1)]
    44  y1d=[nc1.YORIG+nc1.YCELL*i for i in range(nrow1)]
    45  x1,y1=np.meshgrid(x1d, y1d)
    46  maxx,maxy=x1[-1,-1],y1[-1,-1]
    47  minx,miny=x1[0,0],y1[0,0]
    48  
    49  idxx = np.where(abs(x) <= (maxx - minx) /2+nc1.XCELL*10)
    50  xc,yc = x[idxx],  y[idxx]
    51  idxy = np.where(abs(yc) <= (maxy - miny) /2+nc1.YCELL*10)
    52  ny=len(idxy[0])
    53  xyc= [(x[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]],y[idxx[0][idxy[0][i]],idxx[1][idxy[0][i]]]) for i in range(ny)]
    54
    55  for v in Vp:
    56    zz=nc1.createVariable(v,"f4",('TSTEP','LAY','ROW','COL'))
    57    nc1.variables[v].long_name    = nc.variables[v].long_name
    58    nc1.variables[v].units        = nc.variables[v].units
    59    nc1.variables[v].var_desc     = nc.variables[v].var_desc
    60
    61  for t in range(nt):
    62    for iv in range(nv):
    63      nc1.variables['TFLAG'][t,iv,:]=nc.variables['TFLAG'][t,0,:]
    64  for t in range(nt):
    65    for v in range(nv):
    66      c = np.array([var[iv,t,idxx[0][idxy[0][i]], idxx[1][idxy[0][i]]] for i in range(ny)])
    67      if np.sum(c)==0: continue
    68      nc1.variables[Vp[iv]][t, 0, :, :] = griddata(xyc, c, (x1, y1), method='cubic')
    69  nc1.SDATE,nc1.STIME=nc1.variables['TFLAG'][0,0,:]
    70  nc1.TSTEP=nc.TSTEP
    71  nc1.NVARS=nv
    72  nc1.close()
```

## CAMx模擬結果檢討

圖1為原始VERDI之圖面，由於數據解析度的限制(包括氣象與排放量檔案的解析度)，網格為53X53，解析度為81km。在珠江三角洲的西南側有最高值，在嶺南地區有最低值。

| ![D1_9Km1.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/D1_9Km1.png)|
|:--:|
| <b>原始VERDI之圖面，網格數53X53</b>|

圖2為內插後的結果(linear)：階梯狀完全消除、海面上色階可以呈現出合理的曲線。最大值不變，但範圍略有減少，仍能保持濃度顯著的空間梯度。最低值不變，但範圍顯著減少。東南沿海的4個較高網格連成一個高濃度帶，有模糊化的趨勢。

| ![D1_9Km2.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/D1_9Km2.png)|
|:--:|
| <b>線性內插結果，網格數增加9X9倍</b>|

圖3為內插後的結果(cubic)：較線性內插更圓緩，容許更大的濃度梯度。高低值範圍較linear更寬廣。

| ![D1_9Km3.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/D1_9Km3.png)|
|:--:|
| <b>cubic內插結果，網格數增加9X9倍</b>|


圖4為同一日[ecmwf](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/NRTdownload/)的GO3數據：模式對西側內地有低估，東南沿海則有高估。

| ![D1_9Km4.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/D1_9Km4.png)|
|:--:|
| <b>GO3再分析數據之內插結果</b>|


## 參考資料與連結
1. 連結 
  - [VERDI網站、下載點](http://www.cmascenter.org/verdi/)
  - VERDI手冊
    - [1.4版檔案](https://www.cmascenter.org/verdi/documentation/1.4.1/VerdiUserManual1.4.1.htm)
    - [1.5版官網](https://www.airqualitymodeling.org/index.php/VERDI_1.5_User_Manual)
    - VERDI筆記：[VERDI使用說明v2](http://www.evernote.com/l/AH2gBcV7qsJFr4E7jSW5x4A0FCoW4QW7otEpython) 
    - [python課綱筆記](http://www.evernote.com/l/AH30OmUntodEqYJyeIF1AreK8Z508_MHWCI/)
2. cubic spline 
  - 楊昌彪老師(2016)Spline Interpolation 的數學概念，[國立中山大學資訊系平行處理實驗室](http://par.cse.nsysu.edu.tw/~homework/algo01/9031636/new_page_2.htm)
  - [scipy.interpolate.CubicSpline](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html)
  - [scipy.interpolate.griddata](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html)
3. GO3 
  - Michela Giusti(2019)https://confluence.ecmwf.int/display/CUSF/GEMS+ozone
