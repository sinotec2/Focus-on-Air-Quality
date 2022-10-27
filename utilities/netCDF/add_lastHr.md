---
layout: default
title: add_lastHr
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-10-13 17:46:44
---

# 延長nc檔案之最末小時
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
- 模式時間內插時會需要模擬範圍之後的1小時值，對於批次作業而言，這項需要還蠻尷尬的，因為這1個小時需要多模擬1天。
- 最簡便的作法，是將nc檔案最末小時予以複製到最後，將檔案延長1個小時。
- 因CMAQ對TFLAG的檢查非常嚴格，需將標籤都填寫正確才行，因此簡單的ncks再ncrcat作法，無法滿足，還是要寫程式處理才行。
- 此處以dtconvert作為時間計算的工具。
- BCON的資料在3維變數中，要特別處理。

## 程式碼

```python
$ cat ~/bin/add_lastHr.py
#!/opt/anaconda3/bin/python
import netCDF4
import os, sys
import datetime


def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime.datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

def jul2dt(jultm):
  jul,tm=jultm[:]
  yr=int(jul/1000)
  ih=int(tm/10000.)
  return datetime.datetime(yr,1,1)+datetime.timedelta(days=int(jul-yr*1000-1))+datetime.timedelta(hours=ih)

fname=sys.argv[1]
nc = netCDF4.Dataset(fname,'r+')
v='TFLAG'
nt,nvars,ndt=(nc.variables[v].shape[i] for i in range(3))
dend=jul2dt(list(nc.variables[v][nt-1,0,:]))
SDATE=dt2jul(dend+datetime.timedelta(days=1./24.))
for i in range(2):
  nc.variables[v][nt,:,i]=[SDATE[i] for j in range(nvars)]

V=[list(filter(lambda x:nc.variables[x].ndim==j, [i for i in nc.variables])) for j in [1,2,3,4]]
if 'BCON' in fname:
  for x in V[2]:
    if x==v:continue
    nc.variables[x][nt,:,:]=nc.variables[x][nt-24,:,:]
else:
  for x in V[3]:
    nc.variables[x][nt,:,:,:]=nc.variables[x][nt-24,:,:,:]
nc.close()
```
