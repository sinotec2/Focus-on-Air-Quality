---
layout: default
title: "FNL檔案之免密下載"
parent: "NCEP"
grand_parent: "wind models"
nav_order: 1
date:               
last_modified_date:   2021-11-26 19:47:53
tags: Crawlers WPS
---

# FNL檔案之免密下載

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

## 密碼管理政策

- NCAR DRS更新了他們的帳密管理政策，再也不設限了。大量的下載移到ORCID，網頁介面的少量下載，可以使用python或csh腳本直接下載。
  
## 腳本說明

### python script

- 少了驗證帳密的動作
- 目錄設定的原則並沒有改變
- `http`改成了`https`。提升了安全性。

```python
#kuang@MiniWei /Users/WRF4.1/NCEP/SRF_ds461.0/2024
#$ cat rda-download.py 
#!/usr/bin/env python
""" 
Python script to download selected files from rda.ucar.edu.
After you save the file, don't forget to make it executable
i.e. - "chmod 755 <name_of_script>"
"""
import sys, os
from urllib.request import build_opener

opener = build_opener()

filelist = [
  'https://data.rda.ucar.edu/ds461.0/little_r/2024/SURFACE_OBS:2024022700',
...
  'https://data.rda.ucar.edu/ds461.0/little_r/2024/SURFACE_OBS:2024030118'
]

for file in filelist:
    ofile = os.path.basename(file)
    sys.stdout.write("downloading " + ofile + " ... ")
    sys.stdout.flush()
    infile = opener.open(file)
    outfile = open(ofile, "wb")
    outfile.write(infile.read())
    outfile.close()
    sys.stdout.write("done\n")
```
### csh script


```csh
#!/usr/bin/env csh
#
# c-shell script to download selected files from rda.ucar.edu using Wget
# NOTE: if you want to run under a different shell, make sure you change
#       the 'set' commands according to your shell's syntax
# after you save the file, don't forget to make it executable
#   i.e. - "chmod 755 <name_of_script>"
#
# Experienced Wget Users: add additional command-line flags to 'opts' here
#   Use the -r (--recursive) option with care
#   Do NOT use the -b (--background) option - simultaneous file downloads
#       can cause your data access to be blocked
set opts = "-N"
#
# Check wget version.  Set the --no-check-certificate option 
# if wget version is 1.10 or higher
set v = `wget -V |grep 'GNU Wget ' | cut -d ' ' -f 3`
set a = `echo $v | cut -d '.' -f 1`
set b = `echo $v | cut -d '.' -f 2`
if(100 * $a + $b > 109) then
  set cert_opt = "--no-check-certificate"
else
  set cert_opt = ""
endif

set filelist= ( \
  https://data.rda.ucar.edu/ds083.2/grib2/2024/2024.02/fnl_20240227_00_00.grib2  \
...
  https://data.rda.ucar.edu/ds083.2/grib2/2024/2024.03/fnl_20240301_18_00.grib2  \)
while($#filelist > 0)
  set syscmd = "wget $cert_opt $opts $filelist[1]"
  echo "$syscmd ..."
  $syscmd
  shift filelist
end

```
