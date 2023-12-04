import os, sys, time
import requests
from bs4 import BeautifulSoup
from pandas import *
import numpy as np

df0=read_csv('df0WithBasic.csv')
df=DataFrame({})
columns= ['proj_id','chiAbs','engAbs' ]
cname={'中文摘要':'chi','摘要':'eng'}
df['proj_id']=list(df0.proj_id)
for c in columns[1:]:
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
    data = {}
    for lang in ['chi','eng']:
        table_rows = soup.select('#'+lang+'Subject table tbody tr')
        for row in table_rows:
            column = row.find_all('td')
            if column:
                key = row.find('th').text.strip()
                value = column[0].text.strip()
                data[key] = [value]
    # 创建Pandas DataFrame
    idx=df.loc[df.proj_id==project_id].index
    for c in cname:
        df.loc[idx,cname[c]+'Abs']=data[c][0]
    i+=1
    if i%100==99:
        print(i)
    time.sleep(1)
df.set_index('proj_idx').to_csv('df0WithAbs.csv')
