#kuang@DEVP /nas2/sespub/epa_reports/downloading
#$ cat get_eiaDetail.py
#!/home/kuang/.conda/envs/py39/bin/python
import pandas as pd
import os, sys, time, random, glob, shutil
import requests
from bs4 import BeautifulSoup

'''
usage: get_eia.py B01 6 60 (kind of project, start and end of sequences)
'''

dfi=pd.read_csv(sys.argv[1]+'.csv')
dfi=dfi.loc[dfi.cat!='cat'].reset_index(drop=True)

# 创建一个 Chrome 浏览器实例
df=pd.DataFrame({})

for i in range(len(dfi)):
    id=dfi['id'][i]
    cat=dfi['cat'][i]
    nam=dfi['name'][i]
    url='https://eiadoc.moenv.gov.tw/eiaweb/10.aspx?hcode='+id+'&srctype=0'
    html_content = requests.get(url).text
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the table within the HTML content
    table = soup.find_all('table', {'class': 'table-condensed'})
    # Extract table data into a list of dictionaries
    ids=table[0].find_all({'input':'id'})
    dd={}
    for j in ids:
        dd.update({j.get('id'):[j.get('value')]})
    ids=table[1].find_all({'textarea':'id'})
    dd.update({ids[0].get('id'):[ids[0].text]})
    if i==0:
        df=pd.DataFrame(dd)
    else:
        combined_df = pd.concat([df, pd.DataFrame(dd)], ignore_index=True)
        df = combined_df
    if i%10==0:
        print(str(i)+nam)
        time.sleep(random.uniform(5, 20))
df.to_csv('detail.csv')
