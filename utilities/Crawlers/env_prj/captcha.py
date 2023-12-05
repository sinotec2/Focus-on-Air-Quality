from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2, os, time, glob
import pytesseract
from PIL import Image
from pandas import *

def get_captcha(i):

    # 打开截图文件
    screenshot_path = "./screenshot.png"
    screenshot = Image.open(screenshot_path)

    # 设置裁剪区域的位置和大小
    x = 100  # 距左边界的像素
    y = 750  # 距顶部的像素
    w = 80  # 宽度
    h = 50  # 高度
    
    x = 200  # 距左边界的像素
    y = 1500  # 距顶部的像素
    w = 150  # 宽度
    h = 100  # 高度
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

df0=read_csv('df0.csv')
df0=df0.loc[df0.yr_mg>=110].reset_index(drop=True)

# 创建 Chrome 驱动器
driver = webdriver.Firefox()
source_directory="/Users/kuang/Downloads"

for i in range(len(df0)):
    # 打开网页
    proj_id=df0.proj_id[i]
    cat_nam=df0.cat_nam[i]
    title=df0.title[i]
    group_id=df0.group_id[i]
    target_directory="/nas2/ses_pub/EPAReports/"+group_id+"_"+cat_nam
    os.makedirs(os.path.expanduser(target_directory))

    url = "https://epq.moenv.gov.tw/ProjectDoc/FileDownload?proj_id="+proj_id+"&group_id="+group_id

    i=0
    while i<10:
        i+=1
        driver.get(url)
        driver.save_screenshot("./screenshot.png")
        CaptchaCode=get_captcha(i)
        if len(CaptchaCode)!=4:continue
        if len(set(list(CaptchaCode))-set(list('/?,.!@#$%^&*()|')+['\n']+["'"]+['"'])) != len(CaptchaCode):continue
        # 输入验证码（如果需要）
        captcha_input = driver.find_element(By.ID, "CaptchaCode")
        print(i,CaptchaCode)
        captcha_input.send_keys(CaptchaCode)
        time.sleep(3)
        # 点击 "我同意"
        agree_button = driver.find_element(By.XPATH, "//input[@value='我同意']")
        agree_button.click()
        wait = WebDriverWait(driver, 10)
        try:
            ok_button = driver.find_element(By.XPATH, "//button[text()='OK']")
            # 点击 OK 按钮
            ok_button.click()
            continue
        except:
            pdf_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.pdf"))
            sfile=os.path.join(os.path.expanduser(source_directory), pdf_files[0])
            tfile=os.path.join(os.path.expanduser(target_directory), proj_id+"_"+title+".pdf")
            os.system("mv "+sfile+" "+tfile)
            break
    # 关闭浏览器
driver.quit()
