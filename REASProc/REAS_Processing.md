---
layout: default
title: REAS Python
nav_order: 5
has_children: true
permalink: /REASProc/
last_modified_date:   2021-12-11 21:38:25
---

# REAS排放處理相關程式

{: .fs-6 .fw-300 }

---

## 數據下載
- 來源：[日本國立環境研究所](https://www.nies.go.jp/REAS/index.html#REASv3.2.1)
  - 按照年代、污染項目儲存  
  - Gridded Data Sets, see [Information for Data](https://www.nies.go.jp/REAS/Brief%20description%20about%20gridded%20data%20v3.2.1.pdf)
- 注意  
  - 共10個污染物質項目、270個文字檔案
  - 部分物質名稱之後有底線`_`
  - 雖然標題為**Gridded** Data，目錄下仍然也都有**點源**檔案

### 下載解壓縮

```bash
for s in SO2 NOX CO_ PM10_ PM2.5 BC_ OC_ NMV NH3 CO2;do 
  wget https://www.nies.go.jp/REAS/REASv3.2.1_Grid/$s/${s}_2015_GRID.tar.gz
  tar xvfz ${s}_2015_GRID.tar.gz
done
```
### 資料結構分析
```python 
os.system('findc  "REAS*" >fnames.txt')
os.system('for i in $(cat fnames.txt);do grep "/mon" $i|cut -d[ -f1;done >spec.txt')
with open('spec.txt','r') as f:
  l=[i.strip('\n').strip('_') for i in f]
fname_spec={i.split()[0]:i.split()[1] for i in l}
nmv=set([fname_spec[f] for f in fnames if 'NMV' in f]) #共21-2(NMV, Total_NMV)種VOC
specNonV=set([fname_spec[f] for f in fnames if 'NMV' not in f]) #共9種CNPS，part(BC,OC,PM2.5,PM10),CO2,ACNS
```
- 可以得到所有的成分共29種


## Reference
- Kurokawa, J. and Ohara, T. (2020). Long-term historical trends in air pollutant emissions in Asia: Regional Emission inventory in ASia (REAS) version 3. [Atmospheric Chemistry and Physics](https://acp.copernicus.org/articles/20/12761/2020/acp-20-12761-2020.html) 20 (21):12761–12793. doi:10.5194/acp-20-12761-2020.
