---
layout: default
title:  natural earth shp檔轉topo.json
parent: earth
grand_parent: Graphics
date: 2022-08-08
last_modified_date: 2022-09-02 11:57:54
tags: graphics earth gdal geojson
---

# natural earth shp檔轉topo.json
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

- 當增加[cambecc(2016)][eth] [earth][ens]套件的解析度時，會需要有較詳盡的底圖做為參考基準。這項作業的緣起是想重置[earth][eth]套件的底圖，在海岸線及湖泊外加上省(中國範圍)、縣(臺灣地區)等行政區向量圖，以備未來套用高解析度數據。
- [cambecc(2016)][eth]提供的向量底圖網址已經失效，同樣的內容改在[github][NTV]或[naturalearthdata官網][NE]提供。
  - 前者可供一次性全下載(約16GB)：`git clone https://github.com/nvkelso/natural-earth-vector.git`
  - 後者可視實際需要選取下載個別(zip)檔案。
- [Natural Earth(NE)][NE]目前為wrf-python等繪圖程式內設之公開底圖資料來源。其內容除自然(海岸線、河川、湖泊)之外，亦有文化類如行政區等疆界底圖。詳細解析度如表所示。

大類|次類|細類|說明
-|-|-|-
自然疆界(physical)|||
文化疆界(cultural)|Admin 0 – Countries|258 countries|
-|Admin 0 – Countries point-of-views|246~258 countries|國家主要領土(with Taiwan)
-|Admin 0 – Details|199 issue passports.|個別國家所有領土(with Taiwan)
-|Admin 0 – Boundary Lines|199 issue passports.|含領海(with Taiwan)
-|Admin 0 – Breakaway, Disputed Areas||主權爭議地區
-|Admin 1 – States, Provinces||[各國轄下之州、省範圍](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_1_states_provinces_lines.zip)
-|Admin 2 – Counties||美國各郡
-|[Populated Places](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_populated_places.zip)||主要城市包括大多數州(省)治

- 有關底圖的解析度：雖然NE提供到10m解析度的shape檔，但在[earth][ens]公開的套件中，隱含了內設的繪圖解析度，因此如果放大解析度時會出現鋸齒問題。
  - 原設定圖面最大倍率為3000。
  - 由其滑鼠點到位置的座標小數點到0.01來看，其解析度應為0.01度，約為1公里。
  - 這可以說明何以其海岸線會出現鋸齒狀。
  - 依據[cambecc(2016)][eth]之說明，此舉為topojson這支程式壓縮過程的結果
- [topojson][topojson]檔案的內容樣式特色是
  1. 較shape檔、geojson檔更加精練、檔案也較小，有存取便捷的特色。
  1. 以物件為主的json檔，而不是以座標為主。
  1. 一般性的點、線、多邊形等幾何特徵(如shape檔案中的物件)轉變成點、線、弧等單元，
  1. 座標系統由原來離散點的經緯度浮點實數，轉變成整數、且據關連性的indexing。
  1. topojson[轉換程式](https://trac.osgeo.org/gdal/wiki/Release/1.11.0-News)是OGR gdal套件中的一個程式，安裝時會複製到`/usr/bin/topojson`，其使用詳`topojson --help`

## 使用gdal套件轉換

- [cambecc(2016)][eth]建議使gdal套件來轉換.shp檔到.json檔、最後由`topojson`轉換程式轉成earth-topo.json檔案。經增修其腳本如下：

### oo.cs腳本

```bash
#kuang@node03 /nas1/Data/javascripts/D3js/earthCWB/public/data/topo
#$ cat oo.cs
for res in 10 50 110;do
for itm in coastline populated_places ;do
  ogr2ogr -f GeoJSON ${itm}_${res}m.json ne_${res}m_${itm}.shp
done
done
for itm in lakes ;do
  ogr2ogr -f GeoJSON -where "scalerank < 4" ${itm}_10m.json ne_10m_${itm}.shp
  ogr2ogr -f GeoJSON -where "scalerank < 4" ${itm}_50m.json ne_50m_${itm}.shp
  ogr2ogr -f GeoJSON -where "scalerank < 2 AND admin='admin-0'" ${itm}_110m.json ne_110m_${itm}.shp
done
itm=rivers_lake_centerlines_scale_rank
  ogr2ogr -f GeoJSON ${itm}_50m.json ne_50m_${itm}.shp
  ogr2ogr -f GeoJSON -simplify 1 ${itm}_tiny.json ne_110m_$itm.shp
riv=${itm/s_lake_centerlines_scale_rank/}
mv ${itm}_tiny.json ${riv}_tiny.json

itm=populated_places
for i in $(ls ${itm}*.json);do
  j=${i/${itm}/city}
  mv $i $j
done

ogr2ogr -f GeoJSON -simplify 1 coastline_tiny.json ne_110m_coastline.shp
ogr2ogr -f GeoJSON -simplify 1 -where "scalerank < 2 AND admin='admin-0'" lakes_tiny.json ne_110m_lakes.shp

ogr2ogr -f GeoJSON bounds_10m.json ne_10m_admin_1_states_provinces_lines.shp
ogr2ogr -f GeoJSON bounds_110m.json ne_110m_admin_0_boundary_lines_land.shp
ogr2ogr -f GeoJSON -simplify 1 bounds_tiny.json ne_110m_admin_0_boundary_lines_land.shp

topojson  --q1 100000 -o earth-topo.json \
coastline_10m.json coastline_50m.json coastline_110m.json \
lakes_10m.json lakes_50m.json lakes_110m.json \
river_50m.json river_tiny.json \
city_10m.json city_110m.json \
bounds_10m.json bounds_110m.json bounds_tiny.json
```

- 增加城市、河川、行政區界
- 還需修改的.js程式如下

### earth.js

- 畫面提交後會出現底圖，主要是在函數buildRenderer內控制
- 定義變數。原僅呼叫海岸線及湖泊，以下增加((...)內為json檔內之變數名稱)：
  1. 河川(rivers_lake_centerlines)
  1. 城市(populated_places)
  1. 行政區界(admin_1_states_provinces_lines)

```java
...
        var path = d3.geo.path().projection(globe.projection).pointRadius(7);
        var coastline = d3.select(".coastline");
        var river = d3.select(".rivers_lake_centerlines");
        var lakes = d3.select(".lakes");
        var city = d3.select(".populated_places");
        var bound= d3.select(".admin_1_states_provinces_lines");
        d3.selectAll("path").attr("d", path);  // do an initial draw -- fixes issue with safari
...
```

- 在停等滑鼠動作過程的起、迄點，呼叫到前述項目的最小、與最大解析度條件

```java
...
        // Attach to map rendering events on input controller.
        dispatch.listenTo(
            inputController, {
                moveStart: function() {
                    //river.datum(mesh.riverLo);
                    coastline.datum(mesh.coastLo);
                    lakes.datum(mesh.lakesLo);
                    //city.datum(mesh.cityLo);
                    //bound.datum(mesh.boundLo);
                    rendererAgent.trigger("start");
                },
                move: function() {
                    doDraw_throttled();
                },
                moveEnd: function() {
                    //river.datum(mesh.riverHi);
                    coastline.datum(mesh.coastHi);
                    lakes.datum(mesh.lakesHi);
                    //city.datum(mesh.cityHi);
                    //bound.datum(mesh.boundHi);
                    d3.selectAll("path").attr("d", path);
                    rendererAgent.trigger("render");
                },
                click: drawLocationMark
            });
...
```
- 關閉(放棄)這些新增項目的原因
  1. [cambecc(2016)][eth]似乎不接受線段之geometry，還是未給定顏色遭覆蓋，原因不明，新增項目均為黑影、且線段頭尾相連成為多邊形。
  1. 即使點狀之城市也為黑點，且大小不隨滑鼠縮放動作而異。

- 讀取解析度上下界

```java
...
    /**
     * @param resource the GeoJSON resource's URL
     * @returns {Object} a promise for GeoJSON topology features: {boundaryLo:, boundaryHi:}
     */
    function buildMesh(resource) {
        var cancel = this.cancel;
        report.status("Downloading...");
        return µ.loadJson(resource).then(function(topo) {
            if (cancel.requested) return null;
            log.time("building meshes");
            var o = topo.objects;
            var coastLo = topojson.feature(topo, µ.isMobile() ? o.coastline_tiny : o.coastline_110m);
            var coastHi = topojson.feature(topo, µ.isMobile() ? o.coastline_110m : o.coastline_10m); //50m -> 10m
            var riverLo = topojson.feature(topo, µ.isMobile() ? o.river : o.river_50m);
            var riverHi = topojson.feature(topo, µ.isMobile() ? o.river_50m : o.river_50m);
            var lakesLo = topojson.feature(topo, µ.isMobile() ? o.lakes_tiny : o.lakes_110m);
            var lakesHi = topojson.feature(topo, µ.isMobile() ? o.lakes_110m : o.lakes_10m);
            var cityLo = topojson.feature(topo, µ.isMobile() ? o.city_tiny : o.city_110m);
            var cityHi = topojson.feature(topo, µ.isMobile() ? o.city_110m : o.city_10m);
            var boundLo = topojson.feature(topo, µ.isMobile() ? o.bounds_tiny : o.bounds_110m);
            var boundHi = topojson.feature(topo, µ.isMobile() ? o.bounds_110m : o.bounds_10m);
            log.timeEnd("building meshes");
            return {
                coastLo: coastLo,
                coastHi: coastHi,
                riverLo: riverLo,
                riverHi: riverHi,
                lakesLo: lakesLo,
                lakesHi: lakesHi,
                cityLo: cityLo,
                cityHi: cityHi,
                boundLo: boundLo,
                boundHi: boundHi,
            };
        });
    }
```

### globes.js

- 有3處定義需注意新增：
  1. function standardGlobe() {defineMap: function(mapSvg, foregroundSvg) 
  1. function orthographic() {defineMap: function(mapSvg, foregroundSvg)
  1. function waterman() {defineMap: function(mapSvg, foregroundSvg) 

## GeoJson版本

- 由於[earth][ens]套件中不能接受多邊形之geometry，乃構想將shape檔中的多邊形轉換成之GeoJson，直接併入EN json檔中再進行轉換。

### shape to GeoJSON

- [mbostock, Mike Bostock](https://github.com/mbostock/shapefile)製作了一個好用的命令列執行檔。
- 轉換方式
  1. shape檔轉GeoJson可以借助[線上轉檔服務](https://products.aspose.app/gis/conversion/shapefile-to-geojson)。需提供.shp、.shx、.pro、.dbf等4個檔。
  2. 或直接取得臺灣縣市界的geoJSON檔案([eg. G0V@github](https://github.com/g0v/twgeojson/raw/master/json/twCounty2010.geo.json))
  3. 只是前述作法仍需注意年代版本，版本如果太舊會無法與現況對應。因[內政部](https://data.gov.tw/dataset/7441)不時更新數據，還是以最新版本shape檔進行轉換為宜。
- 轉成(或取得)geometry皆為MultiPolygon或polygon，與EN海岸線屬同一性質。

### coastline_10m.json 檔案之整理合併

1. 將coastline_10m.json檔案中臺灣部分(及離島)予以去除，以避免重疊干擾。(搜尋經緯度、整批物件一併去除)
2. 將前述轉成(取得)GeoJson檔案中features的物件，貼在coastline_10m.json檔案後面，(features是個序列，要記得逗點區格)。
3. 重新進行oo.cs當中的topojson動作，合併各個json檔。
4. 輸出點數(`--q1`)會影響物件的解析度。內設值為10K點，會得到約4Km的解析度，如增加為100K點，可以得到約400m的解析度，即使放大到縣市範圍(scaleExtent=60K)尚可接受。

```bash
topojson --help
 ...
 --q1, --post-quantization      maximum number of differentiable points along either dimension               [default: 10000]
```

### 結果

| ![GeoJson版本.png](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/GeoJson版本.png) |
|:--:|
| <b>圖 以g0v之twCounty2010.geo.json置換臺灣島海岸線之成果</b>|  

[NTV]: <https://github.com/nvkelso/natural-earth-vector> "Natural Earth is a public domain map dataset available at 1:10m, 1:50m, and 1:110 million scales. Featuring tightly integrated vector (here) and raster data (over there:https://github.com/nvkelso/natural-earth-raster), with Natural Earth you can make a variety of visually pleasing, well-crafted maps with cartography or GIS software."
[eth]: <https://github.com/cambecc/earth> "cambecc(2016), earth building, launching and etc on GitHub. "
[ens]: <https://earth.nullschool.net/> "earth, a visualization of global weather conditions, forecast by supercomputers, updated every three hours"
[NE]: <https://www.naturalearthdata.com/> "Natural Earth是一個地圖資料集專案，提供了1:10m、1:50m和1:110百萬三種比例尺的資料。Natural Earth提供的資料詳盡且細緻，資料集包含的資料整合了向量和點陣圖兩項資料。"
[topojson]: <https://en.wikipedia.org/wiki/GeoJSON#TopoJSON> "TopoJSON 是自GeoJSON發展的一個分支，二者都是對地理訊息的編碼方式。TopoJSON不以離散方式來表示幾何物件，而是從「弧」這個單元共享線段之整合。弧是點的序列，而線串和多邊形被定義為弧的序列。 每個弧只定義一次，但可以通過不同的形狀多次引用，從而減少冗餘並減小文件大小。此外，TopoJSON 促進了使用地理訊息的應用程序，例如保留原貌的簡化形狀、自動地圖著色和製圖等。"