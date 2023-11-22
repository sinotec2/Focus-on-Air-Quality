import pandas as pd
from bs4 import BeautifulSoup
import os

df0=pd.DataFrame({})
col=['cat','id','gov','name','book','prog','desc']
with open("fnames.txt",'r') as f:
  fnames=[i.strip('\n') for i in f]
for fname in fnames:
  with open(fname,'r') as html:
    #使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

# 找到表格
    table = soup.find('table', {'id': 'cphContent_gvAbstract'})

# 提取表头
    header = [th.text.strip() for th in table.find_all('th', {'class': 'gridHeader'})]

# 提取表格数据
    data = []
    for row in table.find_all('tr', {'class': 'gridRow'}):
      row_data = [td.text.strip() for td in row.find_all('td')]
      data.append(row_data)

# 创建Pandas DataFrame
    df1 = pd.DataFrame(data, columns=header)
    combined_df = pd.concat([df0, df1], ignore_index=True)
    df0 = combined_df
    

