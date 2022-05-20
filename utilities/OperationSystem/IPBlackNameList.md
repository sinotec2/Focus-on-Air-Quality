---
layout: default
title: 自動添加並啟用IP黑名單
parent:   Operation System
grand_parent: Utilities
last_modified_date: 2022-04-28 10:09:48
---

# 自動添加並啟用IP黑名單
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC 
{:toc}

---

## 背景
- 開設了httpd之後，即使是最沒有什麼可以駭的html形式，仍然吸引不少駭客前來挑戰，從硬碟下載不少空品模式方面的數據檔。不知道駭客們下載數百G數據回去後，會不會罵我放這麼多東西來浪費他們的時間、空間。
- 其實我也蠻心疼他們的時間的，因為家裏的網路是非對稱，上載的速度是非常慢的，而且也讓Mac電腦沒事在空轉。最重要的會癱瘓網路的其他功能，讓我沒有興趣繼續發展遠端模擬系統。
- 2022-04-23打算不再糾結了，爬了一些網友的建議，決定還是自己來寫一個[自動添加並啟用IP黑名單]()的作業系統。
- 基本上，Mac不像Linux有[iptable](https://zh.wikipedia.org/wiki/Iptables)這麼靈活的防火牆程式
  - ***系統偏好設定*** 中的防火牆沒法在日常的實務中幫上什麼忙，還是需要自己分析、自己添加黑名單、讓root來定期檢討啟用，才能即時阻擋駭客的騷擾。
  - 即使是商業軟體(如[spamhaus](www.spamhaus.org))提供的[黑名單](https://www.spamhaus.org/drop/drop.lasso)，更新頻率也是一天一次，似乎也無法幫上忙。
  - [網友](http://yenpai.idis.com.tw/archives/399-教學-自動透過-iptables-封鎖-ip-黑名單)建議：
    - `依據官方解釋，這些 IP 網段主要是被用來當做發送垃圾封包使用，因此，這並不能有效的阻擋真實 IP 的攻擊。若要對真實 IP 來查驗，那可能只能多透過腳本寫出針對本機連線的次數、特性等分析加阻擋。但無論如何，我們還是把它列入阻擋清單當中吧。`

### 存取記錄
- Mac將httpd的存取記錄寫在httpd/access_log裏，內容如下：
  - IP、[存取時間（LST）]、動作、以及指向檔案

```bash
#kuang@114-32-164-198 ~/bin/BlockIP
#$ tacc
tail /usr/local/var/log/httpd/access_log
157.55.39.99 - - [23/Apr/2022:19:34:02 +0800] "GET /README.md HTTP/1.1" 200 824
66.249.66.159 - - [23/Apr/2022:19:37:19 +0800] "GET /NCLonOTM2.html HTTP/1.1" 200 4265
157.55.39.159 - - [23/Apr/2022:19:39:37 +0800] "GET /LeafletDigitizer/ HTTP/1.1" 200 2303
157.55.39.159 - - [23/Apr/2022:19:40:38 +0800] "GET /wms1/ HTTP/1.1" 200 335
157.55.39.159 - - [23/Apr/2022:19:46:39 +0800] "GET /Shared/ HTTP/1.1" 200 598
37.0.8.132 - - [23/Apr/2022:20:00:55 +0800] "GET / HTTP/1.1" 200 7187
40.77.167.6 - - [23/Apr/2022:20:08:25 +0800] "GET /runtime.js HTTP/1.1" 200 37905
207.46.13.132 - - [23/Apr/2022:20:10:36 +0800] "GET /jquery_chained/demo.html HTTP/1.1" 200 22437
45.155.204.146 - - [23/Apr/2022:20:17:35 +0800] "GET /?XDEBUG_SESSION_START=phpstorm HTTP/1.1" 200 7187
157.55.39.99 - - [23/Apr/2022:20:24:36 +0800] "GET /lc-gif-player/demo.html HTTP/1.1" 200 5531
```

- 有2個版本的httpd與log檔
  - /usr/local/var/log是搭配/usr/local/opt/httpd/bin/httpd（Apache2.4）
  - /var/log/apache2/access_log是搭配/usr/sbin/apachectl(自帶Apache)
  - MacOS更新後必須[重裝Apache2.4](https://getgrav.org/blog/macos-monterey-apache-multiple-php-versions)，不能使用自帶的apachectl。

```bash
#kuang@114-32-164-198 ~/bin/BlockIP
$ cat ~/bin/tacc
#/usr/local/opt/httpd/bin/httpd Version
f=/usr/local/var/log/httpd/access_log
#
# /usr/sbin/apachectl Version
#f=/var/log/apache2/access_log
echo tail $f
tail $f
```

### 存取分析程式
- 使用pandas的樞紐分析，可以看到駭客一天內就存取了900～15萬次，有的分成7天慢慢下載。所以等到一天結束再來阻擋、應該是不太來得及。
- 又分析小時的分布，大致上一個小時、一個ip要存取500次以上、而又不是駭客的機會不多。
- ip location infomation(lst)
  - ip地理位置基本是個猜測值、猜得準不準就是各家本事。[業者](https://ipinfo.io/)的詢問結果差強人意，但因為是免費，還蠻具競爭優勢的。
  - 所提供的付費服務方案是給一月之內詢問15萬次的用戶。這裏即使每小時詢問10次，一天240次，應該也不會造成業者的負擔（最後沒有使用在日常作業。因為不論是哪裡來的大量存取、不合理就必須阻擋）。
  - 在該網免費註冊會即可得到**TOKEN**，在每次詢問時必須提供。
  - 該業者也將[python程式庫](https://github.com/ipinfo/python)提供出來，會方便很多。但是Mac裝置不成功，只好保留以curl程式下載文字、再詳細分析IP位置的內容（dip, dictionary of ip）。
- 程式除了讀取完整的存取log檔，也分析當時的登入地點，這樣可以即時了解網站是否被駭。

```python
from pandas import *
import subprocess
from datetime import datetime,timedelta
import sys, os
import numpy as np

def wrt_csv(lines,fname):
  ip=[i.split()[0] for i in lines]
  tflag=[i.split()[3].replace('[','') for i in lines]
  dates=[i.split(':')[0] for i in tflag]
  df=DataFrame({'ip':ip,'time':tflag,'date':dates})
  pv=pivot_table(df,index=['ip','date'],values='time',aggfunc='count').reset_index()
  pvc=pivot_table(pv,index='ip',values='date',aggfunc='count').reset_index()
  pvs=pivot_table(pv,index='ip',values='time',aggfunc='sum').reset_index()
  pvsc=merge(pvc,pvs,on='ip')
  pvsc=pvsc.sort_values('time',ascending=False).reset_index(drop=True)
  pvsc['city']=[0 for i in range(len(pvsc))]
  for i in range(min(10,len(pvsc))):
    ii=pvsc.ip[i]
    lst=subprocess.check_output('curl -s ipinfo.io/'+ii+'\?token=TOKEN',shell=True).decode('utf8').split('\n')
    itm=[j.split('"')[1] for j in lst if len(j)>1]
    val=[j.split('"')[3] for j in lst if len(j)>1]
    dip={it:va for it,va in zip(itm,val)}
    pvsc.loc[i,'city']=dip['city']
  pvsc.set_index('ip').to_csv(fname)
  return 0
with open('/usr/local/var/log/httpd/access_log','r') as f:
  lines=[i for i in f]
fname='~/bin/BlockIP/IP_count.csv'
r=wrt_csv(lines,fname)

TF=(datetime.now()+timedelta(hours=0)).strftime("%d/%b/%Y:%H")
accfname='/usr/local/var/log/httpd/access_log'
lines=subprocess.check_output('/usr/bin/grep --color=never  "'+TF+'" '+accfname,shell=True).decode('utf8').split('\n')
lines=[i for i in lines if len(i)>1]
fname='~/bin/BlockIP/IP_count'+TF.replace('/','_')+'.csv'
r=wrt_csv(lines,fname)
```
- head of IP_count.csv，可以看到iMac是如何被駭客蹂躪

|ip|date|count|location|
|:-:|:-:|:-:|-|
|179.61.240.77|1|153082|Newmarket|
|34.140.248.32|7|150463|Brussels|
|130.211.54.158|6|106475|Brussels|
|35.233.62.116|5|73948|Brussels|
|114.32.164.198|28|2136|Taipei（Home）|
|59.124.9.103|3|1880|Taipei|
|118.163.33.43|22|1520|Taipei|
|45.136.4.119|1|990|Istanbul|
|114.84.195.13|1|989|Shanghai|

## 防止駭客侵擾的策略方法
- 其實知道網站被駭客盯上，關閉就可以了。這是過去iMac只在上班時間開放的理由。但還是有困難：
  - 非上班時間，還是有正常使用的需求。這要怪華人焚膏繼晷的民族精神。
  - 上班時間駭客從正常使用的通訊過程得知iMac的存在，也大方的造訪。不僅沒有防護、而且嚴重降低網路的速度
  - 上班時間無預警關閉網站，對客戶實在是不好的網站經驗
  - 畢竟關閉網站還是必須手動操作，總不能讓電腦自己開關，這網管也太不負責了。
- IP黑名單方案
  - UCAR的[資料庫網站](https://rda.ucar.edu/)，曾經就是以這個方式管理(這是個人親身實證經歷)，經多方閃躲，最後UCAR網管還是選擇以username黑名單而不用IP，而Mac後來也改以[每天少量下載](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/NCEP/)，而不是久久一次大批次下載的策略。因為擋IP真的很嚴酷。
  - 網友提供了Mac上的寶貴經驗([Block Access to Particular IP Address on Mac](https://medium.com/ringcentral-developers/how-to-block-a-particular-ip-address-on-mac-a587805972e5))
  - 只要能夠確認IP存取過程確實是駭客的無聊行為，即使黑名單策略較為嚴苛應該也不為過。

### 封包過濾 PFctl程式
- Mac自帶封包過濾的控制程式PFctl,可以做為動態[阻擋IP黑名單](https://medium.com/ringcentral-developers/how-to-block-a-particular-ip-address-on-mac-a587805972e5)的主程式。
- pfctl是透過/etc/pf.conf檔案來指定黑名單IP。
- 其設定方式為：`block drop from any to 192.168.1.1`
- 啟動方式：`pfctl -e -f /etc/pf.conf`
- 因為是命令列就可以完成的工作，適合用來定期執行。

## 作業系統
### 每小時分析程式
- 使用grep指令，篩出過去一個小時的存取記錄。grep內設有顏色，會出現亂碼，需要關閉。
- 以[osascript](https://support.apple.com/zh-tw/guide/terminal/trml1003/mac)出現在consol的對話框來提醒注意
- 將每個存取超過500次的IP列到pf.conf檔案裏
- 最後啟動（更新）pfctl

```python
#kuang@114-32-164-198 ~/bin/BlockIP
#$ cat ana_accHr.py
#!/opt/anaconda3/bin/python
from datetime import datetime,timedelta 
import subprocess
from pandas import *
import sys, os
import numpy as np

TF=(datetime.now()+timedelta(hours=-1)).strftime("%d/%b/%Y:%H")
accfname='/usr/local/var/log/httpd/access_log'
lines=subprocess.check_output('/usr/bin/grep --color=never  "'+TF+'" '+accfname,shell=True).decode('utf8').split('\n')
if len(lines)<=500:sys.exit('acc less than 500 times')
lip=[i.split()[0] for i in lines if len(i)>0]
sip=list(set(lip))
nip=np.array([lip.count(i) for i in sip])
mip=np.max(nip)
if mip>500:
  msg='tell app "System Events" to display dialog "Hourly acc >500 !!,tail /etc/pf.conf"'
  os.system("/usr/bin/osascript -e '"+msg+"'&")
  df=DataFrame({'ip':sip,'nm':nip})
  dfm=df.loc[df.nm>500]
  for i in dfm.ip:
    os.system('echo "block drop from any to '+i+'">>/etc/pf.conf')   
  os.system('pfctl -e -f /etc/pf.conf')
```

### crontab設定
- 設定逐時檢討。
- 因為必須改變PF狀態，需要以root權限執行crontab

```bash
#check the acc # >500/hr and block them
0 *  *  *  * /Users/kuang/bin/BlockIP/ana_accHr.py 
```

## Result
- 希望最好不要看到對話框出現
- 4/27清晨真的啟動了機制，一個小時就存取了近2000次，這應該沒有錯怪它了。
- 其餘的好兄弟試了1\~2次就會放棄

|ip|date|count|location|
|:-:|:-:|:-:|-|
|35.233.62.116|1|1890|Brussels|
|66.249.68.57|1|2|Salem|
|103.59.156.16|1|1|Haegok|
|14.225.253.120|1|1|Hạ Long|

## 修正作法：外部黑名單
### 精進的必要與步驟
- 因$web之權限開放，前述pf rule 也不正確，致駭客還是來訪。作法需精進。
  - 先關閉$web之讀取、執行權限。此舉阻擋大多數的惡意瀏覽。
  - 新增pf.conf的規則
    - 使用table指令讀入外部黑名單
    - 指定需要關閉的網路卡：  `ppp0` (外部IP)
  - 確認pfctl真的能擋住黑名單
    - 使用手機瀏覽imac ppp0網址，由tacc找到手機IP、加入黑名單、
    - 重新啟動pfctl，再次測試手機是否能正常瀏覽，如果不能，才是對的。
  - 修改ana_accHr.py，將惡意IP加入外部黑名單檔案(bname)。

### 新增pf.conf規則

```bash
#kuang@114-32-164-198 ~/bin/BlockIP
$ tail /etc/pf.conf
#
# com.apple anchor point
#
scrub-anchor "com.apple/*"
nat-anchor "com.apple/*"
rdr-anchor "com.apple/*"
dummynet-anchor "com.apple/*"
anchor "com.apple/*"
load anchor "com.apple" from "/etc/pf.anchors/com.apple"

ext_if="{ ppp0 }"

table <badips> persist file "/Users/kuang/bin/BlockIP/pf.blocked.ip.conf"
block on $ext_if from { <badips> } to any
```

### 外部黑名單
- 黑名單之外部檔案：/Users/kuang/bin/BlockIP/pf.blocked.ip.conf
  - 參考[ken](https://bbken.org/author/ken/page/3/?PageSpeed=noscript)的建議名單，大多是中國大陸的平台網站。

### 修改python程式
  - 將前述ana_accHr.py 修正成下述：

```python
kuang@114-32-164-198 ~/bin/BlockIP
$ tail ana_accHr.py
  bname='/Users/kuang/bin/BlockIP/pf.blocked.ip.conf'
  msg='tell app "System Events" to display dialog "Hourly acc >500 !!,tail /etc/pf.conf"'
  os.system("/usr/bin/osascript -e '"+msg+"'&")
  df=DataFrame({'ip':sip,'nm':nip})
  dfm=df.loc[df.nm>500]
  for i in dfm.ip:
    nline=subprocess.check_output('grep '+i+' '+bname+'|wc -l',shell=True).decode('utf8').strip('\t').split()[0]
    if nline>0:continue
    os.system('echo '+i+'>>'+bname)
    
  os.system('/sbin/pfctl -ef /etc/pf.conf')
```

## Reference
- 阿百, [自動透過 iptables 封鎖 IP 黑名單](http://yenpai.idis.com.tw/archives/399-教學-自動透過-iptables-封鎖-ip-黑名單), 2012 年 11 月 12 日
- Vyshakh Babji, [Block Access to Particular IP Address on Mac](https://medium.com/ringcentral-developers/how-to-block-a-particular-ip-address-on-mac-a587805972e5), Jul 3, 2019
- pfctl: Packet Filter Control
  - Ares163, [mac下的iptables---pfctl](https://www.jianshu.com/p/eefe3877650f), 2018.09.28
  - 喜欢踢足球的老罗, [macOS的pfctl使用](https://blog.csdn.net/SCHOLAR_II/article/details/111213190) , 2020-12-15.
  - Johnny 鋼鍊, [Mac OSX 內建防火牆 PF 使用筆記](https://j796160836.pixnet.net/blog/post/45551232--[教學]-mac-osx-內建防火牆-pf-使用筆記), Dec 20 Wed 2017.
  - Ken, [Blocking bad bots with PF](https://bbken.org/author/ken/page/3/?PageSpeed=noscript), 4 月 4 日， 2020 年
- ipinfo, [IPinfo Python Client Library](https://github.com/ipinfo/python),22 Nov 2021
- suupport.apple.com, [在 Mac 上使用 AppleScript 和「終端機」來自動執行任務](https://support.apple.com/zh-tw/guide/terminal/trml1003/mac), 2022