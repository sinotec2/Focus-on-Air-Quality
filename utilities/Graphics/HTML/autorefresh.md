---
layout: default
title:  自動更新文字檔內容
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-06-07 22:44:36
---

# 自動更新文字檔內容

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
- 程式在背景執行，一直猛按瀏覽器的`重現更新`鍵，來更新最新的輸出結果，這樣也不是個辦法，應該有更聰明的html來做這事吧？！
  - 自動更新可以用[meta tag更新](https://stackoverflow.com/questions/8711888/auto-refresh-code-in-html-using-meta-tags) ，不必自己點按。
  - 讀文字檔案可以用[object](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/object)連到指定的文字檔即可

## html
### isc3/aermod

- 只需更新文字檔案的目錄（/isc_results/isc3_ **RAND** /log.out）即可

```html
<!DOCTYPE html>
<html>
  
<head>
    <title>isc3/aermod progress</title>
    <meta http-equiv="refresh" content="10">
</head>
  
<body>
    <h2>Welcome To ISC3/AERMOD Remote Center</h2>
    <p>The log will reload after 10s.</p>
    <object height=300 width=950 type='text/plain' border=0 data=/isc_results/isc3_RAND/log.out></object>
</body>
  
</html>
```

### CALPUFF

```html
root@114-32-164-198 /Library/WebServer/Documents/cpuff_results/demo
# cat autorefresh.html 
<!DOCTYPE html>
<html>
  
<head>
    <title>cpuff progress</title>
    <meta http-equiv="refresh" content="10">
</head>
  
<body>
    <h2>Welcome To CALPUFF Remote Center</h2>
    <p>The log will reload after 10s.</p>
    <object height=300 width=950 type='text/plain' border=0 data=/cpuff_results/cpuf_RAND/cpuff.out></object>
</body>
  
</html>
```

