import os, glob
from bs4 import BeautifulSoup
import pandas as pd

source_directory="./"
html_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.html"))
df0=pd.DataFrame({})
gp_cat={}
for fname in html_files:
  # 初始化包含数据的列表
  data_list = []
  cat_id=fname.split('/')[-1][1:3]
  with open(fname,'r') as html:
    #使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html, 'html.parser')

# 查找包含proj_id、group_id和title的元素
    download_links = soup.find_all('a', class_='download_icon')

    for link in download_links:
      # 获取链接的href属性值
      href = link['href']
    
      # 使用split方法分割href，提取proj_id和group_id
      proj_id = href.split('proj_id=')[1].split('&')[0]
      if 'group_id' not in href:continue
      group_id = href.split('group_id=')[1]
      gp_cat.update({group_id:cat_id})
      # 获取链接的title属性值
      title = link['title']
    
      # 将提取的数据添加到data_list中
      data_list.append({'proj_id': proj_id, 'group_id': group_id, 'title': title})
  # 将data_list转换为Pandas数据表
  df = pd.DataFrame(data_list)
  combined_df = pd.concat([df0, df], ignore_index=True)
  df0=combined_df
# 打印Pandas数据表
df0['cat']=[gp_cat[i] for i in df0.group_id]
df0.set_index('proj_id').to_csv('env_prj.csv')

