---
layout: default
title:  dt2jul and jul2dt
parent: Dates and Times
grand_parent: Utilities
last_modified_date:   2021-12-28 21:21:21
---

# dtconvertor
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
## Datetime轉Julian day
- [Julian day](https://zh.wikipedia.org/wiki/%E5%84%92%E7%95%A5%E6%97%A5)(*YYYYJJJ*)是地球科學上常用的日期表示方式，因為是連續的數字，經常用在時間間距的計算。
- Juian day就是距離當年元旦的日數+1，比較容易計算。
- 小時的計算就有一點複雜，此處以距離元旦0時的總秒數，扣掉日數差異造成的秒數，就是餘下的秒數，除以3600即為小時數。

## Julian day轉Datetime
- datetime 模組有豐富的函數可供計算使用，因此將整數的日期轉成datetime形式，有其便利之處。
- 直接用datetime.timedelta來計算元旦後的日數即可

## 程式碼
```python
def dt2jul(dt):
  yr=dt.year
  deltaT=dt-datetime(yr,1,1)
  deltaH=int((deltaT.total_seconds()-deltaT.days*24*3600)/3600.)
  return (yr*1000+deltaT.days+1,deltaH*10000)

def jul2dt(jultm):
  jul,tm=jultm[:]
  yr=int(jul/1000)
  ih=int(tm/10000.)
  return datetime(yr,1,1)+timedelta(days=int(jul-yr*1000-1))+timedelta(hours=ih)
```

## Reference
