from bs4 import BeautifulSoup
import requests
import os, json
with open('href_n.txt', 'r') as f:
    html_contents=[i for i in f]
for html_content in html_contents[:]:
    soup = BeautifulSoup(html_content, 'html.parser')
    # ▒~N▒▒~O~V <a> ▒~E~C▒|
    a_tag = soup.find('a')

    # ▒~O~P▒~O~V URL ▒~R~L▒| ~G▒~X
    url = a_tag['href'].split('&')[0].split('=')[1]
    url="https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode="+url
    title = a_tag['title']
    if not os.path.exists(os.path.join(os.path.expanduser("./"), title+'.html')):
#    response = requests.get(url)
#        f.write(response.content)
#    with open(title+".html", "wb") as f:
        url2=url.replace('?','\\?').replace('=','\\=')
        with open('a.cs','w') as f:
            f.write('url='+url2+'\n/usr/bin/wget -q $url -O '+title+'.html\n')
        os.system('chmod u+x ./a.cs;./a.cs' )
#    driver = webdriver.Firefox()
#    driver.get(url)
#        f.write(driver.page_source)
    with open(title+".html",'r') as html:
#使用Beautiful Soup解析HTML
        soup = BeautifulSoup(html, 'html.parser')
    LawName = soup.find('a', {'id': 'hlLawName'}).getText()
    LawDate = soup.find('tr',{'id': ['trLNODate','trLNNDate']}).getText().split('\n')[2]
    articles = soup.find_all('a', {'href': True, 'name': True})
    result = {'LawName':LawName,'LawDate':LawDate}

    # 遍历每个條
    for article in articles:
        article_name = article.text.strip()
        if ":" in article_name:continue
        article_number = article['name']
        next_element = article.find_next('div', class_='line-0000')
    
        if next_element:
            article_text = next_element.text.strip()
            result[article_name] = article_text
    if len(result)==-0:continue
    with open(title+".json", "w") as f:
        json.dump(result,f)