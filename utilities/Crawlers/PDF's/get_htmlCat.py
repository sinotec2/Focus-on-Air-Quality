from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time,json, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def click_wait(pth,itm):
    # 点击元素
    element = driver.find_element(pth,itm)
    element.click()
# 等待直到页面更新
    wait = WebDriverWait(driver, 10)  # 设置至少等待时间
    wait.until(EC.staleness_of(element))  # 等待直到元素变为陈旧，即页面更新
    return 0
    
driver = webdriver.Chrome()
driver.get("https://eiadoc.epa.gov.tw/eiaweb/")
with open("/Users/kuang/MyPrograms/rd_eia/proj_class.json") as f:
    bb=json.load(f)
for cat in list(bb)[:]:
    
    # 选择计划类别
    select = Select(driver.find_element(By.ID,"cphContent_dlFtrDECAL"))
    select.select_by_value(cat)

    # 点击查询按钮
    driver.find_element(By.ID,"cphContent_lnkFtrAbstract").click()
    time.sleep(10)    
    try:
        # 保存末頁结果
        result=click_wait(By.LINK_TEXT,">")

        fname=cat+'_page-1.html'
        with open(fname, "w") as f:
            f.write(driver.page_source)

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
        result=click_wait(By.LINK_TEXT,"<")
    except:
        last=50;npage=5
    # 保存第一页结果
    fnames=[cat+'_page'+str(i)+'.html' for i in range(0,npage)]
    with open(fnames[1], "w") as f:
        f.write(driver.page_source)
    for i in range(2,npage):
        pth=By.LINK_TEXT;ii=str(i)
        if i<=4: #skip the meeting pages selection
            pth=By.XPATH;ii='(//a[text()="'+ii+'"])[2]'
        if (i-1)%5==0:
            if i==6:
                pth=By.LINK_TEXT;ii="..."
            else:
                pth=By.XPATH;ii='(//a[text()="..."])[2]'
        else:
            if os.path.exists(fnames[i]):continue
        result=click_wait(pth,ii)
        if os.path.exists(fnames[i]):continue
        with open(fnames[i], "w") as f:
            f.write(driver.page_source)   
        time.sleep(10)
