
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def click_wait(pth,itm):
    # 点击元素
    element = driver.find_element(pth,itm)
    element.click()
# 等待直到页面更新
    wait = WebDriverWait(driver, 10)  # 设置至少等待时间
    wait.until(EC.staleness_of(element))  # 等待直到元素变为陈旧，即页面更新
    return 0
from selenium.webdriver.firefox.options import Options
firefox_options = Options()
firefox_options.add_argument("--headless")  # 启用无头模式

wait_time = 10
for cat in ['{:02d}'.format(i) for i in range(1,2)]:
    driver = webdriver.Firefox(options=firefox_options)
    driver.get("https://epq.moenv.gov.tw/Query/ResultList?Classification="+cat+"#")


    # 创建 WebDriverWait 实例
    wait = WebDriverWait(driver, wait_time)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//select[@name="DataTables_Table_0_length"]')))

    # 选择计划类别为"工厂的设立"
    select = Select(driver.find_element(By.XPATH, '//select[@name="DataTables_Table_0_length"]'))
    select.select_by_value('50')
    fnames=['p'+cat+'_'+str(1)+'.html' ]
    with open(fnames[0], "w") as f:
        f.write(driver.page_source)
    html_content=driver.page_source
    #使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找包含页码的元素
    page_element = soup.find_all('li', {'class': 'paginate_button'}) # page-item '

    # 提取页码文本
    npage = int(page_element[-2].text.strip())
    fnames+=['p'+cat+'_'+str(i)+'.html' for i in range(2,npage+1)]
    for i in range(2,npage+1):
        pth=By.LINK_TEXT;ii=str(i)
        result=click_wait(pth,ii)
        if os.path.exists(fnames[i-1]):continue
        with open(fnames[i-1], "w") as f:
            f.write(driver.page_source)   
        time.sleep(10)    
    driver.quit()
