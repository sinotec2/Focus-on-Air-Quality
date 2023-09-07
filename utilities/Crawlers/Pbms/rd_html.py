#kuang@master ~/Documents/Pbms
#$ cat rd_html.py
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
with open("d.html",'r') as html_doc:
  soup = BeautifulSoup(html_doc, 'html.parser')
#print(soup.prettify())
#i=0
#for link in soup.find_all('a'):
#  print(i,link.get('href'))
#  i+=1
#  if i>10:break
txt=soup.get_text()
txt=txt.replace('(如季報等)','（如季報等）')
txt=txt.replace('(家戶垃圾)','（家戶垃圾）')
txt=txt.replace('(Rupture Disk)','（Rupture Disk）')
txt=txt.replace('(逾期)','（逾期）')
txt=txt.replace('(W值)','（W值）')
i1=txt.split('(')
i1=i1[1:]
ID=[i.split(')')[0] for i in i1]
TTL=[i.split(')')[1] for i in i1]
HREF=[]
i=0
for link in soup.find_all('a'):
  i+=1
  if i%2 == 1:continue
  HREF.append(link.get('href'))
n=len(HREF)
for i in range(n):
    TTL[i]=TTL[i].replace('（','(')
    TTL[i]=TTL[i].replace('）',')')
    TTL[i]=TTL[i].replace('/','_')
id_nam='ContentPlaceHolder1_DataList1_maskname_'
id_tim='ContentPlaceHolder1_DataList1_lblPostTime_'
id_con='ContentPlaceHolder1_DataList1_Label4_'
br='<br>'
nx='\n'
pbm_tit='== 問題說明 =='
evl_tit='== 審查 =='
sol_tit='== 處理對策說明 =='
ref_tit='== Reference =='
a1='問題說明';a2='處理對策';a3='：';a4='  '
for i in range(n):
  fname=TTL[i]+'.html'
  try:
    with open(fname,'r') as html_doc:
      soup = BeautifulSoup(html_doc, 'html.parser')
  except:
    continue
  names,times,conts=[],[],[]
  for span in soup.find_all('span'):
    if type(span.get('id')) != str:continue
    if span.get('id')[:-1]==id_nam:
      names.append('[['+span.text+']]')
    if span.get('id')[:-1]==id_tim:
      times.append(span.text)
    if span.get('id')[:-1]==id_con:
      text=span.text
      text=text.replace(a1,'').replace(a2,'').replace(a3,'').replace(a4,'')
      for num in range(1,10):
        text=text.replace(str(num)+'.','<br>\n'+str(num)+'.')
        text=text.replace('('+str(num)+')','<br>\n'+'('+str(num)+')')
      conts.append(text+br+nx)
  m=len(names)
  fname=TTL[i]+'.md'
  with open(fname,'w') as txt:
    txt.write(times[0]+names[0]+br+nx)
    txt.write(pbm_tit+nx)
    txt.write(conts[0])
    txt.write(evl_tit+nx)
    for j in range(1,m):
      txt.write('* '+times[j]+names[j]+br+nx)
    txt.write(sol_tit+nx)
    if m <= 2:
      txt.write(conts[1])
    else:
      for j in range(1,m):
        txt.write('=== '+times[j]+' '+names[j]+'==='+nx)
        txt.write(conts[j])
    txt.write(ref_tit+nx)
    txt.write('* ['+HREF[i]+' sinotechKM 編號:'+ID[i]+']')
