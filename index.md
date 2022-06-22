---
layout: default
title: Home
nav_order: 1
description: "Analysis tools and Simulation Experience about the Air Quality"
permalink: /
last_modified_date: 2022-06-03 17:15:36
---

# Focus on Air Quality
{: .fs-9 }

這裡分享有關空氣品質及模式的分析工具與經驗
{: .fs-6 .fw-300 }

[News at 2022-06-22](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/5IncProc/){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [sinotec2.github.io](https://sinotec2.github.io/){: .btn .fs-5 .mb-4 .mb-md-0 } [Leave messages at GitHub](https://sinotec2.github.io/Focus-on-Air-Quality/discussions/){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What's New
- 2022-06-22 電廠造成環境中O<sub>3</sub>或PM局部濃度的降低(負的增量)，這在法規中的增量分析該如何看待?學界和開發單位(顧問公司)立場不一。公版模式的後處理是景丰做的，這讓我們在審查時遭遇困難，因為教授不認為負值增量是開發單位的優惠。這一題關係到後處理該怎麼做，整理在 [增量濃度分析程序與檢討](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/5IncProc/) 也提出策略建議，請參考。
- 2022-06-04 把[2018/3/31~4/8 東亞地區解析度15Km之沙塵暴模擬分析](https://sinotec2.github.io/cmaqprog/NCL_China_WBDust/)整理在一起，也用[imageMagicks](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/imageMagicks)改善了VERDI圖檔留太多空白、背景重現的問題。
- 2022-06-02 更新了[AERMOD review](https://sinotec2.github.io/aermod/AERMOD_review.html)及[trajectory models](https://sinotec2.github.io/aermod/traj_review.html)2個學位論文搜尋結果，以及[可排序搜尋之表格](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/Graphics/HTML/SortFindTab/)的作法。回顧了CMAQ低估SO<sub>2</sub>和硫酸鹽的問題、看到公版模式對此也是束手無策，還是回頭開始慢慢更新[CAMx的工作方法](https://sinotec2.github.io/Focus-on-Air-Quality/CAMx/)比較實際一點。
- 2022-05-26 完成了新的[文獻回顧與專討(Paper Reviews)](https://sinotec2.github.io/Focus-on-Air-Quality/PaperReview/)大項，希望過去做的一些回顧性的文章、對外的公開簡報、經典的圖表，可以陸續用Markdown的格式整理起來，參考文獻、連結可以做得更好。有些不合時宜、可以有更多數據的，也都可以修正補充，還能留下修改時間，不致讓讀者用到太舊的資料。不過偏向domain的個案應用就是了。
- 2022-05-03 51勞動節假期間回顧了ncf線性篩選的問題，雖然過去解決了很多類似的問題，但究竟是怎麼回事，還是一知半解，網友也很少討論。給它取名叫[NC檔案多維度批次篩選](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/linear_fitering_NC/)，追究起來呢這是個誤會，nc.Dataset畢竟和np.array是有不小的差異的，後者還是比較會轉彎。
- 2022-04-19 疫情來了，有網友把每天公告的數據用leaflet寫了網頁公開在github.io。這引起我的興趣，也把一些靜態(廣播)網頁陸續搬到[https://sinotec2.github.io/](https://sinotec2.github.io/)，實則也想關閉httpd一下，好好找個防止[駭客攻擊](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/5IncProc/IPBlackNameList)的方法（不過這題基本上應該算是完成了@2022-04-23:）。
- 2022-04-09 新增了[煙流模式](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/)與[軌跡模式](https://sinotec2.github.io/Focus-on-Air-Quality/TrajModels/)的筆記、遠端計算網站也新增了[CALPUFF](http://114.32.164.198/CALPUFF.html)以及[CALINE](http://114.32.164.198/CALINE3.html)的功能。這2個加州開始發展的模式有著天壤之別的命運，是否開放原始碼似乎是蠻關鍵的因素，引以為戒啊。
- 2022-02-20 公司新購了工作站，意味著更大範圍、更多網格數的模擬變得更可能實現。不過初步嘗試，同時執行CWBWRF_15及3k雙向巢狀網格的[wrf.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/dowrf/)作業並沒有成功，只得以[ndown.exe](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/REAL/ndown/)及單向套疊進行，看起來是OK的。這表示對臺灣佔有80%貢獻的華東～華南地區，以後會跟臺灣本島同框進行空品模擬，這好像比較符合比例原則，有待爾後詳細的ISAM分析加以確認。
- 2022-02-11 自從過年期間iMac更新到Monterey之後，遠端執行的[CGI系統無法運作](https://discussions.apple.com/thread/253579026)，AERMAP的前處理程式[gen_inp](https://sinotec2.github.io/Focus-on-Air-Quality/PlumeModels/REnTG_pathways/gen_inp/)只得重新發布成讀取2020內政部[20M_dtm](https://data.gov.tw/dataset/138563)版本，不再以[EIO](https://pypi.org/project/elevation/)讀取30M_dtm，但還是維持本地執行[gdal_translate](https://gdal.org/programs/gdal_translate.html)的方案。(後續：參考[程式人生](https://www.796t.com/article.php?id=453663)建議重裝Apache/2.4.52，[遠端執行系統教學網站](http://114.32.164.198/aermods.html)終究還是修好了，不過也表示還欠很多相關遠端執行的筆記還沒有寫。重裝的筆記詳[monterey-pbms](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/POST/5IncProc/MacNetWorks/#monterey-pbms))
- 2022-01-30 東亞範圍15Km解析度的CMAQ模擬一直是個挑戰，除了資料的準備外，工作站是不是負荷得了也是關鍵。初步成果看來還好，因為是用手機操作，先貼上[結果](http://114.32.164.198/soong/pm10.gif)，過程與細節再慢慢補上囉。(2022-02-11已補上[東亞地區解析度15Km之CMAQ模擬分析](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/Abundant_NoG_Runs))
- 2022-01-05 日本國立環境研究所[REAS](https://www.nies.go.jp/REAS/)排放量有簡單的處理方式了。解析度15~27公里採內插、81公里採加總，結果如[圖](https://sinotec2.github.io/Focus-on-Air-Quality/Global_Regional_Emission/REAS/reas2cmaq/#結果檢視)。
- 2021-12-28 繼沙塵暴的[CMAQ-ISAM](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ISAM/)分析之後，同一個案也作為[ECMWF](https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4?tab=overview)再分析數據[下載](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/EC_ReAna/)、[重製](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2D1m3/)過程的[範例](https://sinotec2.github.io/Focus-on-Air-Quality/AQana/GAQuality/ECMWF/grb2D1m3/#%E7%B5%90%E6%9E%9C%E6%AA%A2%E8%A6%96)。這些再分析、反衍、模擬還是得正本清源找到揚沙的機制，這正是[WRF-chem](https://ruc.noaa.gov/wrf/wrf-chem/)的強項之一，因此又完成了[WRF-chem](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WRF-chem/)的安裝與東亞範圍的[模擬](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WRF-chem/rd_dust/#%E7%B5%90%E6%9E%9C%E6%AA%A2%E6%A0%B8)，這也符合規劃方向，陸續擴大[WRF](https://sinotec2.github.io/Focus-on-Air-Quality/wind_models/WRF/)的網格範圍、增加水平的解析度，以與中央氣象局的作法一致，希望可以避免除可能的錯誤和不必要的爭議。
- 2021-12-22 2018年4月5日大陸沙塵暴在臺灣造成高達200 &mu; g/M<sup>3</sup>的高值，**CMAQ-ISAM**分析結果如[圖](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/ISAM/SA_PM25_IONS/#%E6%88%90%E6%9E%9C%E6%AA%A2%E8%A6%96)，此次也整理了[CMAQ/bcon/mcip/isam](https://sinotec2.github.io/Focus-on-Air-Quality/GridModels/BCON/)相關的程式、輸入檔的準備過程、腳本等。應用了[Youtube](https://www.youtube.com/watch?v=8EbU2FIIOTU)來播放濃度結果動畫，同時也可以縮減貼圖檔案體積造成的壓力。
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

FAQ is &copy; 2021-{{ "now" | date: "%Y" }} by [sinotec2](http://github.com/sinotec2/).

### License

FAQ is distributed by an [MIT license](https://github.com/pmarsceill/just-the-docs/tree/master/LICENSE.txt).

### Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. Read more about becoming a contributor in [GitHub repo](https://github.com/sinotec2/Focus-on-Air-Quality/discussions/).

#### The contributor of FAQ

<ul class="list-style-none">
{% for contributor in site.github.contributors %}
  <li class="d-inline-block mr-1">
     <a href="{{ contributor.html_url }}"><img src="{{ contributor.avatar_url }}" width="32" height="32" alt="{{ contributor.login }}"/></a>
  </li>
{% endfor %}
</ul>
