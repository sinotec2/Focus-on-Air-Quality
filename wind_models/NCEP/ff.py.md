---
layout: default
title: "FNL檔案之自動化下載"
parent: "NCEP"
grand_parent: "wind models"
nav_order: 1
date:               
last_modified_date:   2021-11-26 19:47:53
---

# FNL檔案之自動化下載

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
- FNL的全名是(**F**i**N**a**L**) Operational Global Analysis data，是全球數據同化系統（GDAS）的作業結果，空間解析度0.25(083.3)～1度(083.2)、時間間距是6小時。
- FNL在40項WPS可接受的再分析檔案中，屬於穩定性高、解析度較高的選擇。
- 不過FNL沒有提供自動切割的界面，如果要下載全球0.25度的數據，檔案會非常大，要注意頻寬與磁碟空間。

## 批次執行與自動執行
詳見[樓上](/Focus-on-Air-Quality/wind_models/NCEP/)。

## 程式分段說明
- 使用py27、有較高的穩定性、避免更新可能造成的錯誤。
- 引進模組，使用urllib2、cookielib來下載，不從檔案匯入，直接讀取遠端cookie，詳見[Python 中讓 urllib 使用 cookie 的方法](https://blog.m157q.tw/posts/2018/01/06/use-cookie-with-urllib-in-python/)。

```python
kuang@114-32-164-198 ~/python_eg/NCEP_fetch
$ cat -n ff.py 
     1	#!/opt/anaconda3/envs/py27/bin/python
     2	#
     3	# python script to download selected files from rda.ucar.edu
     4	# after you save the file, don't forget to make it executable
     5	#   i.e. - "chmod 755 <name_of_script>"
     6	#
     7	import sys
     8	import os
     9	import urllib2
    10	import cookielib
    11	import datetime
    12	import subprocess
    13	
```

- datetime轉str之副程式

```python
    14	def dt2str(dt):
    15	    a=[int(i) for i in str(dt).split()[0].split('-')]
    16	    return str(a[0]*100*100+a[1]*100+a[2])
```

- 在command line 操作時相關指令(無用)

```python
    17	#
    18	#if (len(sys.argv) == 0):
    19	#  print "usage: "+sys.argv[0]+" [-q] password_on_RDA_webserver"
    20	#  print "-q suppresses the progress message for each file that is downloaded"
    21	#  sys.exit(1)
    22	#
    23	passwd_idx=1
    24	verbose=True
    25	if (len(sys.argv) == 3 and sys.argv[1] == "-q"):
    26	  passwd_idx=2
    27	  verbose=False
    28	#
```

- cookie的管理
  - 這段程式碼是NCEP網站自動產生的
  - 同一批次登入時網站會先產生一登入驗證檔案，因此如有舊檔會需要先去除。
  - 需先在網站登錄email及密碼，將帳密寫在****處，如此才能登入網站。

```python
    29	cj=cookielib.MozillaCookieJar()
    30	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    31	#
    32	# check for existing cookies file and authenticate if necessary
    33	do_authentication=False
    34	if (os.path.isfile("auth.rda.ucar.edu")):
    35	  cj.load("auth.rda.ucar.edu",False,True)
    36	  for cookie in cj:
    37	    if (cookie.name == "sess" and cookie.is_expired()):
    38	      do_authentication=True
    39	else:
    40	  do_authentication=True
    41	if (do_authentication):
    42	#  passwd=sys.argv[1]
    43	  passwd='******'
    44	  login=opener.open("https://rda.ucar.edu/cgi-bin/login","email=*****@***&password="+passwd+"&action=login")
    45	#
    46	# save the authentication cookies for future downloads
    47	# NOTE! - cookies are saved for future sessions because overly-frequent authentication to our server can cause your data access to be blocked
    48	  cj.clear_session_cookies()
    49	  cj.save("auth.rda.ucar.edu",True,True)
    50	#
```

- 由檔案系統目錄讀取舊年代`yrold`、並讀取上次作業的最後日期`blk`

```python
    50	#
    51	# download the data file(s)
    52	#os.system('/Users/kuang/bin/ncep.cs')
    53	path='/Users/WRF4.1/NCEP/FNL/'
    54	yrold=os.popen('ls -d '+path+'20*|tail -n1').read().strip('\n').split('/')[-1]
    55	blk=os.popen('ls '+path+yrold+'|tail -n1').read().strip('\n').split('_')
```

- 計算下載起始日期`bdate`,由date指令取得今天日期。FNL更新到實際時間的**前2天**，即為結束日期。

```python
    56	try:
    57	  begd=int(blk[1])
    58	except:
    59	  begd=(int(yrold)-1)*10000+1231
    60	ldate = datetime.datetime(begd/100/100,begd/100%100,begd%100)
    61	bdate = ldate+datetime.timedelta(days=1)
    62	nowd = int(subprocess.check_output("date +%Y%m%d%H", shell=True)[:-3])
    63	tdate = datetime.datetime(nowd/100/100,nowd/100%100,nowd%100)
    64	edate = tdate+datetime.timedelta(days=-2)
```

- 由起訖日期計算總日數`leng`

```python
    65	E_B=str(edate-bdate)
    66	if 'day' not in E_B:
    67	  leng=1
    68	else:
    69	  leng=int(str(edate-bdate).split('day')[0])+1
    70	if leng<=0:sys.exit('no need to download, bdate='+str(bdate)+' edate='+str(edate))
```

- 產生需要下載的日期、年代(有可能要建新目錄)、月份

```python
    71	ymds=[dt2str(bdate+datetime.timedelta(days=i)) for i in xrange(leng)]
    72	yrs=[ymd[:4] for ymd in ymds]
    73	#add new year directory if necessary
    74	for yr in yrs:
    75	  os.system('mkdir -p '+path+'/'+yr)
    76	mos=[ymd[4:6] for ymd in ymds]
```

- 拆解檔案url、形成逐日、逐6小時之url序列`listoffiles`

```python
    77	head=['grib2/'+yr+'/'+yr+'.' for yr in yrs]
    78	med='/fnl_'
    79	udl='_'
    80	tail='_00.grib2'
    81	listoffiles=[head[i]+mos[i]+med+ymds[i]+udl+str(h)+tail for i in xrange(len(ymds)) for h in ['00','06','12','18']]
    82	#sys.exit('OK')
```

- 逐一下載檔案
  - 這段程式碼主要是NCEP網站自動產生的
  - 因部分作業系統對檔名中的冒號`:`會出現亂碼，如果是，需將其改成底線`_`。
  - 不適用fnl檔名命名規則

```python
    83	for file in listoffiles:
    84	  idx=file.rfind("/")
    85	  if (idx > 0):
    86	    ofile=file[idx+1:].replace(':','_')
    87	  else:
    88	    ofile=file.replace(':','_')
    89	  yr=file.split('/')[1]
    90	  path1=path+yr+'/'
    91	  if os.path.isfile(path1+ofile):continue
    92	  if (verbose):
    93	    sys.stdout.write("downloading "+ofile+"...")
    94	    sys.stdout.flush()
    95	  try:
    96	    infile=opener.open("http://rda.ucar.edu/data/ds083.2/"+file)
    97	  except:
    98	    continue
    99	  outfile=open(ofile,"wb")
   100	  outfile.write(infile.read())
   101	  outfile.close()
```

## 完整程式碼
- [ff.py](https://raw.githubusercontent.com/sinotec2/python_eg/master/NCEP_fetch/ff.py)



