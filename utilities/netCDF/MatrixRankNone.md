---
layout: default
title:  矩陣階層numpy.newaxis(None)的用法
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-02-07 11:14:54
---
# 矩陣階層numpy.newaxis(None)的用法
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
- 地球科學領域經常遇到不同階層數的矩陣要進行4則(或更複雜的數學)運算的處境，一般的作法：
  - 以迴圈方式逐一進行，速度非常慢
  - 以[廣播](https://www.w3help.cc/a/202108/607444.html)方式進行，應用有其限制
  - **擴張**較階層較低的矩陣以與高階矩陣一樣(使用repeat、tile[指令](https://www.itread01.com/content/1546505845.html))。將會增加記憶體，且速度慢。
- 此處介紹以newaxis(None)指令，來增加虛擬的維度，產生類似tile的效果，一次性擴張低階矩陣以進行計算，速度快且不會造成記憶體增加。

## 空值(None)
- [空值](https://www.itread01.com/content/1550520906.html)是python變數的一個特殊屬性，在pandas中經常[應用](https://ithelp.ithome.com.tw/articles/10200052?sc=rss.qu)到。
- 此處是宣告一個空值之維度，其真實長度並不存在。

## 作法及範例
- 等號左側(LHS)的計算目標必須是一個已知形狀、高階的矩陣，形狀等同右側之高階矩陣(HLMatrix)
  - 可以使用已經定義過的既有(可覆蓋的)矩陣，也可以用np.zeros來宣告新的空白矩陣。

```python
LHS=np.zeros(shape=HLMatrix.shape)
```
- 等號右側的低階矩陣(LLMatrix)
  - 在已有的維度方向上要符合HLMatrix的格點數
  - 在空缺的維度上補以空值None，如下例：3維之排放量除以1維之面積

```python
NOx=NOx/area[None,:,None]
```
- 將逐時的壓力場減去時間平均之壓力場

```python
PH=nc['PH'][:]
PHBm=np.mean(PHB,axis=0) #const in time
PH=PHB[:,:,:,:]-PHBm[None,:,:,:]
```

- 2維濃度在時間向進行擴張(repeat)

```python
    arr=np.zeros(shape=(len(idt),nrow,ncol))
    arr[:,:,:]=var[None,:,:]*rat*unit_SHIP[s]
```
- [矩陣之降階](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2bc/#矩陣之降階selection)(selection)
  - source code:[github](https://github.com/sinotec2/cmaq_relatives/blob/master/bcon/grb2bc.py)

```python
def trans4_3(tt,ll,mm,ii):
#4-d transform to 3-d
  N=[np.zeros(shape=(tt,ll,mm),dtype=int) for i in range(4)]
  N[0][:,:,:]=np.array([t for t in range(tt)])[:,None,None]
  N[1][:,:,:]=np.array([k for k in range(ll)])[None,:,None]
  N[2][:,:,:]=ii[0][None,None,:]
  N[3][:,:,:]=ii[1][None,None,:]
  for n in range(4):
    N[n]=N[n].flatten()
  return N
```

## Further Reading
- [np.newaxis的用法](https://www.itread01.com/content/1547568207.html)