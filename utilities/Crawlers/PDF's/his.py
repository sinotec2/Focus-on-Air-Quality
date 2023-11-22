from pandas import *
df=read_csv('cat.csv')
df.head)
df.head()
len(set(df.cat))
!cp ../works/*json .
ls *json
import json
with open('proj_class.json','r') as f:
    pc=json.load(f)
len(set(pc))
set(pc)-set(df.cat)
nov=set(pc)-set(df.cat)
[pc[i] for i in nov]
col=['cat','id','gov','name','book','prog','desc']
df.columns=col
df.loc[df.id=='0870141D']
df.loc[df.id.map(lambda x:'41D' in x)]
lst
!ls
!lst
!lst
!lst
lst
!lst
!lst
!vi rd_allPages.py
!vi rd_allPages.py
df.loc[df.id.map(lambda x:'41D' in x)]
len(set(df.book))
set(df.book)
set(df.prog)
!lst
df=df.sort_values(by="id", ascending=False)
df.head()
df=df.sort_values(by="id", ascending=False).reset_index(drop=True)
df.head()
a=df.loc[(df.prog=='通過審查') & (df.id.map(lambda x:int(x[:4])>=107))]
len(a)
a.head(30)
df=df.drop_duplicates().reset_index(drop=True)
df.head()
len(df)
!wc cat.csv
a=df.loc[(df.prog=='通過審查') & (df.id.map(lambda x:int(x[:4])>=107))].reset_index(drop=True)
len(a)
a.head(30)
set(a.book)
set(df.prog)
[i for i in set(df.prog) if '通過' in i]
[i for i in list(set(df.prog)) if '通過' in i]
[i for i in list(set(df.prog)) if '通過' in i and type(i)== str]
[i for i in list(set(df.prog)) if type(i)== str]
b=[i for i in list(set(df.prog)) if type(i)== str]
[i for i in b if '通過' in i and type(i)== str]
pas=[i for i in b if '通過' in i and type(i)== str]
a=df.loc[(df.prog.map(lambda x: x in pas)) & (df.id.map(lambda x:int(x[:4])>=107))].reset_index(drop=True)
len(a)
a.head(30)
pc
[i for i in pc.values if '風' in i]
pc.values
[i for i in pc if '風' in pc[i]]
wind=df.loc[df.nam.map(lambda x:'風' in x)].reset_index(drop=True)
wind=df.loc[df.name.map(lambda x:'風' in x)].reset_index(drop=True)
wind.head()
len(wind)
wind.name
wind=df.loc[df.name.map(lambda x:'風力' in x)].reset_index(drop=True)
len(wind)
wind.name
wind.head()
set(df.prog)
wind=df.loc[(df.name.map(lambda x:'風力' in x)) & (df.prog!='審查中')].reset_index(drop=True)
len(wind)
wind.tail()
near=(df.id.map(lambda x:int(x[:4])>=107))
wind=df.loc[(df.name.map(lambda x:'風力' in x)) & (df.prog!='審查中') & near ].reset_index(drop=True)
len(wind)
wind.tail()
wind=df.loc[(df.name.map(lambda x:'風力' in x)) & (df.prog!='審查中') & (df.id.map(lambda x:int(x[:4])>=107)) ].reset_index(drop=True)
len(wind)
x='0920251A'
int(x[:4])>=107
near=(df.id.map(lambda x:int(x[:3])>=107))
wind=df.loc[(df.name.map(lambda x:'風力' in x)) & (df.prog!='審查中') & near ].reset_index(drop=True)
len(wind)
wind
wind.set_index('cat').to_csv(wind5yrpas.csv)
wind.set_index('cat').to_csv('wind5yrpas.csv')
a=df.loc[df.name.map(lambda x:'風' in x)].reset_index(drop=True)
len(a)
a
a=df.loc[df.name.map(lambda x:'風' in x and '風力' not in x)].reset_index(drop=True)
len(a)
a
wind=df.loc[(df.name.map(lambda x:'風力' in x or '風電' in x)) & (df.prog!='審查中') & near ].reset_index(drop=True)
len(wind)
!lst
ls -lh *csv
!wc wind5yrpas.csv
B27=df.loc[df.cat=='B27'].reset_index(drop=True)
len(B27]
len(B27)
B27
B27=df.loc[(df.cat=='B27') & (df.name.map(lambda x:'廠' in x))].reset_index(drop=True)
len(B27)
B27
B27=df.loc[(df.cat=='B27') & (df.name.map(lambda x:'廠' in x and '風力' not in x)) & near].reset_index(drop=True)
len(B27)
B27
B27.set_index('cat').to_csv('B27.csv')
len(wind)
B02=df.loc[(df.cat=='B02') & near].reset_index(drop=True)
len(B02)
B62
B02
pc
[i for i in pc if '捷' in pc[i]]
B02.set_index('cat').to_csv('B02.csv')
B05=df.loc[(df.cat=='B05') & near].reset_index(drop=True)
B02
B02=df.loc[(df.cat=='B02') & (df.prog!='審查中') & near].reset_index(drop=True)
len(B02)
B02.set_index('cat').to_csv('B02.csv')
B05=df.loc[(df.cat=='B05') & (df.prog!='審查中') & near].reset_index(drop=True)
len(B05)
B05
51+9+147+9
51+9+14+9
!lst
!lst "*csv"
B05.set_index('cat').to_csv('B05.csv')
B02.cat=[i+'_'+pc[i] for i in B02.cat]
B02.head()
B02.set_index('cat').to_csv('B02.csv')
B05.cat=[i+'_'+pc[i] for i in B05.cat]
B05.set_index('cat').to_csv('B05.csv')
B27.cat=[i+'_'+pc[i] for i in B27.cat]
B27.head()
wind.cat=[i+'_'+pc[i] for i in wind.cat]
wind.set_index('cat').to_csv('wind5yrpas.csv')
%history -f cat4.py
ls
!ls all*html|wc
!ls all*html>fnames.txt
ls *py
ls -lrth *.py
with open("fnames.txt",'r') as f:
    fnames=[i.strip('\n') for i in f]
df0=pd.DataFrame({})
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
import pandas as pd
from bs4 import BeautifulSoup
with open("fnames.txt",'r') as f:
    fnames=[i.strip('\n') for i in f]
df0=pd.DataFrame({})
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
len(df0)
df0.head()
col
df0.columns=col
df0=df0.sort_values(by="id", ascending=False).reset_index(drop=True)
df0=df0.drop_duplicates().reset_index(drop=True)
len(df0)
st=set(df0.name)-set(df.name)
len(st)
list(st)[:30]
df0.loc[df0.name==list(st)[0]]
n='士林電機廠土地使用變更整體開發計畫環境影響說明書'
df.loc[df.name==n]
len(df)
[i for i in pc if '樓' in pc[i]]
B24=df.loc[df.cat.map(lambda x:x[:3]=='B24')]
B24.loc[B24.name==n]
a=df0.loc[df0.name.map(lambda x:'電廠' in x)]
len(a)
a
nam_cat={i:j for i,j in zip(df.name,df.cat)}
len(st)
len(df0)
a=df0.loc[df0.name.map(lambda x:x not in st),"name"]
a.head()
a.index[:5]
df0[a.index]['cat']=[nam_cat[i] for i in list(a)]
df0.loc[a.index,'cat']=[nam_cat[i] for i in list(a)]
df0.head()
df0.head(20)
a=df0.loc[(df0.name.map(lambda x:x not in st)) & (df0.name.map(lambda x:'電廠' in x))]
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'電廠' in x))]
len(a)
a
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'發電廠' in x))]
len(a)
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'電廠' in x))]
a.loc[a.name.map(lambda x:'發' not in x)]
len(a.loc[a.name.map(lambda x:'發' not in x)])
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'電廠' in x and ' 和平水泥廠計畫' not in x))]
len(a)
len(a.loc[a.name.map(lambda x:'發' not in x)])
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'電廠' in x and '和平水泥廠計畫' not in x))]
len(a)
df0.loc[a.index,'cat']='B27'
a.head()
df0.head(30)
'大中部離岸風力發電計畫環境影響說明書' in st
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'風力' in x))]
len(a)
a
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'風力' in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
a
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'風力' in x and '工業區' not in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
a
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'風力' in x and '工業' not in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
a
list(a.name)[:40]
list(a.name)[40:]
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'風力' in x and '工業' not in x and '台中港區' not in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
df0.loc[a.index,'cat']='B27'
len(df0.loc[(df0.name.map(lambda x:x in st)) & (df0.cat.map(lambda x:x[0]!='B'))])
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.cat.map(lambda x:x[0]!='B'))]
a.head()
a.tail()
len(df0),len(df)
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'捷運' in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
list(a.name)[:40]
notMRT=['富邦人壽高雄捷運凹子底站旁商業區開發案環境影響說明書','冠德建設捷運新莊線菜寮站(捷四)聯合開發案(4、5 樓變更使用)環境影響說明書變更內容對照表-停止營運期間環境監測']
list(a.name)[40:80]
notMRT+=['冠德建設捷運新莊線台(捷二)聯合開發案(3、4 樓變更使用)環境影響說明書第2次變更內容對照表－停止環境監測','冠德建設捷運新莊線菜寮站(捷二)聯合開發案(3、4 樓變更使用)環境影響說明書變更內容對照表',]
notMRT
list(a.name)[80:120]
len(a)
list(a.name)[120:]
notMRT
a=df0.loc[(df0.name.map(lambda x:x in st)) & (df0.name.map(lambda x:'捷運' in x and '富邦人壽' not in x and '冠德建設' not in x)) & (df0.cat.map(lambda x:x[0]!='B'))]
len(a)
[i for i in pc if '捷' in pc[i]]
df0.loc[a.index,'cat']='B05'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'園區' in x ))]
len(a)
list(a.name)[:40]
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'科學園區' in x ))]
len(a)
list(a.name)[:40]
df0.loc[a.index,'cat']='B02'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'產業園區' in x ))]
list(a.name)[:40]
len(a)
df0.loc[a.index,'cat']='B02'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'園區' in x ))]
a.head(40)
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'工業園區' in x ))]
len(a)
df0.loc[a.index,'cat']='B02'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'園區' in x ))]
a.head(40)
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'科技園區' in x ))]
len(a)
df0.loc[a.index,'cat']='B02'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'智慧園區' in x ))]
len(a)
df0.loc[a.index,'cat']='B02'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'園區' in x ))]
list(a.name)[:40]
yq=['創新園區','軟體園區','科技商務園區','林口園區','醫學園區']
%history -f yq.py
!tail -n20 yq.py
for i in yq:
    a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:i in x))]
    df0.loc[a.index,'cat']='B02'
len(df0.loc[df0.cat.map(lambda x:x[0]!='B')])
a=df0.loc[df0.cat.map(lambda x:x[0]!='B')]
a.head(40)
list(a.name)[40:80]
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'電力' in x ))]
len(a)
a
df0.loc[a.index,'cat']='B27'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'科學城' in x ))]
len(a)
a
yq=['創新園區','軟體園區','科技商務園區','林口園區','醫學園區','科學城']
for i in yq:
    a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:i in x))]
    df0.loc[a.index,'cat']='B02'
a=df0.loc[df0.cat.map(lambda x:x[0]!='B')]
list(a.name)[:40]
yq=['創新園區','軟體園區','科技商務園區','林口園區','醫學園區','科學城','工業區','工商綜合專用區','研發科技中心']
for i in yq:
    a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:i in x))]
    df0.loc[a.index,'cat']='B02'
a=df0.loc[df0.cat.map(lambda x:x[0]!='B')]
list(a.name)[:40]
list(a.name)[40:80]
list(a.name)[80:120]
list(a.name)[120:160]
bs=['B02','B05','B27']
a=df0.loc[df0.cat.map(lambda x:x in bs)]
len(a)
!grep near *py
len(df0.loc[(df0.cat.map(lambda x:x in bs)) & (df.prog!='審查中') & near])
near0=(df0.id.map(lambda x:int(x[:3])>=107))
a=df0.loc[(df0.cat.map(lambda x:x in bs)) & (df0.prog!='審查中') & near0])
a=df0.loc[(df0.cat.map(lambda x:x in bs)) & (df0.prog!='審查中') & near0]
len(a)
pwd
ls *csv
a.head()
!grep pc\[ *py
!grep pc *py
!grep nam_cat *py
a.head()
nam_cat0={i:j for i,j in zip(a.name,a.cat)}
a.cat=[i+'_'+pc[i] for i in a.cat]
a.head()
a=df0.loc[(df0.cat.map(lambda x:x in bs)) & (df0.prog!='審查中') & near0]
a=df0.loc[(df0.cat.map(lambda x:x in bs)) & (df0.prog!='審查中') & near0].reset_index(drop=True)
a.cat=[i+'_'+pc[i] for i in a.cat]
a.head()
len(a)
a.set_index('cat').to_csv('cat4all.csv')
ls *csv
!cat B02.csv B05.csv B27.csv wind5yrpas.csv>cat4.csv
cat4=read_csv('cat4.csv')
set(cat4.name)-set(a.name)
s=list(set(cat4.name)-set(a.name))[1:]
a=df0.loc[df0.name.map(lambda x:x in s)]
a
a=df.loc[df.name.map(lambda x:x in s)]
a
s
s=list(set(cat4.name)-set(a.name))
a=df.loc[df.name.map(lambda x:x in s)]
a
s
!lst
a=read_csv('cat4all.csv')
s=list(set(cat4.name)-set(a.name))[:]
s
b=df.loc[df.name.map(lambda x:x in s)]
b
!grep df0 *py
combined_df = pd.concat([a, b], ignore_index=True)
len(combined_df)
len(a)
a=combined_df
a.set_index('cat').to_csv('cat4all.csv')
!ls *csv
pwd
ls -lrth *csv
!wc cat.csv
b
combined_df = pd.concat([df0, b], ignore_index=True)
b0=df0.loc[df0.name.map(lambda x:x in s)]
b0
s
b
lst
!lst
ls -lrth *csv
df0=combined_df
df0=df0.drop_duplicates().reset_index(drop=True)
len(df0)
!lst
df0.set_index('cat').to_csv('all_pages.csv')
%history -f all_pages.py
len(a)
list(a.name)[:40]
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'捷' in x ))]
len(a)
a
a=df0.loc[(df0.cat.map(lambda x:x[0]=='B')) & (df0.name.map(lambda x:'捷' in x ))]
a.head(40)
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'輕軌' in x ))]
a
df0.loc[a.index,'cat']='B05'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'軌' in x ))]
a
[i for i in pc if '鐵' in pc[i]]
pc['B04']
df0.loc[a.index,'cat']='B04'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'鐵路' in x ))]
len(a)
a
[i for i in pc if '高速' in pc[i]]
df0.loc[a.index,'cat']='B04'
df0.set_index('cat').to_csv('all_pages.csv')
len(df0.loc[df0.cat=='B04'])
len(df0.loc[df0.cat=='B05'])
len(df0.loc[df0.cat=='B02'])
len(df0.loc[df0.cat=='B01'])
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'六輕' in x ))]
len(a)
a
a=df0.loc[(df0.name.map(lambda x:'六輕' in x ))]
a.head(40)
list(a.name)[40:80]
a=df0.loc[(df0.cat.map(lambda x:x[0]=='B')) & (df0.name.map(lambda x:'六輕' in x ))]
len(a)
a
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'六輕' in x ))]
df0.loc[a.index,'cat']='B01'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'三輕' in x ))]
len(a)
a
df0.loc[a.index,'cat']='B01'
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'二輕' in x ))]
len(a)
a=df0.loc[(df0.cat.map(lambda x:x[0]!='B')) & (df0.name.map(lambda x:'五輕' in x ))]
len(a)
df0.set_index('cat').to_csv('all_pages.csv')
!lst
%history -f all_pages.py
!wc all_pages.csv
!wc cat4all.csv
cp cat4all.csv ../works/
ls -lrth *py
cat rd_allPages.py
7500*10/60/24
26/(78+28+6)
26/(78+28+6)*7.5
ls -lrth *py
!cat rd_allPages.py
ls -lrth *py
!vi cat4.py
!cat rd_eia.py
ls -lrth *py
!cat rd_eia.py
!lst
ls -lrth *py
cd ../works/
ls *py
ls -lrth *py
cd ../eia_htmls
ls -lrth *py
cat get_html.py
ls -lrth *py
%history -f all_pages.py
