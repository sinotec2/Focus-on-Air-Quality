---
layout: default
title:  json converters
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-07-26 09:21:43
---
# grib2json
## download and compile
- need [maven][maven], `brew install maven` on macOS

```bash
git clone https://github.com/cambecc/grib2json.git
cd grib2json
mvn package
gz=/Users/Data/javascripts/D3js/earth/grib2json/target/grib2json-0.8.0-SNAPSHOT.tar.gz
cd  ~/MyPrograms/
tar tvfz $gz
ln -s ~/MyPrograms/grib2json-0.8.0-SNAPSHOT/bin/grib2json ~/bin
```

## help

### all options

```bash
> grib2json --help
Usage: grib2json [options] FILE
	[--compact -c] : enable compact Json formatting
	[--data -d] : print GRIB record data
	[--filter.category --fc value] : select records with this numeric category
	[--filter.parameter --fp value] : select records with this numeric parameter
	[--filter.surface --fs value] : select records with this numeric surface type
	[--filter.value --fv value] : select records with this numeric surface value
	[--help -h] : display this help
	[--names -n] : print names of numeric codes
	[--output -o value] : write output to the specified file (default is stdout)
	[--verbose -v] : enable logging to stdout
```
### pickup certain variables

--fp|parameterNumberName|#
:-:|-|-
0|Temperature|13
1|Relative_humidity|12
1|Pressure_reduced_to_MSL|1
2|U-component_of_wind|12
3|V-component_of_wind|12
5|Geopotential_height|11
6|Dew_point_temperature|1
8|Total_precipitation|1
9|Vertical_velocity|11
17|Skin_temperature|1

```bash
# --fp wind: convert both U and V-component of wind
grib2json -n -d --fp wind --fs 103 --fv 10.0 -o current-wind-surface-level-cwb-3K.json $grb

$ for i in {1..10};do echo $i $(grib2json --names --fp $i  $gb |grep "parameterNumberName");done
1 "parameterNumberName":"Relative_humidity", 
...
"parameterNumberName":"Vertical_velocity", "parameterNumberName":"Vertical_velocity",
10
```

### dump grib2 file to json
- with data：` grib2json -d -n -o $gb.json $gb`

# nc2json

# resource
- cambecc(2017), A command line utility that decodes [GRIB2](http://en.wikipedia.org/wiki/GRIB) files as JSON, [grib2json](https://github.com/cambecc/grib2json)
- pwcazenave(2017), Convert netCDF output to JSON for use in [earth](http://earth.nullschool.net https://github.com/cambecc/earth https://gitlab.ecosystem-modelling.pml.ac.uk/pica/earth), [netcdf2json](https://github.com/pwcazenave/netcdf2json/blob/master/netcdf2json.py)


[maven]: <https://zh.wikipedia.org/zh-tw/Apache_Maven> "Apache Maven，是一個軟體（特別是Java軟體）專案管理及自動構建工具，由Apache軟體基金會所提供。基於專案物件模型（縮寫：POM）概念，Maven利用一個中央資訊片斷(pom.xml)能管理一個專案的構建、報告和文件等步驟。Maven也可被用於構建和管理各種專案，例如C#，Ruby，Scala和其他語言編寫的專案。Maven曾是Jakarta專案的子專案，現為由Apache軟體基金會主持的獨立Apache專案。"