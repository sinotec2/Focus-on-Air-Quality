---
layout: default
title: 鄉鎮區平均值計算
parent: Taiwan AQ Analysis
grand_parent: AQ Data Analysis
last_modified_date: 2022-02-08 13:46:05
tags: python
---

# 環保署測站數據鄉鎮區平均值之計算
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

- 測站及鄉鎮區都是空間上的維度，但因為同一個鄉鎮區有可能有2個以上的測站，需要平均。還有更多的鄉鎮區並沒有測站，這需要內、外插。
- 平均方式：此處使用內積`np.dot`方式，以加快計算速度。
- 內、外插方式有很多，此處以鄰近測站之值做為沒有測站鄉鎮區之值，依據[town_aqstEnew.csv][town_aqstEnew.csv]之關聯。
- 時間上，本程式讀取全年日均值處理結果，詳[說明](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/TWNAQ/daymean/)。
- 處理結果的檢視：參[geoplot繪製行政區範圍等值圖](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/matplotlib/choropleth_geoplot/)

## 程式重點說明

### IO's

- 引數
  - 需要1個引數：年代(4碼)
- 鄉鎮區與測站編號的對照表[town_aqstEnew.csv][town_aqstEnew.csv]
- 輸出：YYYYres.csv

### 檔案讀取與測站之確認

- 因為跨了20年，測站及鄉鎮區的設定略有變更，須逐年測試、修正檢討。

```python
yr=sys.argv[1]

fname='/nas1/CAM-chem/Annuals/town_aqstEnew.csv'
twn=read_csv(fname)
twn=twn.loc[twn.aq_st.map(lambda x:'0;' not in x)].reset_index(drop=True)
twn['stns']=[Series([int(i) for i in j[:-1].split(';')]) for j in twn.aq_st]
all_stn=[]
for i in twn.stns:
  if len(i)==0:continue
  a=all_stn+list(i)
  all_stn=list(set(a))
all_stn=set(all_stn)

df=read_csv(yr+'.csv')
df.stn=[int(i) for i in df.stn]
col=df.columns[2:]
s=set(df.stn)

new=s-all_stn
old=all_stn-s
if len(old)>0:
    print(old)

if len(new)>0:
  df=df.loc[df.stn.map(lambda x:x not in new)].reset_index(drop=True)
```


### 測站缺值之填入

- 在排序、轉成矩陣之前，需對測站是否不存在造成缺值情況進行處理。
- 此處填入`np.nan`，在一併以`fillna`全部改成負值。

```python
nt,ns,ni=len(set(df.ymd)),len(set(df.stn)),len(col)

if len(df)!=nt*ns:
#sys.exit('time or station data missing!')
  pv=pivot_table(df,index='ymd',values='stn',aggfunc='count').reset_index()
  ymd_ng=list(pv.loc[pv.stn!=ns,'ymd'])
  for i in ymd_ng:
    ss=set(list(df.loc[df.ymd==i,'stn']))
    for j in s-ss:
      df1=DataFrame({'ymd':[i],'stn':[j]})
      for c in col:
        df1[c]=np.nan
      df=df.append(df1,ignore_index=True)
```

### 輸入csv檔轉成矩陣

- 負值必須將其遮蔽

```python
df=df.sort_values(['ymd','stn']).reset_index(drop=True)
df=df.fillna(-999)
dta=df.values
var=np.zeros(shape=(ni,nt,ns))
m=0
for t in range(nt):
  var[:,t,:]=dta[m:m+ns,2:].T
  m+=ns
var = np.ma.masked_where(var< 0, var)
```

### 測站編號與序號的對照

- 因測站編號不是從0開始，也會跳號，因此需以一個字典(`seqn`)來記錄編號與序號的對照關係。

```python
nw=len(twn)
twn=twn.sort_values(['new_code']).reset_index(drop=True)
seq=list(all_stn-old)
seq.sort()
seqn={seq[i]:i for i in range(len(seq))}
```

### 矩陣內積之執行

- 疏鬆矩陣fac的形成
- 因var矩陣中存在有缺值，是個遮蔽矩陣，因此必須使用`np.ma.dot`，否則只要有一個`nan`值，該日全部的鄉鎮區平均結果都會是`nan`

```python
fac=np.zeros(shape=(ns,nw))
for t in range(nw):
  n=len(twn.stns[t])
  if n==0:sys.exit('no stations in this town')
  for i in twn.stns[t]:
    if i in old:continue
    fac[seqn[i],t]=1/n
res=np.ma.dot(var,fac)
```

### 將矩陣轉為資料表

- 使用`np.outer`將維度向量(日期、鄉鎮區代碼)重複足夠多次，以符合二者長度的乘積。

```python
ymd=list(set(df.ymd));ymd.sort()
ymd=np.array(ymd,dtype=int)
one=np.ones(shape=(nw),dtype=int)
ymds=np.outer(ymd,one)
cod=list(set(twn.new_code));cod.sort()
cod=np.array(cod,dtype=int)
one=np.ones(shape=(nt),dtype=int)
cods=np.outer(one,cod)
dd=DataFrame({'ymd':ymds.flatten(),'TOWNCODE':cods.flatten()})
i=0
for c in col:
  dd[c]=res[i,:,:].flatten()
  dd.loc[dd[c]<0,c]=np.nan
  i+=1
```

### 結果輸出

```python
dd=dd.loc[dd.TOWNCODE>0].reset_index(drop=True)
dd.set_index('ymd').to_csv(yr+'res.csv')
```

## 程式下載

{% include download.html content="[stn_dot.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/TWNAQ/stn_dot.py)" %}

[town_aqstEnew.csv]: https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/AQana/GAQuality/NCAR_ACOM/CAM_pys/town_aqstEnew.csv "鄉鎮區與測站編號的對照表"