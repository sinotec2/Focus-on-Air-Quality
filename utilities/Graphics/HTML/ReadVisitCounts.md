---
layout: default
title:  網站來訪閱讀人次統計
parent: HTML
grand_parent: Graphics
last_modified_date: 2022-06-17 11:32:47
---

# 網站來訪閱讀人次統計

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

- 參考[浮云的博客](https://last2win.com/2020/01/19/GitHub-jekyll-view-counter/)
- 最後使用[不蒜子](https://cloud.tencent.com/developer/article/1669144)的2行js版本。

### 需要修正
- 編輯FOCUS-ON-AIR_QUALITY/_includes/header_custom.html

```html
<script src="https://busuanzi.ibruce.info/jquery/1.11.2/jquery.min.js"></script>
<!--<script src="//busuanzi.ibruce.info/jquery/2.1.3/jquery.min.js"></script>-->

<script src="https://busuanzi.ibruce.info/pintuer/1.0/pintuer.mini.js"></script>
<script src="https://busuanzi.ibruce.info/respond/1.4.2/respond.min.js"></script>
<script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>

```
- 編輯FOCUS-ON-AIR_QUALITY/_includes/footer_custom.html
- 原作者版本

```html
<div class="line text-big">
  <div class="x2 x2-move">
      <span id="busuanzi_container_page_pv">
          <div class="padding border border-sub border-dotted fadein-left">
              本文总阅读量<span id="busuanzi_value_page_pv"></span>次
          </div>
      </span>
  </div>
  <div class="x2 x1-move">
          <span id="busuanzi_container_site_pv">
              <div class="padding border border-sub border-dotted fadein-bottom">
                  本站总访问量<span id="busuanzi_value_site_pv"></span>次
              </div>
          </span>
  </div>
  <div class="x2 x1-move">
      <span id="busuanzi_container_site_uv">
           <div class="padding border border-sub border-dotted fadein-right">
               本站总访客数<span id="busuanzi_value_site_uv"></span>人
           </div>
      </span>
  </div>
</div>
```
- 修正版本
  - `{{ ... }}`內容為Jekyll指令
  - `id=...`會連結到header呼叫的js程式
  - `&emsp;`會[空4格](https://www.geeksforgeeks.org/how-to-insert-spaces-tabs-in-text-using-html-css/)
```html
{%- if site.footer_content -%}
  <p class="text-small text-grey-dk-100 mb-0">{{ site.footer_content }}</p>
{%- endif -%}

<p class="text-small text-grey-dk-100 mb-0">
<span id="busuanzi_container_page_pv">
    reads:<span id="busuanzi_value_page_pv"></span>times, &emsp;</span>
  <span id="busuanzi_container_site_pv">
          visits:<span id="busuanzi_value_site_pv"></span>, &emsp;</span>
<span id="busuanzi_container_site_uv">
       visitors:<span id="busuanzi_value_site_uv"></span>.</span>
</p>
```
## 結果

![ReadVisitCount](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/ReadVisitCount.PNG)

- 計數會連到[busuanzi.ibruce.info]()網站，計數結果顯示速度會有些慢。
- Github如果正在執行workflow，js會算不出來結果。
- 因計數自github.io重新編譯起算，因此數字會經常歸0
