from bs4 import BeautifulSoup
fn=open('sheet001.htm','r')
soup = BeautifulSoup(fn,'html.parser')
fn=open('inter_nam.txt','w')
for i in soup.find_all('a'):
    fn.write(i['href'].split('/')[2].split('.')[0]+'\n')
fn.close()
