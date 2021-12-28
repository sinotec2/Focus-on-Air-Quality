

# Focus on Air Quality

這裡分享有關空氣品質及模式的分析工具與經驗


[What's New](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)、[Leave messages on GitHub](https://github.com/sinotec2/Focus-on-Air-Quality/discussions/)

---

## What's New
- 2021-12-10 [船舶排放](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ship/)依據的是面源資料庫中的一個(`NSC`)類別，但因港區排放太過集中，當成面源會低估其影響，因此要區分一部分排放成為點源。這是其複雜之處。因為TEDS11的船舶排放比TEDS10少很多，此處還是以2016年的數據為準。從面源到船舶，TEDS的處理算是完成了。
- 2021-12-08 整體TEDS系統最複雜(也最真實)的部分應該算是點源了，程式撰寫也花最多的篇幅。點源結束在[pt2em_d04](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/pt2em_d04/)這支轉檔程式，可以用來檢查高空點源的位置、時間變化是否正確。也可以參考[nbviewer](https://nbviewer.org/github/sinotec2/TEDS_PTSE/blob/main/pt2em_d04.ipynb)
- 2021-12-06 陸續完成了整體的架構和TEDS的處理程式，目前進度做了面源、植物源、線源、到了[高空點源](https://sinotec2.github.io/Focus-on-Air-Quality/EmisProc/ptse/ptseE_ONS)的**時變係數**。嘗試將[markdown](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseE_ONS.md)檔案[轉成](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/md2ipynb)[ipynb](https://raw.githubusercontent.com/sinotec2/Focus-on-Air-Quality/main/EmisProc/ptse/ptseE_ONS.ipynb)檔案，讓使用者可以在自己電腦上嘗試做看看(不必一定要工作站)，但畢竟`ipynb`強悍的是互動教學，太深的`for`、`if` 區段要配合說明就很難寫了，我盡量用加註`for eg.`方式說明，使用者自己可以用不同範例來試看看囉!([try this on nbviewer](https://nbviewer.org/github/sinotec2/Focus-on-Air-Quality/blob/main/EmisProc/ptse/ptseE_ONS.ipynb))
- 2021-11-30 一篇[evernote筆記](https://www.evernote.com/shard/s125/sh/b3f7003a-fd1d-4918-b617-1acb90b45219/25b5cbe6b72feca8dc5f0cec636eee78)拆成4篇[github.io](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/cwbWRF_3Km/)，應該可以把CWB數值預報的下載轉檔過程講解得清楚啦。慶幸的是這一題也有[網友](https://medium.com/%E6%9F%BF%E7%94%9C%E8%8C%B6%E9%A6%99/pygrib-%E7%AC%AC%E4%B8%80%E7%AB%A0-6b47e54f9085)在作，可能我們做得比較「硬斗」一點，我個人覺得內容比較豐富。
- 2021-11-29 與github-page經過一番奮戰，陸續完成了WPS、OBSGRID、REAL & WRF的架構，what's learned與圖片再慢慢加，應該有點參考價值啦。
- 2021-11-27 雖然程式有點舊，但還是忠實的進行著[NCEP](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/NCEP/)檔案自動下載與排程。
- 2021-11-26 陸續將過去CWB相關筆記上載到jtd，花了一些時間測試建立grand_children層級
  - CODiS網站[爬蟲程式](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/cwb_daily_download/)、
  - [軌跡程式](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/traj/)、
  - [little_r轉檔程式](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/CODiS/add_srfFF/)
- 2021-11-25 上載[dowps.md](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WPS/)之上載、新成立wind_models之parent層級
- 2021-11-24 前一天熬夜執行2018春季個案，處理了海溫數據，順便寫了[sst.md](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/SST/)
- 2021-11-23 貼上ncks.md做為測試jtd系統的範例

## About the project

FAQ is &copy; 2021-now by [sinotec2](http://github.com/sinotec2/).

### License

FAQ is distributed by an [MIT license](https://github.com/pmarsceill/just-the-docs/tree/master/LICENSE.txt).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [GitHub repo](https://github.com/sinotec2/Focus-on-Air-Quality/discussions/).

#### The contributor of FAQ

<ul class="list-style-none">
for contributor in site.github.contributors 
  <li class="d-inline-block mr-1">
 [contributor.login](https://github.com/sinotec2/Focus-on-Air-Quality/discussions/)
  </li>

</ul>

