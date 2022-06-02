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

## 背景與資源方案
- 不必懷疑，國家圖書館[博碩士論文知識加值系統](https://ndltd.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi?o=d)已經提供非常完整的排序、搜尋功能，夫復何求？只差儲存分享的功能，總得將搜索的結果存在一個平台，不能每次都上國圖把諸多條件再打搜一遍吧?
- 早期用excel來做這事，還可以把摘要放在表格中，自動產生參考文獻標準寫法，真的很方便。但excel程式太大、也不是跨平台，手機也想能看，excel方案也投降了。
- markdown雖然可以跨平台，但不能重排。(還有待發展吧)
- zotero也是無敵方案，無可挑剔，有需要的人一起建立群組分享這些文獻，還能動態擴充，如果有協作，zotero是首選。只是zotero還不太能適應害羞的臺灣人。
- jQuery的[Sortable and Searchable Tables - Tablesort](https://www.jqueryscript.net/table/jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort.html)就成為好用、簡單的解決方案，唯一要做的就是把csv表格轉成html格式。這可不能用人工慢慢建吧?!還好，不少好心的網友提供了線上服務(如[Data Design Group, Inc.](https://www.convertcsv.com/csv-to-html.htm))，需要一點點程序、並且忍受廣告，但幸好這事只需要久久做一次。

## 文獻內容之csv檔案
- 國圖搜尋結果轉成csv檔案這一階段，目前還沒有另人滿意的自動方案。
  - 但是有比較聰明的手動方案，就是用excel複製、選擇性貼上(轉置)，將國圖直排的表格貼成橫排的資料庫型式。
- 每個系所的格調略有差異。這是沒法程式化的原因。
  - 因為不是每天執行，目前還沒有設計爬蟲程式的意願。

## html表頭
### 格式
- 直接抄下網友[SeanJM]()提供的2個css
- 平常OK，但放在github.io時會發生困難，因為style.css會呼叫google的Roboto.css，通過一個未加密的網站(http://...)，這對github來說是行不通的(同理適用在後續的2個js)。
  - 解決方案就是從該網站下載Roboto.css也放上github.io的repository，這樣不透過http呼叫肯定是沒有問題的。
  - 當然style.css的url指令就不需要了。

```html
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" type="text/css" href="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/css/tablesort.css">
<link rel="stylesheet" type="text/css" href="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/css/styles.css">
<link rel="stylesheet" type="text/css" href="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/css/Roboto.css">
```

### js程式
- github.io不允許呼叫`http://code.jquery.com/jquery-1.10.1.min.js`以及`http://yandex.st/highlightjs/7.3/highlight.min.js`這2支程式。作法同樣是從網站上下載後上放上Repository，讓html可以不必透過連外網直接讀到即可。

```html
<title>AERMOD ref</title>
<script type="text/javascript" src="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/jquery-1.10.1.min.js"></script>
<script type="text/javascript" src="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/highlight.min.js"></script>
<script type="text/javascript" src="jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort/tablesort.js"></script>
<script type="text/javascript">
            // For Demo Purposes
            $(function () {
                $('table.table-sort').tablesort();
                hljs.initHighlightingOnLoad(); // Syntax Hilighting
            });
        </script>
</head>
```
## 本體
### 表頭
- 表頭與傳統的表格有些不太一樣，呼叫js程式`table-sort`、`table-sort-search`、以及`table-sort-show-search-count`等3支程式


```html
<body>
<table class="table-sort table-sort-search table-sort-show-search-count">
  <thead>
    <tr style="text-align: center;">
      <th class="table-sort">類型</th>
      <th class="table-sort">研究生</th>
      <th class="table-sort">出版年</th>
      <th class="table-sort">論文名稱</th>
      <th class="table-sort">指導教授</th>
      <th class="table-sort">學位</th>
      <th class="table-sort">校院名稱</th>
      <th class="table-sort">系所名稱</th>
    </tr>
  </thead>
```
### 表內容
- 與傳統表格無異
```html
<tbody><tr>
<td>HRA</td>
<td>丁玉苓</td>
<td align="right">2020</td>
<td><a href=https://hdl.handle.net/11296/w9ap6u target="_block">半導體封裝及測試性工業區有害空氣污染物健康風險評估-以楠梓加工出口區為例</a></td>
<td>林清和</td>
<td>碩士</td>
<td>輔英科技大學</td>
<td>環境工程與科學系碩士班</td>
</tr>
...
</tbody></table>
```

## 實作範例
- [sinotec2.gitub.io:空品模式學位論文整理表格](https://sinotec2.github.io/)
  - [AERMOD review](https://sinotec2.github.io/aermod/AERMOD_review.html)
  - [trajectory models](https://sinotec2.github.io/aermod/traj_review.html)

## Reference
- SeanJM, 2013, [jQuery Plugin For Sortable and Searchable Tables - Tablesort](https://www.jqueryscript.net/table/jQuery-Plugin-For-Sortable-Searchable-Tables-Tablesort.html), 2013-07-01