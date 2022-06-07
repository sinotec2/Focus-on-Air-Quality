---
layout: default
title: AERMOD
parent: CGI-pythons
grand_parent: Utilities
last_modified_date: 2022-06-07 20:21:17
---
# AERMOD/ISCST3遠端模擬控制程式設計
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
- 作業目標：給定AERMOD/ISC runstream檔、氣象及地形檔案，啟動遠端執行程式，並提供結果檔案之連結。
- 考量及優勢
  1. 避免本地執行檔之編譯、前後處理程式系統之建置
  1. 使用遠端計算資源
  1. 快速上手、有助進行模式設定敏感性之測試
- 整體架構詳見[ISCST/AERMOD 主程式](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/RemoteSystem/main/)之說明，此處著眼於CGI程式的說明。
- 程式碼：[AERMOD.py](https://github.com/sinotec2/CGI_Pythons/blob/main/isc/AERMOD.py)

## 執行前的檢核
### 執行緒之讀取
- 應用subprocess模組進行讀取。bash指令運用了ps、grep、以及wc
- 因工作站有可能同時運作了iscst及aermod程式，因此分別讀取緒數予以相加。
- 工作站為 6 核心，限制總緒數在5以下以提高服務效能(see [TODO's]())
- 必須在程式已開始就先確認執行緒數，儘快提供使用者正確的資訊，以避免錯誤期待。

```python
npid1=subprocess.check_output('ps -ef|grep aermod|grep -v grep|wc -l',shell=True).decode('utf8').strip('\n')
npid2=subprocess.check_output('ps -ef|grep iscst3|grep -v grep|wc -l',shell=True).decode('utf8').strip('\n')
npid=int(npid1)+int(npid2)
if npid>=5:
  print 'total '+str(npid)+' iscst or aermod processes are running, please wait. </br>'
  print '</body></html>'
  sys.exit()
```

### 檔案數的檢核
- html提供的檔案欄位數共有4個，最少需2個檔案（ISCST3的runstream與氣象檔案）
- 將檔名記住備用(`inames`)
```python
RUNMDL=ISCST3
if model=='AERMOD': RUNMDL=AERMOD
inames=[]
for nf in '1234':
  fileitem = form['filename'+nf]
  if fileitem.filename:
    fn = os.path.basename(fileitem.filename)
    open(pth+fn, 'wb').write(fileitem.file.read())
    inames.append(pth+fn)
  else:
    if nf=='4':continue
    if model=='ISCST' and nf=='3':continue
    print 'Absent of file number: '+nf+'</body></html>'
    sys.exit('err input file')
```
### 檔案名稱之讀取
- 從runstream需讀到錯誤訊息檔(`ename`)、繪圖檔(`pname`)、摘要檔(`sname`)的名稱
- 另外產生std output(`oname`)以及kml、grd檔(`kname`)

```python
ename=subprocess.check_output('grep ERRORFIL '+inames[0],shell=True).decode('utf8').strip('\n').split()[1]
pname=subprocess.check_output('grep PLOTFILE '+inames[0]+'|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').split()
sname=subprocess.check_output('grep SUMMFILE '+inames[0]+'|awk "{print \$NF}"',shell=True).decode('utf8').strip('\n').split()
ext=inames[0].split('.')[-1]
iname=inames[0].split('/')[-1]
oname=iname.replace(ext,'out')
kname=[p+'.kml'for p in pname[:]]+[p+'.grd'for p in pname[:]]
```

## 程式之執行
- 複製一份[會自動更新的html]()檔到工作目錄