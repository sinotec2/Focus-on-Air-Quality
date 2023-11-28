#!/home/kuang/.conda/envs/py39/bin/python
import pandas as pd
import os, sys, time, random, glob, shutil
import requests

'''
usage: get_eia.py B01 6 60 (kind of project, start and end of sequences)
'''

df=pd.read_csv(sys.argv[1]+'.csv')
df=df.loc[df.cat!='cat'].reset_index(drop=True)
col=list(df.columns[:])
# 创建一个 Chrome 浏览器实例

source_directory = "." #"/home/kuang/Downloads"
iend={'C':14,'A':31}
ib,ie=[int(sys.argv[i]) for i in [2,3]]
for i in range(ib,ie): #range(5,len(df)):
    id=df['id'][i]
    cat=df['cat'][i]
    nam=df['name'][i]
    target_directory = "/nas2/sespub/epa_reports/"+cat+'/'+id+'_'+nam
    url_root='https://eiadoc.moenv.gov.tw/eiaweb/DownloadFiles.ashx?shcode='+id+'&sFileName='
    if not os.path.exists(os.path.expanduser(target_directory)):
        os.makedirs(os.path.expanduser(target_directory))
    for ac in 'CA':
        pdf_files=[ac+'{:02d}'.format(i)+'.PDF' for i in range(1,iend[ac])]
        urls = [url_root+p for p in pdf_files] # 循环遍历 URL 列表并下载文件
        for url in urls:
            pdf_file=url[-7:]
            if os.path.exists(os.path.join(os.path.expanduser(target_directory), pdf_file)):continue
            response = requests.get(url)
            if response.headers['Content-Type']=='application/download':
                with open(pdf_file, "wb") as f:
                    f.write(response.content)
                # 关闭浏览器
                # 生成5到20之间的随机秒数
                print(url)
                time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
            else:
                #print('file:'+id+url[-7:]+'not exist')
                if ac=='C':
                    if pdf_file!='C01.PDF':continue #try appendix files
                    url=url.replace(pdf_file,'000.PDF')
                    pdf_file=url[-7:]
                    if os.path.exists(os.path.join(os.path.expanduser(target_directory), pdf_file)):break
                    response = requests.get(url)
                    if response.headers['Content-Type']=='application/download':
                        with open(pdf_file, "wb") as f:
                            f.write(response.content)
                        # 关闭浏览器
                        # 生成5到20之间的随机秒数
                        print(url)
                    time.sleep(random.uniform(5, 20))  # 等待加载完成，根据需要调整等待时间
                    break #no more trying
                break #last appendix file
    pdf_files = glob.glob(os.path.join(os.path.expanduser(source_directory), "*.PDF"))
    if len(pdf_files)>0:
        for pdf_file in pdf_files:
            shutil.move(pdf_file, os.path.join(os.path.expanduser(target_directory), os.path.basename(pdf_file)))
            #print(f"移动文件 {pdf_file} 到 {target_directory}")
