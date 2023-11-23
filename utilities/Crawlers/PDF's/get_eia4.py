#!/home/kuang/.conda/envs/py39/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os, sys, time, random, glob, shutil

'''
usage: get_eia.py B01 6 60 (kind of project, start and end of sequences)
'''

df=pd.read_csv(sys.argv[1]+'.csv')
df=df.loc[df.cat!='cat'].reset_index(drop=True)
col=list(df.columns[:])
# 创建一个 Chrome 浏览器实例

source_directory = "." #"/home/kuang/Downloads"
chrome_driver="/home/kuang/.cache/selenium/chromedriver/linux64/119.0.6045.105/chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")  # 启用无头模式
iend={'C':14,'A':31}
ib,ie=[int(sys.argv[i]) for i in [2,3]]
for i in range(ib,ie): #range(5,len(df)):
    driver = webdriver.Chrome(options=chrome_options)
    id=df['id'][i]
    cat=df['cat'][i]
    nam=df['name'][i]
    target_directory = "/nas2/sespub/epa_reports/"+cat+'/'+id+'_'+nam
    url_root='https://eiadoc.epa.gov.tw/eiaweb/DownloadFiles.ashx?shcode='+id+'&sFileName='
    if not os.path.exists(os.path.expanduser(target_directory)):
        os.makedirs(os.path.expanduser(target_directory))
    for ac in 'CA':
        pdf_files=[ac+'{:02d}'.format(i)+'.PDF' for i in range(1,iend[ac])]
        urls = [url_root+p for p in pdf_files] # 循环遍历 URL 列表并下载文件
        for url in urls:
            pdf_file=url[-7:]
            if os.path.exists(os.path.join(os.path.expanduser(target_directory), pdf_file)):continue
            try:
                driver.get(url)
                # 生成5到20之间的随机秒数
                time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
            except:
                #print('file:'+id+url[-7:]+'not exist')
                if ac=='C':
                     if pdf_file=='C01.PDF':
                         url=url.replace(pdf_file,'000.PDF')
                         driver.get(url)
                         time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
                         break #no more trying
                     else:
                         continue #try appendix files
                break #last appendix file
    pdf_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.PDF"))
    if len(pdf_files)>0:
        for pdf_file in pdf_files:
            shutil.move(pdf_file, os.path.join(os.path.expanduser(target_directory), os.path.basename(pdf_file)))
            #print(f"移动文件 {pdf_file} 到 {target_directory}")
    # 关闭浏览器
    driver.quit()
