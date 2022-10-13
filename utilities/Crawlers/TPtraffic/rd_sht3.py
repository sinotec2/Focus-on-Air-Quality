from bs4 import BeautifulSoup
from pandas import *
from pypinyin import pinyin, lazy_pinyin
import itertools

def FindLastABC(end):
    for last in xrange(end,-1,-1):
        if a[last] in ABC:break
    return last
with open('sss.txt') as ftext:
    s=[line.split('\n')[0] for line in ftext]
ABC=['A','B','C','D','E','F']
year,time,dirn,name,road=[],[],[],[],[]
nam_v=['Lvolume','Lratio','Mvolume','Mratio','Svolume','Sratio','PCU','PHF']
v=[]
for iv in xrange(8):            
    v.append([])
note=['zhanming','zhan','shixiangshu'] #站名、站、時相數
for fname in s:
    yr=int(fname.split('_')[1])+90+1911
    if fname.split('.')[1]=='htm':
        fn=open(fname,'r')
        soup = BeautifulSoup(fn,'html.parser')
        td=soup.find_all('td')
        a=[str(td[i]).split('>')[1].split('<')[0] for i in xrange(len(td))]
    else:
        with open(fname) as ftext:
            ln=[line.split() for line in ftext]
            if fname=='sht3_12_SI114.txt':ln.remove(ln[0])
            if fname!='sht3_13_NI028.txt':
                lnn=[ln[-1-i] for i in xrange(len(ln))]
                lna=[]
                for i in xrange(len(lnn)):
                    lna.append([lnn[i][-1-j] for j in xrange(len(lnn[i]))])
                ln=[]
                for i in xrange(len(lna)):
                    ln1=[]
                    for j in xrange(len(lna[i])):
                        string=lna[i][j]
                        sa=''
                        ibeg=len(string)-3
                        if ibeg >=0:
                            while True:
                                try:
                                    string[ibeg:ibeg+3].decode('utf-8')
                                except UnicodeError:
                                    sa=sa+string[ibeg+2]
                                    ibeg=ibeg-1
                                    if ibeg<0:break
                                else:
                                    if len(string[ibeg:ibeg+3].decode('utf-8'))==1:
                                        k=ibeg
                                        sa=sa+string[k]+string[k+1]+string[k+2]
                                    else:
                                        for k in xrange(ibeg+2,ibeg-1,-1):
                                            sa=sa+string[k] 
                                        if 0<ibeg<3:
                                            for k in xrange(ibeg-1,min(-1,ibeg-2),-1):
                                                sa=sa+string[k]
                                    ibeg=ibeg-3
                                    if ibeg<0:break
                        else:
                            for k in xrange(len(string)-1,-1,-1):
                               sa=sa+string[k] 
                        ln1.append(sa)
                    ln.append(ln1)
            a=list(itertools.chain(*ln))
    b=[]
    for i in xrange(100):
        cha=a[i]
        if type(cha)==float:
            b.append(cha)
            continue
        if len(cha)<2:
            b.append(cha)
            continue
        ss=lazy_pinyin(cha.decode('utf8'))
        sss=''
        for j in ss:
            if j.isalnum():sss=sss+j
        b.append(sss)
    for nt in note:
        try:
            b_note=b.index(nt)
        except:
            road_s='not_found'
        else:
            road_s=b[b_note+1]
            break
    last=FindLastABC(len(a)-1)
    A_last=a[last]
    lastend=len(a)
    if fname =='sht3_7_SI061.htm':A_last='D'
    ampm='pm'
    for chr in xrange(12): #repeat for A~F twice
        if fname == 'sht3_9_SI029.htm' and a[last]=='B': 
            lastend=last
            last=FindLastABC(last-1)
            if a[last] == A_last and ampm=='am':break
            if a[last] == A_last and ampm=='pm':ampm='am'
            continue
        tab=[]
        for j in xrange(last,lastend):
            try:
                tt=float(a[j])
            except:
                if len(a[j])>1 and a[j][-1]=='%':
                    tab.append(float(a[j][:-1])/100)
            else:
                tab.append(tt)
        year.append(yr)
        time.append(ampm)
        dirn.append(a[last])
        name.append((fname.split('_')[2]).split('.')[0])
        road.append(road_s)
        if len(tab) <8:
            for iv in xrange(8-len(tab)):
                tab.insert(0,0.0)
        len_tab=len(tab)
        for gt1 in xrange(1,10):
            tt=tab[len(tab)-gt1]
            if 0< tt and tt < 1:
                len_tab=len_tab-gt1+1
                break
        if tab[len_tab-1] > 1 or tab[len_tab-1]==0.: tab=[0.0 for x in tab]            
        for iv in xrange(len_tab-8,len_tab):            
            v[iv-(len_tab-8)].append(tab[iv])
        lastend=last
        last=FindLastABC(last-1)
        if a[last] == A_last and ampm=='am':break
        if a[last] == A_last and ampm=='pm':
            ampm='am'
d={'year':year,'time':time,'dirn':dirn,'name':name,'road':road}
for iv in xrange(8):
    d.update({nam_v[iv]:v[iv]})
df=DataFrame(d)
for i in xrange(len(df)): #每列確認橫向綜合非為0，如果各個車種流量皆為0，則刪除該筆紀錄。
    sm=0.
    for j in nam_v:
        try:
            tt=float(df.loc[i,j])
        except:
            continue
        else:
            if tt>0:sm=sm+tt
    if sm==0.: df=df.drop(i)
cols=['year','time','dirn','name','road']+nam_v
df[cols].set_index('year').to_csv('sht3_df.csv')            
