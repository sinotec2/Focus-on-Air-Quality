#!coding=utf8
import numpy as np
from pandas import *
from pypinyin import pinyin, lazy_pinyin
import subprocess
import json
from datetime import datetime, timedelta
from prep_df import PrepDf
import sys, os


#input and prepare the cnty names
df_cnty=read_csv('cnty.csv',encoding='big5')
for i in range(len(df_cnty)):
  cha=df_cnty.loc[i,'cnty']
  ll=lazy_pinyin(cha)
  s=''
  for l in ll:
    s=s+l
  df_cnty.loc[i,'cnty']=s
df_cnty['no']=[str(s) for s in df_cnty.no]
df_cnty['no']=['0'*(2-len(s))+s for s in df_cnty.no]
df_cnty.loc[len(df_cnty),'no']=51
df_cnty.loc[len(df_cnty)-1,'cnty']='lianjiangxian'

#dictionary of region name to county number
d_cnty={x:str(int(y)) for x,y in zip(df_cnty['cnty'],df_cnty['no'])}
d_cnty.update({'xinbeishi':'31','taoyuanshi':'32',\
'hualianjichang':'45','taidongjichang':'46','lvdaojichang':'46','lanyujichang':'46','magongjichang':'44','jinmenjichang':'50', \
'taizhongjichang':'36','tainanjichang':'21','jiayijichang':'40','qimeijichang':'44','wanganjichang':'44','beiganjichang':'51',\
'nanganjichang':'51','songshanjichang':'1','xiaogangjichang':'2','taoyuanjichang':'32'})

#combination of 5 Municipalities
NewCities={'tainanshi':{'21','41'},'taizhongshi':{'17','36'},'gaoxiongshi':{'2','42'}}

#including the harbors
gangko='gaoxionggang jilonggang anpinggang shenaozhuanyongyougang taibeigang shalunwaihaixieyoufutong suaogang taizhonggang mailiaogang budaigang xingdadianchangxiemeimatou yonganyehuatianranqijieshouzhan magonggang hualiangang hepinggang jinmengang mazugang'.split()
gangkoC=['2','11','21','31','31','36','34','36','39','40','42','42','44','45','45','50','51']
d_gangko={i:j for i,j in zip(gangko,gangkoC)}
d_cnty.update(d_gangko)

# air quality basins
d_kpq={'beibukongpinqu':['taibeishi','taoyuanshi','xinbeishi','jilongshi'], \
'gaopingkongpinqu':['gaoxiongshi','gaoxiongxian','pingdongxian'],\
'huadongkongpinqu':['hualianxian','taidongxian'], \
'yilankongpinqu':['yilanxian'],'yunjianankongpinqu':['yunlinxian','jiayixian','jiayishi','tainanshi'], \
'zhongbukongpinqu':['taizhongshi','taizhongxian','zhanghuaxian','nantouxian'], \
'zhumiaokongpinqu':['miaolixian','xinzhushi','xinzhuxian']}
d_kpq.update({'quanguo':list(df_cnty['cnty'])})
d_kpq.update({'lidao':['jinmenxian','lianjiangxian','penghuxian']})

#execution of dataframe formings and savings
csvs={'m':'mon.csv','w':'week.csv','d':'day.csv'}
for t in 'mwd':
  df='df_A'+t
  try:
    exec(df+'=read_csv("'+df+'")')
  except:  
    exec(df+'=PrepDf("'+csvs[t]+'")')
    exec(df+'.set_index("nsc2").to_csv("'+df+'")')

# output the dictionary
for kc in ['cnty','kpq']:
  with open('d_'+kc+'.json', 'w', newline='') as jsonfile:
    exec('json.dump(d_'+kc+', jsonfile)')

