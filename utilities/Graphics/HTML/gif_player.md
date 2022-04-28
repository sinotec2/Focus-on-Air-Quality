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
- 空氣品質模擬結果是時間與空間的結合，將時間變化的平面濃度分布做成連續播放的動畫形式，是最合理與普遍的作法。範例如[美國本土臭氧指引預報](https://airquality.weather.gov/sectors/conusLoop.php#tabs)
- 一般瀏覽器內設GIF播放器的控制程度較低，不能暫停、前後微調、放大等等，必須套用適合的播放器。


| ![O3_CONUS.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/O3_CONUS.PNG)|
|:-:|
| <b>[美國本土臭氧指引預報](https://airquality.weather.gov/sectors/conusLoop.php#tabs)畫面</b>|

- 除了GIF型式，以電影檔案型式(mov, avi等)在Youtube上架展示，也是一個很多專業領域廣告的方式。
  - 除了基本廣播的功能，Youtube還會記錄點播次數與留言版功能，也是不錯的行銷管道。
- 類似的如IG、FB等等，如果已經有累積足夠的觀眾，也能有大量曝光的機會。只是社交平台上的播放器並沒有微調的功能，可能對動畫檔案的大小也會有所限制。

## html播放器方案
- 一般網頁鑲嵌的GIF播放器為了要吸引讀者的注意，大都設計成自動播放、輪流播放，而對較複雜內容、大型檔案則可以會設計成滑鼠滑過播放、或者是點擊播放。
- 在cssscript.com [JAVASCRIPT & CSS GIF PLAYER](https://www.cssscript.com/tag/gif-player/)這篇中回顧了2017~2022年最新的播放器，內容與樣式都與最新的網路應用(如FB)一致。

### [Gifa11y](https://github.com/search?q=Gifa11y)
- 使用 Vanilla JavaScript 程式庫
- 除了基本的播放功能，作者還公開其細部控制的程式碼，使用者可以自行設計個性之播放按鈕，
### [Gifffer](https://github.com/krasimir/gifffer/)
- 作者已經很久沒有更新了。
- 可以在函數下達放大、縮小的指令
- 沒有提供前、後轉微調的功能

### [LC-GIF-Player](https://github.com/LCweb-ita/LC-GIF-Player)
- 同一函數控制是否允許前後轉、放大

### [gifsee.js](https://github.com/klombomb/gifsee.js)
- 同時提供png檔讓使用者預覽，自動或點擊播放Gif。策略與FB相同。

## 實作成果
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
- lc_gif_player函數有4個引數，依序是GIF檔案與3個選項：
  1. 是否開啟網頁就自動播放。因為GIF檔案如果很大，這會讓網頁有一段時間空白需要有些內容填充因應。
  1. 是否有額外的點擊動作，如開啟另外的網頁等等，內設為否。
  1. 是否不允許前、後微調['move']、放大['fullscreen']GIF進行播放(涉詳細圖面洩漏資訊)，內設為全部開啟。

## Reference
- [buzzfeed](https://github.com/buzzfeed)提供的[LC-GIF-Player](https://github.com/LCweb-ita/LC-GIF-Player)