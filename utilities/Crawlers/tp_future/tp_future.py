#!/home/anaconda3/envs/py37/bin/python
# /nas2/kuang/tp_future/tp_future.py
# coding: utf-8
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import json
from pandas import DataFrame
from selenium import webdriver
import datetime
import time
import codecs
import numpy as np

def clkid(ID):                                  #click the id
  button_element = driver.find_element("id",ID)
  button_element.click()
  return
def clkpath(ID):                       #click the xpath 
  button_element = driver.find_element(By.XPATH,ID)
  button_element.click()
  return
def SelectByIDnValue(ID,v):                     #click and select by value
  select = Select(driver.find_element(By.ID,ID))
  select.select_by_index(v)
  return

def click_run_save(d,t,w,s1,s2):
  day=datetime.date.today()+datetime.timedelta(days=d)
  clkid("tripFuturePickDate")
  driver.find_element(By.ID,"tripFuturePickDate").clear()
  input_1=driver.find_element(By.ID,"tripFuturePickDate")
  input_1.send_keys(day.strftime("%Y/%m/%d"))
  clkid("tripFuturePickTime")
  SelectByIDnValue("tripFuturePickTime",t)
  clkid("freeway_from")
  SelectByIDnValue("freeway_from",w)
  clkid("section_from")
  SelectByIDnValue("section_from",s1)
  clkid("freeway_from")
  SelectByIDnValue("freeway_end",w)
  clkid("section_from")
  SelectByIDnValue("section_end",s2)
  clkpath('//button[@class="button_primary tripplan_btn"]')
  if abs(s1-s2) >10:time.sleep(5)
  n = os.path.join("/nas2/kuang/tp_future", "results.html")
  f = codecs.open(n, "w", "utf−8")
  h = driver.page_source
  f.write(h)
  fn=open('results.html','r')
  soup = BeautifulSoup(fn,'html.parser')
  span=[str(i) for i in list(soup.find_all('span'))]
  lags=[i.split('約')[1].split('分')[0]+'分' for i in span if '約' in i]
  return lags

driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
driver.get("https://1968.freeway.gov.tw/tp_future")
SegOfWay={1:84,2:12,3:7,4:84,5:4,6:8,7:7,8:8,9:6,10:8}
#'1_0': '國道1號', 'N1H_0': '國1高架', '2_0': '國道2號',
# '3_0': '國道3號', 'N3A_0': '國道3甲', '4_0': '國道4號',
# '5_0': '國道5號', '6_0': '國道6號', '8_0': '國道8號', '10_0': '國道10號',

col=['date','hr','highway','segment1','segment2']
col+=['t'+str(i) for i in range(1,8)]
df=DataFrame({i:[] for i in col})
d0=DataFrame({i:[0] for i in col})
d0.set_index('date').to_csv('tp_future.csv')
i=0
for d in range(1,2):
  for t in range(1,49):
    for w in range(1,11):
      for s1 in range(SegOfWay[w]-1):
        s2=s1+1
        lags=click_run_save(d,t,w,s1,s2)
        df.loc[i,'date']=d
        df.iloc[i,1:]=[t,w,s1,s2]+lags
        d0.iloc[0,:]=[d,t,w,s1,s2]+lags
        i+=1
        time.sleep(1)

        lags=click_run_save(d,t,w,s2,s1)
        df.loc[i,'date']=d
        df.iloc[i,1:]=[t,w,s2,s1]+lags
        d0.iloc[0,:]=[d,t,w,s2,s1]+lags
        i+=1
        d0.set_index('date').to_csv('tp_future.csv',header=None,mode='a')
        time.sleep(np.random.randint(low=5,high=30))
