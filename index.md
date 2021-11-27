---
layout: default
title: Home
nav_order: 1
description: "Just the Docs is a responsive Jekyll theme with built-in search that is easily customizable and hosted on GitHub Pages."
permalink: /
last_modified_date: 2021-11-25 09:30:56
---

# Focus on Air Quality
{: .fs-9 }

這裡分享有關空氣品質及模式的分析工具與經驗
{: .fs-6 .fw-300 }

[What's New](https://sinotec2.github.io/jtd/docs/wind_models/NCEP/){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [Leave messages on GitHub](https://github.com/sinotec2/jtd/discussions/){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What's New
- 2021-11-27 雖然程式有點舊，但還是忠實的進行著[NCEP](https://sinotec2.github.io/jtd/docs/wind_models/NCEP/)檔案自動下載與排程。
- 2021-11-26 陸續將過去CWB相關筆記上載到jtd，花了一些時間測試建立grand_children層級
  - CODiS網站[爬蟲程式](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/cwb_daily_download/)、
  - [軌跡程式](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/traj/)、
  - [little_R轉檔程式](https://sinotec2.github.io/jtd/docs/wind_models/CODiS/add_srfFF/)
- 2021-11-25 上載[dowps.md](https://sinotec2.github.io/jtd/docs/wind_models/WPS/)之上載、新成立wind_models之parent層級
- 2021-11-24 前一天熬夜執行2018春季個案，處理了海溫數據，順便寫了[sst.md](https://sinotec2.github.io/jtd/docs/wind_models/SST/)
- 2021-11-23 貼上ncks.md做為測試jtd系統的範例

## About the project

FAQ is &copy; 2021-{{ "now" | date: "%Y" }} by [sinotec2](http://github.com/sinotec2/).

### License

FAQ is distributed by an [MIT license](https://github.com/pmarsceill/just-the-docs/tree/master/LICENSE.txt).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [GitHub repo](https://github.com/sinotec2/jtd/discussions/).

#### The contributor of FAQ

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>

