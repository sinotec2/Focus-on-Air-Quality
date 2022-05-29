import datetime as dt
import time, calendar
import os, sys
import warnings
import pandas as pd
from Lib import plot2D
from numpy import nan


def main():
    global now, tt_list, latlon, cmaqFil
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

    
    ######### 產生繪圖經緯度範圍 [lat: 119.3~122.1(E), lon: 21.82~25.43(N)]
    latlon_limit = [119.3, 122.1, 21.82, 25.43]
    latlon = [119.3, 122.1, 21.82, 25.43]


    ######Sim 先將CMAQ資料讀進來
    cmaqDir = os.path.join(os.getcwd(), 'Data', 'Sim', 'cctm')
    cmaqFil = os.path.join(cmaqDir, 'v1.' + keyTime + '.conc.nc')


    ##畫圖選擇
    MainPlot2D('hour')
    MainPlot2D('day')

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



@MainCMAQData
def MainPlot2D(CMAQData, Ttype):
    '''平面圖繪製'''
    CCtempt = CMAQData.CMAQData.sel(time=slice(tt_list[0] - dt.timedelta(hours=8),
                                               tt_list[1] - dt.timedelta(hours=8))) #只取整個月份的資料
    CCtempt['time']= CCtempt.time + pd.Timedelta(hours=8) # UTC -> LT

    if Ttype == 'hour':
       CCData = CCtempt
       pp2DspcList = ['O3', 'NO2', 'NMHC']
    elif Ttype == 'day':
       warnings.filterwarnings("ignore", category=FutureWarning)
       CCData =  CCtempt.resample(time = '1D').mean()
       pp2DspcList = ['PM10', 'PM25', 'NO2', 'SO2']
    
    pp2D = plot2D.plot2D(CCData, latlon)
    tmpT_list = CCData.time.values
    pp2DTimeList = [i for i in range(len(tmpT_list))]
    for spc in pp2DspcList:
       # print('Start to plot 2D : ' + spc)
        for tt in pp2DTimeList[:8]:
            pp2D.plot2D(spc, tt, type=Ttype)

if __name__ == '__main__':
    main()
