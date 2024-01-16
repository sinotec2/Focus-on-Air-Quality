from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_wait(pth,itm):
    # 点击元素
    element = driver.find_element(pth,itm)
    element.click()
# 等待直到页面更新
    wait = WebDriverWait(driver, 10)  # 设置至少等待时间
    wait.until(EC.staleness_of(element))  # 等待直到元素变为陈旧，即页面更新
    return 0
    
driver = webdriver.Firefox()
driver.get("https://eiadoc.epa.gov.tw/eiaweb/")

# 选择计划类别为"工厂的设立"
select = Select(driver.find_element(By.ID,"cphContent_dlFtrDECAL"))
select.select_by_value("B02")

# 点击查询按钮
driver.find_element(By.ID,"cphContent_lnkFtrAbstract").click()
time.sleep(10)

# 保存末頁结果
result=click_wait(">")

fname='B02_page-1.html'
with open(fname, "w") as f:
    f.write(driver.page_source)

from bs4 import BeautifulSoup
import pandas as pd

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
df = pd.DataFrame(data, columns=header)
last=int(df.iloc[-1,0])
npage=last//10+1
if last%10==0:npage=npage-1

# return to page 1 
# 保存第一页结果
result=click_wait("<")

fnames=['B02_page'+str(i)+'.html' for i in range(0,npage)]
with open(fnames[1], "w") as f:
    f.write(driver.page_source)
for i in range(1,npage):
    ii=str(i)
    if (i-1)%5==0:ii="..."
    result=click_wait(ii)
    with open(fnames[i], "w") as f:
        f.write(driver.page_source)   
    time.sleep(10)
