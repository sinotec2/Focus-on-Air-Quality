---
layout: default
title: Air_Evaluate_tool
parent: 後製工具
grand_parent: Recommend System
nav_order: 1
date: 2022-04-22 10:28:51
last_modified_date: 2022-04-22 10:28:56
---

# 空品性能評估工具(Air_Evaluate_tool)
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


## 檔案結構
- 整體程式庫、數據檔案目錄架構如圖1所示
- 分別將GRIDCRO2D及combine結果連結到mcip與cctm下即可

| ![Perf_Eval.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/Perf_Eval.PNG) |
|:--:|
| <b>圖1空品性能評估工具程式庫、數據檔案目錄架構</b>|

## [AirEva_Taiwan_d4.py](https://github.com/sinotec2/Focus-on-Air-Quality/blob/main/GridModels/TWNEPA_RecommCMAQ/post_process/AirEva_Taiwan_d4.py)
- 此程式由環保署委託單位撰寫、提供。 
  - 對話框出現後輸入年月(ex:2019-01)
  - 按法規架構區分北、中、雲、南、東等6區分別評估

```python
# kuang@DEVP /nas2/cmaq2019/download/model/post_process/Performance/Perf_Tools/Air_Evaluate_tool/Taiwan_d4
# $ cat -n AirEva_Taiwan_d4.py
1  import pandas as pd
2  import os, sys
3  import datetime, calendar
4  from Lib.Evaluate import Evaluate
5  from Lib.simobs_hr2day import simobs_hr2day
6  from Lib.simobs_readhr import sim_readhr, obs_readhr
7
8
9  try:
10      keyTime = input("請輸入性能評估月份，ex:2019-01 : ")
11      YY, MM = keyTime.split('-')
12      LM = calendar.monthrange(int(YY), int(MM))[1]
13      start = keyTime + '-01-00'
14      end   = keyTime + '-' + str(LM) + '-23'
15      RgTT = [start, end]
16  except ValueError:
17      print('！！！ 請確認輸入格式 ！！！')
18      sys.exit()
19  if (YY != '2019'):
20      print("！！！模擬年份請輸入'2019'！！！")
21      sys.exit()
22
23  nowTT = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
24
25  ##資料夾配置
26  workDir = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT+ '( ' +keyTime + ')')
27  ObsDir  = os.path.join(os.getcwd(), 'Data', 'Obs')
28  SimDir  = os.path.join(os.getcwd(), 'Data', 'Sim')
29  cmaqFil = os.path.join(SimDir, 'cctm', 'v1.'+keyTime+'.conc.nc')
30  gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
31  stFil   = os.path.join(SimDir, 'st.csv')
32
33
34  AirQ_Area = {'北部': ['基隆', '汐止', '萬里', '新店', '土城', '板橋', '新莊',
35                        '菜寮', '林口', '淡水', '士林', '中山', '萬華', '古亭',
36                        '松山', '桃園', '大園', '觀音', '平鎮', '龍潭', '湖口',
37                        '竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '陽明',
38                        '宜蘭', '冬山', '富貴角'],
39               '中部': ['竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '沙鹿',
40                        '大里', '忠明', '西屯', '彰化', '線西', '二林', '南投',
41                        '斗六', '崙背', '新港', '朴子', '台西', '嘉義', '竹山', '埔里'],
42               '雲嘉': ['彰化', '線西', '二林', '南投', '斗六', '崙背', '新港',
43                        '朴子', '台西', '嘉義', '新營', '善化', '安南', '台南',
44                        '美濃', '竹山', '埔里', '麥寮'],
45               '南部': ['朴子', '嘉義', '新營', '善化', '安南', '台南', '美濃',
46                        '橋頭', '仁武', '大寮', '林園', '楠梓', '左營', '前金',
47                        '前鎮', '小港', '屏東', '潮州', '恆春'],
48               '東部': ['台東', '花蓮', '埔里', '關山']}
49  #alls=[]
50  #for i in AirQ_Area:
51  #    alls+=AirQ_Area[i]
52  #AirQ_Area={'全區':alls}
53  allVar = {'O3': ['O3','NO2','NMHC'],
54            'PM': ['PM10','PM25','NO2','SO2']}
55
56
57  for area in AirQ_Area:
58      stons = AirQ_Area[area]
59
60      for cats in allVar:
61          Vars = allVar[cats]
62
63          for var in Vars:
64
65              obs_PH = obs_readhr(ObsDir, RgTT, stons, var)
66              sim_PH = sim_readhr(cmaqFil, gridFil, stFil, stons, var, RgTT)
67
68              if (var == 'O3'):
69                 ND = 40.
70              else:
71                 ND = 10.e-10
72              obs_PH = obs_PH.where(obs_PH >= ND, -999.)
73              sim_PH = sim_PH.where(obs_PH >= ND, -999.)
74
75              obs_DA, sim_DA = simobs_hr2day(obs_PH, sim_PH, RgTT)
76
77
78              data_dict = Evaluate(obs_PH, sim_PH, obs_DA, sim_DA, stons, cats, var)
79
80
81              outputfile = os.path.join(workDir, area, cats)
82              try:
83                 os.makedirs(outputfile)
84              except FileExistsError:
85                 pass
86
87              csvfile = os.path.join(outputfile, YY + MM + '_' + var + '_(for ' + cats +').csv')
88              pd.DataFrame.from_dict(data=data_dict).to_csv(csvfile, encoding ='utf-8-sig')
89
90  print('finish')
```
- 結果
  - 按照分析日期單獨建立目錄
  - 其下按照前述6區分別儲存
  - 每個空品區以下按照臭氧及PM分別儲存污染物總表
  - 每個污染項目、每一測站分別詳列驗證結果

```bash
#kuang@master /nas2/cmaq2019/download/model/post_process/Performance/Perf_Tools/Air_Evaluate_tool/Taiwan_d4/Data/Evaluate/2022-04-14-10-40-23( 2019-01)
$ tree
.
|-- 中部
|   |-- O3
|   |   |-- 201901_NMHC_(for O3).csv
|   |   |-- 201901_NO2_(for O3).csv
|   |   `-- 201901_O3_(for O3).csv
|   `-- PM
|       |-- 201901_NO2_(for PM).csv
|       |-- 201901_PM10_(for PM).csv
|       |-- 201901_PM25_(for PM).csv
|       `-- 201901_SO2_(for PM).csv
|-- 北部
|   |-- O3
|   |   |-- 201901_NMHC_(for O3).csv
|   |   |-- 201901_NO2_(for O3).csv
|   |   `-- 201901_O3_(for O3).csv
|   `-- PM
|       |-- 201901_NO2_(for PM).csv
|       |-- 201901_PM10_(for PM).csv
|       |-- 201901_PM25_(for PM).csv
|       `-- 201901_SO2_(for PM).csv
|-- 東部
|   |-- O<sub>3</sub>
|   |   |-- 201901_NMHC_(for O<sub>3</sub>).csv
|   |   |-- 201901_NO2_(for O<sub>3</sub>).csv
|   |   `-- 201901_O<sub>3</sub>_(for O<sub>3</sub>).csv
|   `-- PM
|       |-- 201901_NO2_(for PM).csv
|       |-- 201901_PM10_(for PM).csv
|       |-- 201901_PM25_(for PM).csv
|       `-- 201901_SO2_(for PM).csv
|-- 南部
|   |-- O3
|   |   |-- 201901_NMHC_(for O3).csv
|   |   |-- 201901_NO2_(for O3).csv
|   |   `-- 201901_O3_(for O3).csv
|   `-- PM
|       |-- 201901_NO2_(for PM).csv
|       |-- 201901_PM10_(for PM).csv
|       |-- 201901_PM25_(for PM).csv
|       `-- 201901_SO2_(for PM).csv
`-- 雲嘉
    |-- O3
    |   |-- 201901_NMHC_(for O3).csv
    |   |-- 201901_NO2_(for O3).csv
    |   `-- 201901_O3_(for O3).csv
    `-- PM
        |-- 201901_NO2_(for PM).csv
        |-- 201901_PM10_(for PM).csv
        |-- 201901_PM25_(for PM).csv
        `-- 201901_SO2_(for PM).csv
```
- 因目錄含有中文及空白鍵，以檔案總管開啟較為方便

| ![evalEO3.PNG](https://github.com/sinotec2/Focus-on-Air-Quality/raw/main/assets/images/evalEO3.PNG) |
|:--:|
| <b>圖2空品性能評估工具執行結果範例</b>|

