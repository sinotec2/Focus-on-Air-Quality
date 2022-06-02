---
layout: default
title:  可排序搜尋之表格
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-06-02 16:13:54
---

# 可排序搜尋之表格

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
- 不必懷疑，國家圖書館[博碩士論文知識加值系統](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=d)已經提供非常完整的排序、搜尋功能，夫復何求？只差一個儲存的功能，總得將搜索的結果存在一個平台，不能每次都上國圖把諸多條件再打搜一遍吧?
- 早期用excel來做這事，還可以把摘要放在表格中，真的很方便。但excel程式太大、也不是跨平台，手機也想能看，excel方案也投降了。
- markdown雖然可以跨平台，但不能重排。(還有待發展吧)
- jQuery的[Sortable and Searchable Tables - Tablesort](https://www.jqueryscript.net/table/jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort.html)就成為好用、簡單的解決方案，唯一要做的就是把csv表格轉成html格式。這可不能用人工慢慢建吧?!還好，不少好心的網友提供了線上服務(如[Data Design Group, Inc.](https://www.convertcsv.com/csv-to-html.htm))，幸好這事只需要久久做一次。

## 資源
### setTimeout()，setTimeout()方法
- [程式人生](https://www.796t.com/content/1549098550.html)的方案似乎與按鍵動作可以連結，提醒使用者各項按鍵的功能，但又不會造成畫面的紛亂，類似的作法可以在leaflet的對話框中也可以發現。
- 好處是不必再連結什麼檔案，壞處是由按鍵觸發倒數，無法自動開始

```html
<html><head>
<script type="text/javascript">
function timedMsg()
{
var t=setTimeout("alert('5 seconds!')",5000)
}
</script>
</head><body>
<form>
<input type="button" value="Display timed alertbox!"
onClick="timedMsg()">
</form>
<p>Click on the button above. An alert box will be
displayed after 5 seconds.</p>
</body></html>
```

### jquery.js 方案
- [Baidu](https://zhidao.baidu.com/question/306449269783701524.html)算是非常單純的作法，只有2個變數：
  - #sec為倒數的秒數、
  - #text則為顯示的文字框。

```html
<span id="sec">5</span>秒后文字消失
<div id="text">文字呵呵呵</div>
<script src="js/jquery.js" type="text/javascript"></script><!--注意一定要加载jq文件-->
<!--省略其他html代码-->
<script type="text/javascript">
$(function(){
var time = $('#sec').html();
var interval = setInterval(function () {
--time;
$('#sec').html(time);
if (time <= 0) {
$('#text').hide();
clearInterval(interval);
}
}, 1000);
});
</script>
```

## 實作範例
- 最後方案：Baidu
- 將`<span>`元件放在`<div id=text1>`內，這樣連文字、連倒數的秒數，都會一併消失。
- 範例位址：[https://sinotec2.github.io/cpuff_forecast/](https://sinotec2.github.io/cpuff_forecast/)

```html
...
<h4><a href="https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/Forecast/" target="_blank">CALPUFF Forecasting</a> Results</h4>            
<div id="text1">downloading PMF.gif, need about 10s, please wait... <span id="sec">10</span> </div>
...
```
| ![count_down.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/count_down.PNG)|
|:-:|
| <b>CALPUFF[預測網頁](https://sinotec2.github.io/cpuff_forecast/)倒數計時畫面</b>|

## Reference
- 阿新、程式人生，[js實現div顯示2秒後自動消失](https://www.796t.com/content/1549098550.html), 2019-02-02
- 曉御9, Baidu, [HTML 文字自动消失效果](https://zhidao.baidu.com/question/306449269783701524.html), 2015-09-05