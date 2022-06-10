---
layout: default
title:  倒數計時與自動消失的文字方塊
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-04-28 14:18:56
---

# 倒數計時與自動消失的文字方塊

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
- 網頁開啟後自動下載gif檔案，畫面上一片空白，也不知道是發生什麼事、要等待幾時？實在不是很好的網頁經驗。
- 以既有畫面墊檔：畫面如果與即將顯示的gif不能搭配也蠻突兀的。
- 提示文字。畫面出現後還繼續留在頁面，也頗不協調。
- 似乎[倒數計時與自動消失的文字方塊]()是最佳的解決方案


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
<script src="js/jquery.js" type="text/javascript"></script><!--注意一定要加载jq文件-->
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
...
<h4><a href="https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/CALPUFF/Forecast/" target="_blank">CALPUFF Forecasting</a> Results</h4>            
<div id="text1">downloading PMF.gif, need about 10s, please wait... <span id="sec">10</span> </div>
...

```
| ![count_down.PNG](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/assets/images/count_down.png)|
|:-:|
| <b>CALPUFF[預測網頁](https://sinotec2.github.io/cpuff_forecast/)倒數計時畫面</b>|

## Reference
- 阿新、程式人生，[js實現div顯示2秒後自動消失](https://www.796t.com/content/1549098550.html), 2019-02-02
- 曉御9, Baidu, [HTML 文字自动消失效果](https://zhidao.baidu.com/question/306449269783701524.html), 2015-09-05