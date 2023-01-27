---
layout: default
title:  NCLonOTM遠端服務
parent: CaaS to Graphs
grand_parent: Graphics
last_modified_date: 2023-01-24 05:17:03
tags: graphics CGI_Pythons KML plume_model OpenTopoMap
---
# NCLonOTM遠端服務
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

- 此一包裝程式提供了切割底圖與貼圖的服務
- 本項作業取代傳統SURFER、NCL、或[dat2kml](../../GIS/wr_kml.md)等繪圖方式，以cgi-python程式直接進行NCL與OTM地圖進行疊加，並以CaaS形式對外提供計算服務。
- 或參：[集合OTM圖磚並修剪成tiff檔](../CaaS/tiles_to_tiffFit.md)、[煙流模式結果繪製等值線圖](../NCL/PLT_cn.md)

### 整體策略檢討

(一)過去製圖方式之檢討

- 底圖的截取：
  - 從網頁畫面、使用剪取工具直接就所要的範圍進行截取
    - 無法得到指定座標的精確範圍，須嘗試錯誤
    - 解析度有限(截圖只有72dpi、列印另存pdf檔[^4]可達300dpi)，對高品質要求製圖(>1000dpi)無法配合
  - 使用[OSMOSIS](https://wiki.openstreetmap.org/wiki/Osmosis)
    - 可以就經緯度範圍(box or polygon)進行切割、數個檔案可以再進行整併(merge)
    - 如要較高解析度之地圖，要先全部下載再行切割。
    - 除了命令列方式之外，也有GUI版本[OSMembrane](https://github.com/openstreetmap/OSMembrane)
    - 如果是較大範圍的地圖，整併時會發生問題，需要較專業的merge方式，
    - 在小範圍、接近垂直座標系統的情況下，直接[montage](https://ostechnix.com/how-to-create-a-montage-from-images-in-linux/)拼接較快速方便，也不會有顏色失真的問題(詳[merged_GeoTIFF][5])。
  - 用使[Pbftoosm](https://wiki.openstreetmap.org/wiki/Pbftoosm)或 [osmconvert](https://wiki.openstreetmap.org/wiki/Osmconvert) (都沒有macOS版本)
  - 直接動態下載：(詳[merged_GeoTIFF][5])
    - 與Leaflet或其他網頁存取方式相同
    - 隨時更新圖資內容，與時俱進
    - 下載後另存快取，提升後續存取速度
- SURFER：
  - 好處：
    - 互動式作業方式、也有模版可以使用、容易上手、品質符合水準
    - 也能貼上png或其他格式之地圖
  - 沒有linux/macOS版本
  - [自動化](https://support.goldensoftware.com/hc/en-us/sections/204130857-Surfer-Automation)方面雖有VBA程式、然目前仍無法與其他unix系統相容
  - 底圖的[georeferencing](https://www.goldensoftware.com/blog/georeference-an-image-surfer)須自行(另行)輸入4個頂點的座標
  - 因為不是程式化、自動化的作業方式，修改範圍、解析度時，將難以因應
- NCL
  - 高品質、可貼在地形圖(另一等值圖)上、作業可程式化、自動化
  - 有網友提到[NCL貼中文字][6]的作法。但也有網友提問[無法正確顯示][7]的問題，即使能順利顯示還是得一個個貼。
  - 最大缺點就是不能貼raster底圖，對於目前已有的google map、OSM、OTM資源而言，為非常可惜之限制。
- [dat2kml.py](../../GIS/wr_kml.md)
  - 具有regrid功能：不論非等間距網格、離散點、程式會依據數據範圍重新進行內插、並輸出等間距的網格結果(.grd)檔
  - 雖然在命令列、在CaaS方面，都能提供圖檔的計算，與OSM/OTM/google map搭配顯示(如[數位版](../../GIS/digitizer.md))，也有動態縮放平移的功能，在偵錯階段提供檢核的能力。
  - 然而無法提供報告品質之圖檔，解析度不足以列印。
  - 無法在等值線上標註數字

(二)解決方案的建構目標

- 正確、迅速取得指定範圍、指定解析度之OSM/OTM底圖
- 應用NCL製作報告品質之等值線圖
- 將此二者予以疊加、提供使用者下載

### CaaS提供內容與產出對照表

方案|提供內容|產出|說明
:-:|-|-|-
1|GRIDCART內容文字|切割整併OTM底圖|如果工作站已有將不會另外下載
2|煙流模式輸出之PLT檔|NCL等值線與(貼上)OTM底圖|png圖檔
3|任意.grd檔(ascii)|NCL等值線與(貼上)OTM底圖|png圖檔

### CGI畫面

- 包括1個文字輸入窗、1個檔案選擇器、以及1個執行鍵。
- 伺服器@iMacKuang[^5]

| ![NCLonOTM.png](https://drive.google.com/uc?id=1p4Zu6FEiv8bWUu5nE0LATSaE4PMw2VTe)|
|:--:|
| <b>[http://125.229.149.182/NCLonOTM.html](http://125.229.149.182/NCLonOTM.html)畫面</b>|

### 標籤主題關係圖

![NCLonOTM_star](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/NCLonOTM_star.png)

## 程式說明

### 外部程式

1. cut指令、[sed](../../OperationSystem/sed.md)指令
2. tiles_to_tiffFit.py[^1]
3. NCL貼在OTM底圖上 NCLonOTM.py[^2]
4. 煙流模式結果繪製等值線圖 PLT_cn.ncl[^3]

```python
ran=tf.NamedTemporaryFile().name.replace('/','').replace('tmp','')

WEB='/Library/WebServer/Documents/'
CGI='/Library/WebServer/CGI-Executables/isc/'
CUT=' |cut -c 1-44 >& tmp.PLT'	
FIT='/Users/Data/GIS/OSM_20210318/merged_GeoTIFF/tiles_to_tiffFit.py '
OVL='/Users/Data/GIS/OSM_20210318/merged_GeoTIFF/NCLonOTM.py'
NCL='source /opt/local/bin/conda_ini ncl_stable >/tmp/source.out;'+\
	'/opt/anaconda3/envs/ncl_stable/bin/ncl /Users/Data/GIS/OSM_20210318/merged_GeoTIFF/PLT_cn.ncl'
NULL=' >&/dev/null'
pth=WEB+'isc_results/cntr_'+ran+'/'
OUT=' >> '+pth+'isc.out'
SED='/usr/bin/sed "1,8d" '

os.system('mkdir -p '+pth)
```

### 解讀PLT之內容(PLT_parser)

```python
def PLT_parser(fname):
  with open(fname,'r') as f:
    l=[line.strip('\n') for line in f]
  if l[0][0]=='*':l=l[8:]
  X,Y=([float(l[i].split()[j]) for i in range(len(l))] for j in range(2))
  sX ,sY=list(set(X)),list(set(Y))
  sX.sort()
  sY.sort()
  nx,ny=len(sX),len(sY)
  dx,dy=[round(sX[i+1]-sX[i],3) for i in range(nx-1)],[round(sY[i+1]-sY[i],3) for i in range(ny-1)]
  if len(set(dx))!=1 or len(set(dy))!=1:
    fname=pth+fn
    print """not a regular RE GRIDCART system, sorry! your input is:
    <a data-auto-download href="%s">%s</a>
  	"""  % (fname.replace(WEB,'../../../'),fname.split('/')[-1])
    sys.exit('not a regular RE GRIDCART system')
  return ' %d %d %d %d %d %d ' % (int(min(X)),nx,int(dx[0]),int(min(Y)),ny,int(dy[0]))
```

### CGI 檔頭與輸入

```python
print 'Content-Type: text/html\n\n'
print open(CGI+'header.txt','r')

form = cgi.FieldStorage()
STR = str(form.getvalue("iscinp"))
os.system('echo "'+STR+'"'+OUT)
```

### 執行tiles_to_tiffFit.py

- 詳見[tiles_to_tiffFit.py程式說明](tiles_to_tiffFit.md)

```python
if len(STR)>=4: #in case of input a string
  cmd ='cd '+pth+';'	  
  cmd+= FIT+STR+OUT+';'	
  os.system('echo "'+cmd+'"'+OUT)
  r=os.system(cmd+OUT)
  if r!=0:sys.exit('error in ncl')
  fnames=['fitted.png']
else:	
  fileitem = form['filename']
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
    with open(pth+fn, 'r') as f:
      ll=[l.strip('\n') for l in f]
    if ll[0]=='DSAA':
      x, y, c, (ny, nx) = load_surfer(pth+fn)
      with open(pth+'tmp.PLT','w') as f:
        for j in range(ny):
          for i in range(nx):
            f.write('%f %f %f\n' % (x[j,i],y[j,i],c[j,i]))
    elif ll[0].split()[1] in ['AERMOD','ISCST3']:
      cmd ='cd '+pth+';'	  
      if pth+fn!=pth+'userinp.PLT': cmd+='cp '+pth+fn+' '+pth+'userinp.PLT;'
      cmd+= SED+'userinp.PLT'+CUT+';'
      os.system('echo "'+cmd+'"'+OUT)
      r=os.system(cmd+OUT)
    else:
      print 'wrong format! '+ll[0]
      sys.exit('wrong format')
    cmd ='cd '+pth+';'	  
    cmd+= FIT+' tmp.PLT '+OUT+';'	
    os.system('echo "'+cmd+'"'+OUT)
    r=os.system(cmd+OUT)
```

### 執行副程式PLT_parser

- 產生param.txt與title.txt，用以執行[PLT_cn.ncl](../NCL/PLT_cn.md)

```python
    STR=PLT_parser(pth+'tmp.PLT')	
    cmd ='cd '+pth+';'	  
    cmd+='echo "'+STR+'">param.txt;'
    cmd+='echo "'+fn+'">title.txt;'
    cmd+= NCL+OUT+';'
    cmd+= OVL
    os.system('echo "'+cmd+'"'+OUT)
    r=os.system(cmd+OUT)
    if r!=0:sys.exit('error in ncl')
    fnames=['fitted.png', 'tmp_cn.png', "NCLonOTM.png"]
    descip={ 'fitted.png':'OpenTopoMap: ',
	'tmp_cn.png':'CLN_contour: ',
	'NCLonOTM.png':'contour post on OTM: '}
```

### 輸出成果檔案

```python
for fn in fnames:
  fname=pth+fn
  print """\
  %s<a data-auto-download href="%s">%s</a></br>
  """  % (descip[fn],fname.replace(WEB,'../../../'),fname.split('/')[-1])
print """\
  </body>
  </html>
  """
```

## 範例

![fitted.png](https://drive.google.com/uc?id=1QjRN3gTShz3jDu8hGgRhAlhAtqAOIpYF)|![tmp_cn.png](https://drive.google.com/uc?id=1DK7QFdVjCEk-MRA9K8klC-IsnUhyqa5W)
:-:|:-:
模擬範圍地形圖整併結果|模擬結果等值線圖

### 疊圖結果

- NCLonOTM.png 

![NCLonOTM_ok.png ](https://drive.google.com/uc?id=1A9KI_MtGwRBDJDFcPCBUqnRIfAMVdtzh)

[^1]: 集合OTM圖磚並修剪成tiff檔之py程式，詳見[tiles_to_tiffFit.py程式說明](tiles_to_tiffFit.md)，或下載[tiles_to_tiffFit.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/tiles_to_tiffFit.py)
[^2]: NCL貼在OTM底圖上之轉接程式，詳見[NCLonOTM程式說明](../NCL/NCLonOTM.md)，或下載[NCLonOTM.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/NCLonOTM.py)
[^3]: 煙流模式結果繪製等值線圖之NCL程式，詳見[程式說明](../NCL/PLT_cn.md)，或下載[PLT_cn.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/PLT_cn.ncl)
[^4]: 擷取 Google/OSM 地圖的方法, 小宜(2018-09-14), [易普印 e知識百科][4]
[^5]: 125.229.149.182為Hinet給定，如遇機房更新或系統因素，將不會保留。敬請逕洽作者：sinotec2@gmail.com.

[4]: https://blog.eprint.com.tw/export-openstreetmap-as-files/ "擷取 Google/OSM 地圖的方法, 小宜(2018-09-14), 易普印 e知識百科"
[5]: https://jimmyutterstrom.com/blog/2019/06/05/map-tiles-to-geotiff/ "Generate merged GeoTIFF imagery from web maps (xyz tile servers) with Python, Jimmy Utterström(2019)"
[6]: https://www.796t.com/content/1546220715.html "NCL新增中文字元,阿新(2018-12-31)"
[7]: https://github.com/NCAR/pyngl/issues/4 "Will PyNGL and/or PyNIO support unicode (UTF-8) in some day?"