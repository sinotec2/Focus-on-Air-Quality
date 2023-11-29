---
layout: default
title:  環境相關法規之內部編號
parent: Regulation Reader
grand_parent: Crawlers
nav_order: 1
last_modified_date: 2023-11-29 04:45:34
tags: Crawlers pdf
---

# 環境相關法規之內部編號
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

- 法務部[全國法規資料庫](https://law.moj.gov.tw/Index.aspx)中個別法規的網頁(如公告場所室內空氣品質檢驗測定管理辦法`https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=O0130006`)是有一個`pcode`來作為指標的，必須再下載前得到這個指標與其名稱，以作為產出結果的命名。
- 作法上，先以關鍵字進行搜尋，將搜尋所得的結果畫面另存新檔(`e1.html` ~ `w2.html`)，再從法規列表中取得`href`另存新檔。
- 註記"廢"的意思是該部法規已經廢止不用，不需再下載避免造成困擾。

## 腳本

- 以下為擷取連結之腳本

```bash
for i in e n p s w;do
    grep "hlkLawLink" ${i}?.html|grep -v "label-fei"  >href_${i}.txt
done
```

- 結果如下所示。其中`title`即為法規名稱，href中的`pcode`即為法規指標代碼。

```html
$ head href_s.txt
s1.html: <a id="hlkLawLink" title="三級防制區既存固定污染源應削減污染物排放量準則" href="https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=O0020126&amp;cur=Ln&amp;kw=%e5%9b%ba%e5%ae%9a%e6%b1%a1%e6%9f%93%e6%ba%90">三級防制區既存<mark>固定污染源</mark>應削減污染物排放量準則</a>
s1.html: <a id="hlkLawLink" title="公私場所固定污染源申請改善排放空氣污染物總量及濃度管理辦法" href="https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=O0020061&amp;cur=Ln&amp;kw=%e5%9b%ba%e5%ae%9a%e6%b1%a1%e6%9f%93%e6%ba%90">公私場所<mark>固定污染源</mark>申請改善排放空氣污染物總量及濃度管理辦法</a>
s1.html: <a id="hlkLawLink" title="公私場所固定污染源空氣污染防制設備空氣污染防制費減免辦法" href="https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=O0020076&amp;cur=Ln&amp;kw=%e5%9b%ba%e5%ae%9a%e6%b1%a1%e6%9f%93%e6%ba%90">公私場所<mark>固定污染源</mark>空氣污染防制設備空氣污染防制費減免辦法</a>
s1.html: <a id="hlkLawLink" title="公私場所固定污染源空氣污染物排放量申報管理辦法" href="https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=O0020066&amp;cur=Ln&amp;kw=%e5%9b%ba%e5%ae%9a%e6%b1%a1%e6%9f%93%e6%ba%90">公私場所<mark>固定污染源</mark>空氣污染物排放量申報管理辦法</a>
s1.html: <a id="hlkLawLink" title="公私場所固定污染源復工試車評鑑及管理辦法" href="https://law.moj.gov.tw/Hot/AddHotLaw.ashx?pcode=O0020063&amp;cur=Ln&amp;kw=%e5%9b%ba%e5%ae%9a%e6%b1%a1%e6%9f%93%e6%ba%90">公私場所<mark>固定污染源</mark>復工試車評鑑及管理辦法</a>
```

