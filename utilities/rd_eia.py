import pandas as pd
from bs4 import BeautifulSoup
import os
import subprocess

df0=pd.DataFrame({})
col=['cat', '案號', '主管機關', '名稱', '類別', '進度', '說明']
for icat in range(1,100):
  cat='B{:02d}'.format(icat)
  try:
    result=os.system('ls ~/GitHub/ITnotesGH/_posts/'+cat+'*html>fnames.txt')
  except:
    continue
# 请将HTML内容存储在html变量中
  with open("fnames.txt",'r') as f:
    fnames=[i.strip('\n') for i in f]
  if len(fnames)==0:continue
  abs='id\=\"cphContent_gvAbstract\"'
  for fname in fnames:
    with open(fname,'r') as html:
    #使用Beautiful Soup解析HTML
      soup = BeautifulSoup(html, 'html.parser')

# 找到表格
    table = soup.find('table', {'id': 'cphContent_gvAbstract'})

# 提取表头
    try:
      header = [th.text.strip() for th in table.find_all('th', {'class': 'gridHeader'})]
    except:
      continue
# 提取表格数据
    data = []
    for row in table.find_all('tr', {'class': 'gridRow'}):
      row_data = [td.text.strip() for td in row.find_all('td')]
      data.append(row_data)

# 创建Pandas DataFrame
    df = pd.DataFrame(data, columns=header)
    df.columns=col
    df['cat']=cat
    df0=df0.append(df,ignore_index=True)
df0.set_index('cat').to_csv('cat.csv')
