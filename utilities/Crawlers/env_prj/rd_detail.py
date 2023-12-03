import os, sys, time
import requests
from bs4 import BeautifulSoup
from pandas import *
import numpy as np

df=read_csv('df0.csv')
columns= ['專案計畫編號', '經費年度', '計畫經費', '預算科目', '專案開始日期', '專案結束日期',
 '專案主持人', '主辦單位', '承辦人', '執行單位', '專案分類', '中文關鍵字', '英文關鍵字', '協同主持人',
 '共同主持人', '計畫聯絡人', '計畫聯絡電話', '計畫聯絡信箱']
for c in columns:
    df[c]=np.nan

with open('proj_link.txt') as f:
    htmls=[i for i in f]
i=0
for html in htmls:
    
    soup = BeautifulSoup(html, 'html.parser')

    # 查找包含project_id的链接
    link = soup.find('a', href=True)

    # 获取project_id
    project_id = link['href'].split('proj_id=')[1].split('&')[0]
    if project_id not in list(df.proj_id):continue

    # 定义目标URL
    url = "https://epq.moenv.gov.tw"+link['href']  # 请将URL替换为您的实际目标URL
    if 'keyword' not in url:continue

    # 发起HTTP请求获取页面内容
    response = requests.get(url)

    # 检查是否成功获取页面
    if response.status_code != 200:sys.exit('not connected')
    # 使用BeautifulSoup解析HTML
    html_content=response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # 找到表格
    table = soup.find('div', id="basicInfo")
    column = [th.text.strip() for th in table.find_all('th')]
    # 提取表格数据
    data = []
    for row in table.find('tbody').find_all('tr'):
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(row_data)
    d={c:l for c,l in zip(column,data)}
    # 创建Pandas DataFrame
    idx=df.loc[df.proj_id==project_id].index
    for c in columns:
        if c not in d:continue
        df.loc[idx,c]=d[c][0]
    i+=1
    if i%100==99:
        print(i)
        time.sleep(3)
df.set_index('yr_mg').to_csv('df0WithBasic.csv')   
