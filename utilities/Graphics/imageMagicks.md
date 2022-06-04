---
layout: default
title: imageMagicks
parent: Graphics
grand_parent: Utilities
last_modified_date: 2022-06-04 10:12:36
---

# imageMagicks
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
- [imageMagicks](https://imagemagick.org/index.php)在各種作業平台都能通用的自由軟體。在圖形格式的轉換、修剪、裁切、去/加邊框等等動作，可以批次執行，非常方便。處理模式輸出圖檔，有其必要性與充分性。
- 相關中文說明也非常多。
- 這一題為什麼需要花時間、還寫成筆記，主要因為VERDI圖面有太多留空白的問題，需要裁切。裁切邊框也沒有問題，問題是組合成gif時，背景總又再出現，怎麼都改不了。最後還是[stackoverflow][stackoverflow]的討論比較有用。

### 安裝
- macOS用brew指令、linux用yum指令即可安裝

## 使用範例

### 格式轉換
- 使用[imageMagick](https://imagemagick.org/script/convert.php)串連連續圖檔成為gif
  - 轉換成gif時，convert會自動回復成原來的背景，`-background none`即可取消。
  - 範例:[wrf-python](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/wrf-python/3.vertica/#gif-producing)、[NCL and VERDI](https://sinotec2.github.io/cmaqprog/NCL_China_WBDust/)、
```bash
convert pm10*.png pm10.gif
convert -dispose 2 -coalesce +repage -background none  WRF_chem-*.png -size 895x565 WRF_chem.gif
```

- 解開gif檔案：`convert WRF_chem.gif WRF_chem.png`
  - 如果沒有指定數字格式，會產生WRF_chem-0.png, WRF_chem-1.png,..., WRF_chem-NN.png檔案，要注意檔案的排序。
- 轉換成pdf檔

```bash
kuang@114-32-164-198 /Users/cmaqruns/2016base/data/sites
$ grep convert *cs
sss.cs:    convert a$j.png a$j.pdf
```

### 裁減
- 修剪png檔案
  - 使用imagineMagicks `convert`一次修剪所有[VERDI](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/VERDI/VERDI_batch/#程式外批次檔calpuff結果時間序列圖檔展示)輸出的png檔案、再予以組合成gif
  - 或使用`-bordercolor white -trim` + `-bordercolor white -border 10%x10% `會比較整齊 (5% is enough)

```bash
for i in {0..54};do convert WRF_chem-$i.png -crop 950x550 a.png;mv a.png WRF_chemC-$i.png;done
for i in {0..9};do mv WRF_chemC-$i.png WRF_chemC-0$i.png;done
convert -dispose 2 -coalesce +repage -background none  WRF_chem-*.png -size 895x565 WRF_chem.gif
``` 


## Reference
- fmw42, [stackoverflow:How to trim animated gif (using imagemagick)?](https://stackoverflow.com/questions/44555789/how-to-trim-animated-gif-using-imagemagick), Jun 15, 2017 at 3:34

[stackoverflow]: <https://stackoverflow.com/questions/44555789/how-to-trim-animated-gif-using-imagemagick> "How to trim animated gif (using imagemagick)?"