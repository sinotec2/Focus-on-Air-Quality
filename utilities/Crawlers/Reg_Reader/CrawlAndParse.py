```python
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import json

# 您提供的HTML内容
html_content = """
<div class="col-data"><div class="law-article">
<div class="line-0000 show-number">前條應削減排放量之公私場所，於向直轄市、縣（市）主管機關或中央主管機關委託之機關（以下簡稱審核機關）提出固定污染源操作許可證之展延申請時，應依下列規定辦理：</div><div class="line-0004">一、既存固定污染源之製程符合附表所列應符合條件者，應檢具最近一年檢測報告或其他足以證明符合附表所列之排放管道濃度或削減率之證明文件，併同固定污染源操作許可證展延申請所需檢附資料一併辦理。</div><div class="line-0004">二、既存固定污染源之製程未能符合附表所列應符合條件，需增加空氣污染防制設施者，應檢具其空氣污染物防制設施種類、構造、效能、流程、設計圖說、設置經費及進度之空氣污染防制計畫，向審核機關申請核定工程改善所需期限，改善期限不得逾中華民國一百十四年六月三十日。</div><div class="line-0000 show-number">審核機關受理前項第二款核定工程改善所需期限之申請，屬專責處理一般廢棄物之廢棄物焚化處理程序空氣污染防制計畫，經公私場所報請審核機關核准者，其改善期限不受前項第二款限制。</div></div>
</div>
"""


href="https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=O0020126"
title="a"+'.html'
driver = webdriver.Firefox()
driver.get(href)

with open(title, "w") as f:
    f.write(driver.page_source)

from bs4 import BeautifulSoup
import pandas as pd
with open(title,'r') as html:
#使用Beautiful Soup解析HTML
    soup = BeautifulSoup(html, 'html.parser')
LawName = soup.find('a', {'id': 'hlLawName'}).getText()
LawDate = soup.find('tr',{'id': 'trLNODate'}).getText().split('\n')[2]

article=soup.find_all('div', {'class': 'law-article'})

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 初始化JSON数据
json_data = {}
current_category = None
current_counter = 0

# 遍历HTML内容
for div in soup.find_all('div', class_=["line-0000 show-number", "line-0004"]):
    if "line-0000" in div["class"]:
        # 父层级
        current_counter += 1
        current_category = str(current_counter)
        json_data[current_category] = {'text': div.text}
    elif "line-0004" in div["class"]:
        # 子层级
        sub_category = f"{current_category}.{len(json_data[current_category]) - 1}"
        if "children" not in json_data[current_category]:
            json_data[current_category]["children"] = {}
        json_data[current_category]["children"][sub_category] = {'text': div.text}

# 将JSON数据转为字符串
json_str = json.dumps(json_data, ensure_ascii=False, indent=2)

# 输出JSON字符串
print(json_str)
