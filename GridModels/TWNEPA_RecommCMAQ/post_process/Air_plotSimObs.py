import datetime as dt
import time, calendar
import os, sys
import pandas as pd
from Lib import plotSimObs
from numpy import nan


def main():
    global AirQ_Area, tt_list, plotTimeList, cmaqFil, gridFil, stFil, ObsDir
    AirQ_Area = {'北部': ['基隆', '汐止', '萬里', '新店', '土城', '板橋', '新莊', '菜寮',
                          '林口', '淡水', '士林', '中山', '萬華', '古亭', '松山', '桃園',]}
#                         '大園', '觀音', '平鎮', '龍潭', '湖口', '竹東', '新竹', '頭份', 
#                         '苗栗', '三義', '豐原', '陽明', '宜蘭', '冬山', '富貴角'],
#                '中部': ['竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '沙鹿', '大里',
#                         '忠明', '西屯', '彰化', '線西', '二林', '南投', '斗六', '崙背',
#                         '新港', '朴子', '台西', '嘉義', '竹山', '埔里'], 
#                '雲嘉': ['彰化', '線西', '二林', '南投', '斗六', '崙背', '新港', '朴子',
#                         '台西', '嘉義', '新營', '善化', '安南', '台南', '美濃', '竹山',
#                         '埔里', '麥寮'],
#                '南部': ['朴子', '嘉義', '新營', '善化', '安南', '台南', '美濃', '橋頭',
#                         '仁武', '大寮', '林園', '楠梓', '左營', '前金', '前鎮', '小港',
#                         '屏東', '潮州', '恆春'],
#                '東部': ['台東', '花蓮', '埔里', '關山']}

    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    ######### 產生繪圖時間間距
    try:
       keyTime = input("請輸入繪圖的【月份】，ex:2019-01: ")
       YY, MM = keyTime.split('-')
       monthCountDay = calendar.monthrange(int(YY), int(MM))[1]
       start = dt.datetime(int(YY), int(MM), 1)
       end = dt.datetime(int(YY), int(MM), monthCountDay)
    except ValueError:
       print('！！！ 請確認輸入格式 ！！！')
       sys.exit()

    if (YY != '2019'):
       print("！！！模擬年份請輸入'2019'！！！")
       sys.exit()

    tt_list = [start, end]
    plotTimeList = tt_list
    plotTimeList = [x.date() for x in plotTimeList]

    
    ######Sim 先將CMAQ資料讀進來
    cmaqDir = os.path.join(os.getcwd(), 'Data', 'Sim')
    cmaqFil = os.path.join(cmaqDir, 'cctm', 'v1.' + keyTime + '.conc.nc')
    gridFil = os.path.join(cmaqDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
    stFil   = os.path.join(cmaqDir, 'st.csv')

    ###### Obs 先將觀測資料讀進來
    ObsDir = os.path.join(os.getcwd(), 'Data', 'Obs')

    ##畫圖選擇
    MainPlotTimeSeries('scatter')
    MainPlotTimeSeries('timeseries')

    print('finish')


def MainCMAQData(func):
    from Lib import getCMAQ
    def wrap(*args, **kwargs):
        CMAQData = getCMAQ.getCMAQ(cmaqFil)
        if 'VOC' in CMAQData.CMAQData:
            CMAQData.CMAQData = CMAQData.CMAQData.rename({'VOC': 'NMHC'})  ##更改物種名稱
        if 'PM25_TOT' in CMAQData.CMAQData:
            CMAQData.CMAQData = CMAQData.CMAQData.rename({'PM25_TOT': 'PM25'})  ##更改物種名稱
        func(CMAQData, *args, **kwargs)
    return wrap


def TransData(data, Tvars):

    Trans_data = pd.DataFrame()
    for var in Tvars:
       if (var == 'O3') or (var == 'NMHC'):
          varSer = data[var]
       elif (var == 'NO2_hr'):
          varSer = data['NO2']
       elif (var == 'NO2_day'):
          varSer = data['NO2'].resample('D').mean()
       else:
          varSer = data[var].resample('D').mean()

       mask = (varSer.index >= tt_list[0]) & (varSer.index <= tt_list[-1])
       varSer = varSer.loc[mask]  ###去除掉跑到下個月的時間
       Trans_data =  pd.concat([Trans_data, varSer], axis=1, sort=False)

    Trans_data.columns = Tvars
    return Trans_data

@MainCMAQData
def MainPlotTimeSeries(CMAQData, type):
    from Lib import getEPA
    '''用MCIP換掉原先內部的lat,lon'''
    CMAQData.updateLL(gridFil)

    '''一邊讀入觀測及模擬值並畫圖(折線圖)'''
    for area in AirQ_Area:
#       print('目前進度:', area)
        for st in AirQ_Area[area]:
            #####讀入觀測資訊
            vars = ['PM10', 'PM25', 'NO2', 'SO2', 'O3', 'NMHC']
            obsSt = getEPA.getEPA(st, tt_list, vars, ObsDir)

            #####讀入CMAQ資訊
            stInfo = CMAQData.stInfo(stFil, st)
            stInfo.update({'area': area})
            cmaqSt = CMAQData.getCMAQst(lat=stInfo['lat'], lon=stInfo['lon'], vars=vars)

            if all(pd.isnull(obsSt['NMHC'])) == True:
               Tvars = ['PM10', 'PM25', 'NO2_day', 'SO2', 'O3', 'NO2_hr']
            else:
               Tvars = ['PM10', 'PM25', 'NO2_day', 'SO2', 'O3', 'NO2_hr', 'NMHC']

            pp = plotSimObs.plotSimObs(stInfo, TransData(obsSt, Tvars), TransData(cmaqSt, Tvars))
            for ii in range(len(plotTimeList) - 1):
                pp.plot(Tvars, [plotTimeList[ii], plotTimeList[ii + 1]], type=type)


if __name__ == '__main__':
    main()
