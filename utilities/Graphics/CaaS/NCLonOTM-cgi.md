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

方案|提供內容|產出|說明
:-:|-|-|-
1|GRIDCART內容文字|切割整併OTM底圖|如果工作站已有將不會另外下載
2|煙流模式輸出之PLT檔|NCL等值線與(貼上)OTM底圖|png圖檔
3|任意.grd檔(ascii)|NCL等值線與(貼上)OTM底圖|png圖檔

### CGI畫面

- 包括1個文字輸入窗、1個檔案選擇器、以及1個執行鍵。

| ![NCLonOTM-cgi.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/NCLonOTM-cgi.png)|
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

- 產生param.txt與title.txt，用以執行[PLT_cn.ncl](../NCL/NCLonOTM.md)

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

[^1]: 集合OTM圖磚並修剪成tiff檔之py程式，詳見[tiles_to_tiffFit.py程式說明](tiles_to_tiffFit.md)，或下載[tiles_to_tiffFit.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/tiles_to_tiffFit.py)
[^2]: NCL貼在OTM底圖上之轉接程式，詳見[NCLonOTM程式說明](../NCL/NCLonOTM.md)，或下載[NCLonOTM.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/NCL/NCLonOTM.py)
[^3]: 煙流模式結果繪製等值線圖之NCL程式，詳見[程式說明](../NCL/PLT_cn.md)，或下載[PLT_cn.ncl](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/utilities/Graphics/CaaS/PLT_cn.ncl)