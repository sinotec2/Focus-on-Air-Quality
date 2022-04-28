---
layout: default
title:  GIF播放器
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-04-28 15:37:23
---

# GIF播放器

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
- 空氣品質模擬結果是時間與空間的結合，將時間變化的平面濃度分布做成連續播放的形式，是最合理與普遍的作法。範例如[美國本土臭氧指引預報](https://airquality.weather.gov/sectors/conusLoop.php#tabs)
- 瀏覽器內設GIF播放器的控制程度較低，不能暫停、前後微調、放大等等。
O3_CONUS

| ![O3_CONUS.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/O3_CONUS.png)|
|:-:|
| <b>[美國本土臭氧指引預報](https://airquality.weather.gov/sectors/conusLoop.php#tabs)畫面</b>|

## 播放器方案

##

- 參考網友[buzzfeed](https://github.com/buzzfeed)提供的[LC-GIF-Player](https://github.com/LCweb-ita/LC-GIF-Player)，並加上windy外掛小視窗作為區域流向的參考，如圖所示。


| ![cpuff_forecast.png](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/cpuff_forecast.png)|
|:-:|
| <b>CALPUFF[預測網頁](https://sinotec2.github.io/cpuff_forecast/)畫面</b>|

```html
<link href="lc_gif_player.css" rel="stylesheet">
<script type="text/javascript" src="lc_gif_player.pack.js"></script>
<script type="text/javascript" src="libgif/libgif.min.js"></script>
<script type="text/javascript" src="libgif/libgif.js"></script>
...
<div class="content">
<div class="target target_4" style="max-height: 400px;">
    <img src="" rel:animated_src="example_gifs/PMF.gif" />
</div>

<script type="text/javascript">
document.addEventListener("DOMContentLoaded", function(event) {
    // no autoplay - no extra class - no prev/next commands
    // lc_gif_player('.target_1', false, '', ['move']);   
    // autoplay - no extra class - no fullscreen command
    lc_gif_player('.target_4', true, '', '');    
});
</script>
```

## Reference
- [buzzfeed](https://github.com/buzzfeed)提供的[LC-GIF-Player](https://github.com/LCweb-ita/LC-GIF-Player)