import PyPDF2
import sys 
def dots(l):
    tdic={'':'.','(':')','（':'）'}
    for p in ['','(','(']:
        for i in range(1,11):
            a=p+str(i)+tdic[p]
            n=len(a)
            if l[:n]==a:return True
    return False    
def CNnum(l):
    num=['一','二','三','四','五','六','七','八','九','十',]
    tdic={'':'、','(':')','（':'）'}
    for p in ['','(','(']:
        for i in num:
            a=p+i+tdic[p]
            n=len(a)
            if l[:n]==a:return True
    return False
def ENnum(l):
    num='ABCDEFGHabcdefgh'
    tdic={'':['.','、'],'(':')','（':'）'}
    for p in ['','(']:
        for i in num:
            t=tdic[p]
            if type(t)==list:
                for tt in t:                    
                    a=p+i+tt
                    n=len(a)
                    if l[:n]==a:return True
            else:
                a=p+i+t
                n=len(a)
                if l[:n]==a:return True
    return False
# creating a pdf file object
fnames=[
#"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1020271A) 大潭電廠增建燃氣複循環機組發電計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070401A) 興達電廠燃氣機組更新改建計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070721A) 森霸電力第二期燃氣複循環發電計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1070731A) 台中發電廠新建燃氣機組計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1101051A) 中佳燃氣複循環電廠興建計畫環境影響說明書\C07.pdf",
"D:\E\My Documents\EIAs\電廠\GAS_EIA\(1110461A) 大林發電廠燃氣機組更新改建計畫環境影響說明書\C07.pdf",
]
fname=fnames[int(sys.argv[1])]
pdfFileObj = open(fname, 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)
a=''
i=1
if '7-' not in pdfReader.pages[0].extract_text():i=0
if '7 -' not in pdfReader.pages[0].extract_text():i=0
for pageObj in pdfReader.pages:
    a+=pageObj.extract_text().replace('7-'+str(i),'\n').replace('7 - '+str(i),'\n')
    i+=1
lines=a.split('\n')
outlines=[l.strip().split(':')[0].split('：')[0] for l in lines]
outlines=[l for l in outlines if (dots(l) or CNnum(l) or ENnum(l))  and len(l)<60]# and FloatNotInLine(l)]
outlines=[l for l in outlines if '-' not in l and '所示' not in l]
fname=fname.replace('.pdf','outline.txt')
with open(fname,'w', encoding='utf-8') as f:
    for i in outlines:
        f.write(i+'\n')
    
