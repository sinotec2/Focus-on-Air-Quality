---
layout: default
title:  ncgen & pncgen
parent: NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-06-26 19:20:18
tags: cpost uamiv
---

# ncgen & pncgen
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
- nc格式的檔案處理起來很快速、有效，但是如何不藉著模版、從零開始形成一個新的nc檔案呢？
  - 從python程式的nc.createDimension、nc.createVariable開始
  - 從fortran程式連結libioapi.a程式庫，write3()寫一個新的nc檔案
  - 或是此處要介紹的ncgen程式
- 雖然改變nc的程式已經非常多了，netCDF的原創單位Unidata還是提供了以格式轉換為主要功能的工具ncgen。
- 按照[官網](https://www.unidata.ucar.edu/software/netcdf/workshops/2011/utilities/NcgenExamples.html)說明，ncgen的功能至少有：
  1. 確認CDL(Common Data Language)格式檔案的內容
  1. 反轉[ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)輸出的結果，成為nc檔案。這項功能可以將txt檔案([ncdump](https://sinotec2.github.io/Focus-on-Air-Quality/utilities/netCDF/ncdump)輸出之CDL格式文字檔)，轉成nc檔案。如範例[run.ocean.sh](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/run.ocean.sh.TXT)
  1. 目的同2.，但是是由ncgen讀取cdl檔案來產生C, Fortran, or Java的程式碼、再編譯執行，以產生nc檔案。這樣可以留下處理過程，或用來產生類似、序列的檔案。
- 在此架構下，[PseudoNetCDF]也提供了pncgen，目的希望整合所有地球科學模式的IO格式，也都能有像nc格式一樣，有充分的軟體工具可以支援。

[uamiv]: <https://github.com/sinotec2/camxruns/wiki/CAMx(UAM)的檔案格式> "CAMx所有二進制 I / O文件的格式，乃是遵循早期UAM(城市空氣流域模型EPA，1990年）建立的慣例。 該二進制文件包含4筆不隨時間改變的表頭記錄，其後則為時間序列的數據記錄。詳見CAMx(UAM)的檔案格式"

## ncgen

```bash
Usage: ncgen [-1] [-3] [-4] [-5] [-6] [-7] [-b] [-B buffersize] [-d] [-D debuglevel] [-h] [-k kind ] [-l language=b|c|f77|java] [-M <name>] [-n] [-o outfile] [-P] [-x] [file ... ]
netcdf library version 4.4.0 of Feb 18 2016 16:50:31
```

       -b     Create  a  (binary) netCDF file.  If the -o option is absent, a default file name will be constructed from the base-
              name of the CDL file, with any suffix replaced by the ▒▒.nc▒▒ extension.  If a file already exists with the  specified
              name, it will be overwritten.

       -c     Generate C source code that will create a netCDF file matching the netCDF specification.  The C source code is writ-
              ten to standard output; equivalent to -lc.

       -f     Generate FORTRAN 77 source code that will create a netCDF file matching the netCDF specification.  The  source  code
              is written to standard output; equivalent to -lf77.

       -o netcdf_file
              Name  of  the file to pass to calls to "nc_create()".  If this option is specified it implies (in the absence of any
              explicit -l flag) the "-b" option.  This option is necessary because netCDF files  cannot  be  written  directly  to
              standard output, since standard output is not seekable.

       -k format_name

       -format_code
              The -k flag specifies the format of the file to be created and, by inference, the data model accepted by ncgen (i.e.
              netcdf-3 (classic) versus netcdf-4 vs netcdf-5). As a shortcut, a numeric format_code may be specified instead.  The
              possible format_name values for the -k option are:

                     ▒▒classic▒▒ or ▒▒nc3▒▒ => netCDF classic format

                     ▒▒64-bit offset▒▒ or ▒▒nc6▒▒ => netCDF 64-bit format

                     ▒▒64-bit data or ▒▒nc5▒▒ => netCDF-5 (64-bit data) format
                     ▒▒netCDF-4▒▒ 0r ▒▒nc4▒▒ => netCDF-4 format (enhanced data model)

                     ▒▒netCDF-4 classic model▒▒ or ▒▒nc7▒▒ => netCDF-4 classic model format
       Accepted format_number arguments, just shortcuts for format_names, are:

                     3 => netcdf classic format

                     5 => netcdf 5 format

                     6 => netCDF 64-bit format

                     4 => netCDF-4 format (enhanced data model)

                     7 => netCDF-4 classic model format
       The numeric code "7" is used because "7=3+4", a mnemonic for the format that uses the netCDF-3 data model for compatibility
       with the netCDF-4 storage format for performance. Credit is due to NCO for use of these numeric codes instead  of  the  old
       and confusing format numbers.

       Note:  The  old version format numbers ▒▒1▒▒, ▒▒2▒▒, ▒▒3▒▒, ▒▒4▒▒, equivalent to the format names ▒▒nc3▒▒, ▒▒nc6▒▒, ▒▒nc4▒▒, or ▒▒nc7▒▒ respectively, are also still accepted but deprecated, due to easy confusion between format numbers and format names.  Various
       old format name aliases are also accepted but deprecated, e.g. ▒▒hdf5▒▒, ▒▒enhanced-nc3▒▒, etc.  Also, note that -v is accepted
       to mean the same thing as -k for backward compatibility.

       -x     Don▒▒t initialize data with fill values.  This can speed up creation of large netCDF files  greatly,  but  later  at-
              tempts to read unwritten data from the generated file will not be easily detectable.

       -l output_language
              The  -l  flag  specifies  the output language to use when generating source code that will create or define a netCDF
              file matching the netCDF specification.  The output is written to standard output.   The  currently  supported  lan-
              guages have the following flags.

                     c|C▒▒ => C language output.

                     f77|fortran77▒▒ => FORTRAN 77 language output
                             ; note that currently only the classic model is supported.

                     j|java▒▒ => (experimental) Java language output
                             ;  targets the existing Unidata Java interface, which means that only the classic model is supported.


## pncgen
- 程式碼可以參考
  - [pseudonetcdf.readthedocs.io](https://pseudonetcdf.readthedocs.io/en/latest/_modules/PseudoNetCDF/pncgen.html)(2018)
  - [barronh/pseudonetcdf](https://github.com/barronh/pseudonetcdf/blob/master/scripts/pncgen)，較新
- 範例可以參考[hotexamples](https://python.hotexamples.com/zh/examples/PseudoNetCDF.pncgen/-/pncgen/python-pncgen-function-examples.html)

      $ pncgen --help
      usage: pncgen [-h] [--verbose] [--pnc PNC]
              [-f {see --list-formats for choices}] [--list-formats]
              [--help-format HELPFORMAT] [--sep] [--inherit] [--diskless]
              [--mangle] [--rename RENAME]
              [--remove-singleton REMOVESINGLETON] [--coordkeys key1,key2]
              [-v varname1[,varname2[,...,varnameN]]
              [-a att_nm,var_nm,mode,att_typ,att_val] [-m MASKS]
              [--from-convention FROMCONV] [--to-convention TOCONV]
              [--stack STACK] [--merge] [-s dim,start[,stop[,step]]]
              [-r dim,function[,weight]] [--mesh dim,weight,function]
              [-c dim,mode,wgt1,wgt2,...wgtN] [-e EXTRACT]
              [--extract-file EXTRACTFILE]
              [--extractmethod {ll2ij,nn,linear,cubic,quintic,KDTree}]
              [--op-typ OPERATORS] [--expr EXPRESSIONS]
              [--exprscript EXPRESSIONSCRIPTS] [-O]
              [--out-format {NETCDF3_CLASSIC,NETCDF4_CLASSIC,NETCDF4,arlpackedbit,bpch,cloud_rain,csv,ffi1001,height_pressure,humidity,ioapi,landuse,lateral_boundary,one3d,point_source,temperature,uamiv,vertical_diffusivity,wind,camxfiles.cloud_rain,camxfiles.height_pressure,camxfiles.humidity,camxfiles.landuse,camxfiles.lateral_boundary,camxfiles.one3d,camxfiles.point_source,camxfiles.temperature,camxfiles.uamiv,camxfiles.vertical_diffusivity,camxfiles.wind,noaafiles.arlpackedbit}]
              [--mode {w,a,r+,ws,as,r+s}]
              [ifiles [ifiles ...]] outpath
       PseudoNetCDF Argument Parsing

       positional arguments:
       ifiles                path to a file formatted as type -f
       outpath               path to a output file formatted as --out-format

       optional arguments:
       -h, --help            show this help message and exit
       --verbose             Provides verbosity with pncgen
       --pnc PNC             Set of pseudonetcdf commands to be process separately
       -f {see --list-formats for choices}, --format {see --list-formats for choices}
                            File format (default netcdf), can be one of the
                            choices listed, or an expression that evaluates to a
                            reader. Keyword arguments are passed via ,kwd=value.
       --list-formats        Show format options for -f
       --help-format HELPFORMAT
                            Show help for file format (must be one of the options
                            for -f)
       --sep                 Used to separate groups of arguments for parsing
                            (e.g., pncgen -- [options1] file(s)1 [--sep [options2]
                            file(s)2 [... [--sep [optionsN] file(s)N]]
       --inherit             Allow subparsed sections (separated with -- and --sep)
                            to inherit from global options (-f, --format is always
                            inherited).
       --diskless            Load file into memory; useful for subsequent
                            processing
       --mangle              Remove non-standard ascii from names
       --rename RENAME       Provide pairs of strings to be substituted
                            --rename=type,oldkey,newkey (type: v = variable; d =
                            dimension;)
       --remove-singleton REMOVESINGLETON
                            Remove singleton (length 1) dimensions
       --coordkeys key1,key2
                            Variables to be ignored in pncbo.
       -v varname1[,varname2[,...,varnameN], --variables varname1[,varname2[,...,varnameN]
                            Variable names or regular expressions (using match)
                            separated by ','. If a group(s) has been specified,
                            only variables in that (those) group(s) will be
                            selected.
       -a att_nm,var_nm,mode,att_typ,att_val, --attribute att_nm,var_nm,mode,att_typ,att_val
                            Variables have attributes that can be added following
                            nco syntax (--attribute
                            att_nm,var_nm,mode,att_typ,att_val); mode = a,c,d,m,o
                            and att_typ = f,d,l,s,c,b; att_typ is any valid numpy
                            type.
       -m MASKS, --mask MASKS
                            Masks to apply (e.g., greater,0 or less,0 or values,0,
                            or where,(time[:]%24<12)[:,None].repeat(10,1))
       --from-convention FROMCONV
                            From convention currently only support ioapi
       --to-convention TOCONV
                            To convention currently only supports cf
       --stack STACK         Concatentate (stack) files on the dimension.
       --merge               Combine variables into one file
       -s dim,start[,stop[,step]], --slice dim,start[,stop[,step]]
                            Variables have dimensions (time, layer, lat, lon),
                            which can be subset using dim,start,stop,stride (e.g.,
                            --slice=layer,0,47,5 would sample every fifth layer
                            starting at 0)
       -r dim,function[,weight], --reduce dim,function[,weight]
                            Variable dimensions can be reduced using
                            dim,function,weight syntax (e.g.,
                            --reduce=layer,mean,weight). Weighting is not fully
                            functional.
       --mesh dim,weight,function
                            Variable dimensions can be meshed using
                            dim,function,weight syntax (e.g.,
                            --mesh=time,0.5,mean).
       -c dim,mode,wgt1,wgt2,...wgtN, --convolve dim,mode,wgt1,wgt2,...wgtN
                            Variable dimension is reduced by convolve function
                            (dim,mode,wgt1,wgt2,...wgtN)
       -e EXTRACT, --extract EXTRACT
                            lon/lat coordinates to extract
                            lon1,lat1/lon2,lat2/lon3,lat3/.../lonN,latN
       --extract-file EXTRACTFILE
                            pncparse options for file
       --extractmethod {ll2ij,nn,linear,cubic,quintic,KDTree}
                            Method for extraction
       --op-typ OPERATORS    Operator for binary file operations. Binary file
                            operations use the first two files, then the result
                            and the next file, etc. Use // or <= or % or is not or
                            >> or & or == or != or + or * or - or / or < or >= or
                            ** or > or << or | or is or ^
       --expr EXPRESSIONS    Generic expressions to execute in the context of the
                            file.
       --exprscript EXPRESSIONSCRIPTS
                            Generic expressions to execute in the context of the
                            file.
       -O, --clobber         Overwrite existing file if necessary.
       --out-format {NETCDF3_CLASSIC,NETCDF4_CLASSIC,NETCDF4,arlpackedbit,bpch,cloud_rain,csv,ffi1001,height_pressure,humidity,ioapi,landuse,lateral_boundary,one3d,point_source,temperature,uamiv,vertical_diffusivity,wind,camxfiles.cloud_rain,camxfiles.height_pressure,camxfiles.humidity,camxfiles.landuse,camxfiles.lateral_boundary,camxfiles.one3d,camxfiles.point_source,camxfiles.temperature,camxfiles.uamiv,camxfiles.vertical_diffusivity,camxfiles.wind,noaafiles.arlpackedbit}
                            File output format (e.g., NETCDF3_CLASSIC,
                            NETCDF4_CLASSIC, NETCDF4;pncgen only)
       --mode {w,a,r+,ws,as,r+s}
                            File mode for writing (w, a or r+ or with unbuffered
                            writes ws, as, or r+s; pncgen only).

       Detailed Steps
       --------------

       PseudoNetCDF has many operations and the order often matters. The order is
       consistent with the order of options in the formatted help. The default order
       is summarized as:

       1. Open with specified reader (-f)
       2. Select subset of variables (-v)
       2. Add attributes (-a)
       4. Apply masks (--mask)
       5. Add conventions to support later operations (--to-conv, --from-conv)
       6. Combine files via stacking on dimensions (--stack)
       7. Slice dimensions (-s --slice)
       8. Reduce dimensions (-r --reduce)
       9. Convolve dimensions (-c)
       10. Extract specific coordinates (--extract)
       11. Remove singleton dimensions (--remove-singleton)
       12. Apply expressions (--expr then --exprscripts)
       13. Apply binary operators (--op_typ)

       To impose your own order, use standard options (global options) and then
       use -- to force positional interpretation of remaining options. In remaining
       options, use --sep to separate groups of files and options to be evaluated
       before any global operations.

### example：pnc_congrd02
- `-f uamiv`指定輸入格式是[uamiv][uamiv]
- `-a TSTEP,global,o,i,$NSTEP`指定TSTEP屬性的內容，是整數其值為$NSTEP
       - 再將其轉回[uamiv][uamiv]檔案才會正確
- `--from-conv=ioapi`、`--to-conv=cf`指定協訂內容是ioapi或者是[CF](http://cfconventions.org/latest.html)(Climate and Forecast (CF) Metadata Conventions)。

```bash
$ cat /usr/kbin/pnc_congrd02
PTH=/cluster/miniconda/envs/unresp/bin
PNCD=$PTH/pncdump
NSTEP=`$PNCD --head -f uamiv calpuff.con.S.grd02 |grep NSTEPS|grep \=|awkk 3|tail -n1`
$PTH/pncgen.py -f uamiv -a TSTEP,global,o,i,$NSTEP --from-conv=ioapi --to-conv=cf -O calpuff.con.S.grd02 calpuff.con.S.grd02.nc
$PTH/pncgen --out-format=uamiv -O calpuff.con.S.grd02.nc  calpuff.con.S.grd02
#rm calpuff.con.S.grd02.nc
$PTH/pncgen -f uamiv -O calpuff.con.S.grd02 calpuff.con.S.grd02.nc
```

{% include warning.html content="pncgen的結果檔案是接著-O選項之後，與一般NCO指令是在最後的習慣不同！" %}


## pncgen/pncdump 所有可接受的格式
### 一般格式

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-|:-|-|
||Dataset
||MetaNetCDF|MetaNetCDF.MetaNetCDF
||WrapPNC
||add_derived|MetaNetCDF.add_derived
||aqsraw|epafiles.aqsraw
||ceilometerl2|ceilometerfiles.ceilometerl2
||csv|textfiles.csv
||ffi1001|icarttfiles.ffi1001.ffi1001
||nc
||ncf
||netcdf
||newresolution|MetaNetCDF.newresolution
||reader|aermodfiles.reader
||time_avg_new_unit|MetaNetCDF.time_avg_new_unit
||window|MetaNetCDF.window
||woudcsonde|woudcfiles.woudcsonde

### WRF模式

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-|:-|-|
||wrf|wrffiles.wrf
||wrf_base|wrffiles.wrf_base

### CMAQ模式

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-:|:-|-|
|OMI數據檔|cmaqomidat|cmaqfiles.cmaqomidat||
|網格定義檔|griddesc|cmaqfiles.griddesc||
|濃度|ioapi|cmaqfiles.ioapi||
||ioapi_base|cmaqfiles.ioapi_base||
|光解係數|jtable|cmaqfiles.jtable||
|剖面邊界場|bcon_profile|cmaqfiles.profile.bcon_profile||
|剖面初始場|icon_profile|cmaqfiles.profile.icon_profile||

### GeoChem模式

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-:|:-|-|
|診斷檔|_diag_group|geoschemfiles._diag_group||
|二進位診斷場|bpch|geoschemfiles.bpch||
||bpch1|geoschemfiles.bpch1||
||bpch2|geoschemfiles.bpch2||
||bpch_base|geoschemfiles.bpch_base||
|飛行紀錄|flightlogs|geoschemfiles.flightlogs||
|geoschem NC|gcnc|geoschemfiles.gcnc||
||gcnc_base|geoschemfiles.gcnc_base||
|濃度|geos|geoschemfiles.geos||

### NOAA檔案

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-:|:-|-|
|濃度|arlconcdump|noaafiles.arlconcdump
|壓縮|arlpackedbit|noaafiles.arlpackedbit
|顆粒|arlpardump|noaafiles.arlpardump
|軌跡|arltrajdump|noaafiles.arltrajdump
|l100|l100|noaafiles.l100

### CAMx 

|類別|-f 格式名稱|method名稱|說明|
|:-:|:-|:-|-|
|雲雨|cloud_rain|camxfiles.cloud_rain.Memmap.cloud_rain||
||cloud_rain_center_time|camxfiles.cloud_rain.Transforms.cloud_rain_center_time||
||cloud_rain_center_time_plus|camxfiles.cloud_rain.Transforms.cloud_rain_center_time_plus||
||cloud_rain_plus|camxfiles.cloud_rain.Transforms.cloud_rain_plus||
|垂直擴散係數|vertical_diffusivity|camxfiles.vertical_diffusivity.Memmap.vertical_diffusivity||
|||camxfiles.vertical_diffusivity.Read.vertical_diffusivity||
||vertical_diffusivity_center_time|camxfiles.vertical_diffusivity.Transforms.vertical_diffusivity_center_time||
|高度壓力|height_pressure|camxfiles.height_pressure.Memmap.height_pressure||
|||camxfiles.height_pressure.Read.height_pressure||
||height_pressure_center_time|camxfiles.height_pressure.Transforms.height_pressure_center_time||
||height_pressure_center_time_plus|camxfiles.height_pressure.Transforms.height_pressure_center_time_plus||
||height_pressure_plus|camxfiles.height_pressure.Transforms.height_pressure_plus||
|濕度|humidity,|camxfiles.humidity.Memmap.humidity||
|||camxfiles.humidity.Read.humidity||
||humidity_center_time|camxfiles.humidity.Transforms.humidity_center_time||
|溫度|temperature|camxfiles.temperature.Memmap.temperature||
|||camxfiles.temperature.Read.temperature||
||temperature_center_time|camxfiles.temperature.Transforms.temperature_center_time||
|風|wind|camxfiles.wind.Memmap.wind||
|||camxfiles.wind.Read.wind||
||wind_center_time_cell|camxfiles.wind.Transforms.wind_center_time_cell||
|總臭氧|tomsl3|toms.level3.tomsl3||
|土地使用|landuse|camxfiles.landuse.Memmap.landuse||
|邊界濃度|lateral_boundary|camxfiles.lateral_boundary.Memmap.lateral_boundary||
|常數|one3d|camxfiles.one3d.Memmap.one3d||
|||camxfiles.one3d.Read.one3d||
|點源|point_source|camxfiles.point_source.Memmap.point_source
|||camxfiles.point_source.Read.point_source
|初始值/濃度/面源/瞬間值|uamiv|camxfiles.uamiv.Memmap.uamiv
|||camxfiles.uamiv.Read.uamiv
|細網格瞬間值|finst|camxfiles.finst.Memmap.finst
|臭氧來源|osat|camxfiles.uamiv.Transforms.osat||
|程序分析|ipr|camxfiles.ipr.Memmap.ipr||
||ipr|camxfiles.ipr.Read.ipr||
||irr|camxfiles.irr.Memmap.irr||
||irr|camxfiles.irr.Read.irr||

