---
layout: default
title: "Global AQ Data Analysis"
parent: "AQ Data Analysis"
has_children: true
permalink: /AQana/GAQuality
nav_order: 1
---

# 全球空品模擬結果之下載與格式轉換
{: .no_toc }

- 地區空氣品質的模擬需要正確的邊界條件，過去的設定方式可以是：
  1. 乾淨、不受人為干擾、穩定、均勻的大氣組成(PROFILE)；
  1. 更大範圍的模式模擬或是資料同化的大氣組成(REGRID)；
- 就實際個案中，1.的情況並不存在，只能在某一個相對短暫、局部的狀況可以使用PROFILE，而2.是相對較合理的作法。全球一個大氣的角度，污染互相影響，也可能有迴流的情況，因此在既有全球的架構下進行地區的模擬，是目前最合理的作法。
- 就應用面，因為是作業化模式，這些全球空品模擬結果本身也可以用做即時分析以及研究的對象，議題包括：
  1. 長程傳輸現象與影響
  1. 污染成因探討，生物燃燒(森林、農田、桔稈等)、火山現象(噴發、火山灰、火山氣體)、黃沙、霧霾、都會區光化煙霧等，
  1. 天氣系統所造成污染傳播現象(颱風、高壓出海、冷高壓與低層噴流等)
-美國國家大氣研究中心(NCAR)長久以來發展全球大氣模式，其中也包括大氣成分的模式模擬，其結果也應用在區域空氣品質模式的邊界與初始濃度場。
-目前該中心發展維護的模式是CAM-chem (Community Atmosphere Model )及WACCM (Whole-Atmosphere Community Climate Model )模式。此2模式植基於MOZART-4模式，MOZART模式(Model for OZone and Related chemical Tracers )雖不再維護，然其過去模擬工作之準確性有一定水準，且自2007年迄2018年初，其後由WACCM及CAM-chem等模式完全取代。
- 此處介紹目前全球模式模擬(或資料同化)的作業系統、下載方式、以及資料轉換的方式。

{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---



