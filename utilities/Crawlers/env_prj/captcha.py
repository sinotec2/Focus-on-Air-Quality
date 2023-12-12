from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import cv2, os, time, glob, sys, subprocess
import pytesseract
from PIL import Image
from pandas import *
from selenium.webdriver.firefox.options import Options

def get_captcha(i):

    # 打开截图文件
    screenshot_path = "./screenshot.png"
    screenshot = Image.open(screenshot_path)

    # 设置裁剪区域的位置和大小
    # linux firefox
    x = 100  # 距左边界的像素
    y = 750  # 距顶部的像素
    w = 80  # 宽度
    h = 50  # 高度
# mac Firefox    
#    x = 200  # 距左边界的像素
#    y = 1500  # 距顶部的像素
#    w = 150  # 宽度
#    h = 100  # 高度
    # 裁剪图像
    cropped_image = screenshot.crop((x, y, x + w, y + h))

    # 保存裁剪后的图像
    cropped_image.save("./cropped_image"+str(i)+".png")
    cropped_image=cv2.imread("./cropped_image"+str(i)+".png")
    _, binary_image = cv2.threshold(cropped_image, 128, 255, cv2.THRESH_BINARY)

# 使用 Tesseract 进行 OCR
    CaptchaCode = pytesseract.image_to_string(Image.fromarray(binary_image))
    CaptchaCode=CaptchaCode.replace(' ','').strip('\n')
    print(CaptchaCode,len(CaptchaCode))
    return CaptchaCode

def print_single_line(msg):
    sys.stdout.write('\033[F')  # 光标移动到上一行
    sys.stdout.write('\033[K')  # 清除行
    print(msg)

df0=read_csv('df0.csv')
df0=df0.loc[df0.yr_mg>=100].reset_index(drop=True)

# 创建 Chrome 驱动器
home=subprocess.check_output('echo $HOME',shell=True).decode('utf8').strip('\n')
source_directory=home+"/Downloads"

#firefox_options = Options()
#firefox_options.add_argument("--headless")  
options = webdriver.FirefoxOptions()

# 禁用內建的 PDF 開啟器
options.set_preference("pdfjs.disabled", True)

# 禁用內建的 PDF 下載器
#options.set_preference("plugin.disable_full_page_plugin_for_types", "application/pdf")
not_found=['111年度雲林縣石化業專用監測車操作維護計畫','111年度土壤及地下水污染調查及查證工作計畫-臺南市',
        '111年度土壤污染評估調查及檢測資料勾稽查核計畫','111年綠島鄉及蘭嶼鄉環境衛生計畫',
        '111年度產品碳足跡資訊揭露與發展雲端審查標示制度專案工作計畫',
           '屏東縣-屏東縣殺蛇溪水質淨化場設計案',
           '110年度嘉義縣固定空氣污染源許可暨揮發性有機物稽查管制計畫',
               "110年度臺東縣營建工程污染管制暨電子e化系統設置計畫",
           "110年度土壤及地下水污染調查及查證工作計畫-雲林縣",
           "110年土壤及地下水相關計畫檢測作業品保監督查核計畫",
           "110年度非農地環境雜草管理計畫__臺北市"
          ]
j=1
for i in range(len(df0)):
    # 打开网页
    proj_id=str(df0.proj_id[i])
    cat_nam=df0.cat_nam[i]
    title=df0.title[i].replace(' ','').replace('/','-').replace('\t','') #replace('(','\(').replace(')','\)')
    if title in not_found:continue
    group_id=str(df0.group_id[i])
    target_directory="/nas2/sespub/EPA_PrjReports/"+group_id+"_"+cat_nam
    os.makedirs(os.path.expanduser(target_directory), exist_ok=True)
    tfile=os.path.join(os.path.expanduser(target_directory), proj_id+"_"+title+".pdf")
    if os.path.exists(tfile):continue

    driver = webdriver.Firefox(options=options)
    url = "https://epq.moenv.gov.tw/ProjectDoc/FileDownload?proj_id="+proj_id+"&group_id="+group_id

    ii=0
    pdf_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.pdf"))
    if len(pdf_files)>1:
        sfile=os.path.join(os.path.expanduser(source_directory), '*.pdf')
        os.system("rm "+sfile)

    while ii<10:
        ii+=1
        driver.get(url)
        driver.save_screenshot("./screenshot.png")
        CaptchaCode=get_captcha(ii)
        if len(CaptchaCode)!=4:continue
        if len(set(list(CaptchaCode))-set(list('/?,.!@#$%^&*()[]|')+['\n']+["'"]+['"']+["`"])) != len(CaptchaCode):continue
        # 输入验证码（如果需要）
        captcha_input = driver.find_element(By.ID, "CaptchaCode")
        print_single_line('{:d} '.format(ii)+CaptchaCode+title)
        captcha_input.send_keys(CaptchaCode)
        time.sleep(1)
        # 点击 "我同意"
        agree_button = driver.find_element(By.XPATH, "//input[@value='我同意']")
        agree_button.click()
        time.sleep(1) #wait = WebDriverWait(driver, 30)
        try:
            WebDriverWait(driver, 1).until(
            EC.text_to_be_present_in_element((By.XPATH, "//div[@id='swal2-content']"), "本文件系統調整中，暫不提供下載；請聯絡業務單位")
            )
            # 如果找到元素，表示弹窗出现，处理你的逻辑
            break
        except TimeoutException:
            # 如果等待时间超过1秒，或者找不到元素，表示弹窗未出现，继续执行后续逻辑        
            try:
                ok_button = driver.find_element(By.XPATH, "//button[text()='OK']")
                # 点击 OK 按钮
                ok_button.click()
                continue
            except:
                pdf_files=[]
                iii=0
                while iii<10 and len(pdf_files)==0:
                    time.sleep(10) #wait = WebDriverWait(driver, 30)
                    pdf_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.pdf"))
                    iii+=1
                if len(pdf_files)==0:
                    driver.quit()    # 关闭浏览器
                    break
                pdf_files[0]=pdf_files[0].replace('(','\(').replace(')','\)').replace(' ','\ ')
                tfile=tfile.replace('(','\(').replace(')','\)').replace(' ','\ ')
                sfile=os.path.join(os.path.expanduser(source_directory), pdf_files[0])
                os.system("mv "+sfile+" "+tfile)
                if len(pdf_files)>1:
                    sfile=os.path.join(os.path.expanduser(source_directory), '*.pdf')
                    os.system("rm "+sfile)
                driver.quit()    # 关闭浏览器
                break
    # 判断 WebDriver 是否存在并关闭
    if 'driver' in locals() or 'driver' in globals():
        try:
            driver.quit()
            print("Selenium WebDriver 已关闭。")
        except:
            print("关闭 Selenium WebDriver 时出现错误。")
        else:
            print("Selenium WebDriver 未找到。")

#    if j==1:break