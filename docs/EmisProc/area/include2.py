
def rd_kinLL():
    from pandas import read_csv
    fname='/home/sespub/teds90_camx/REAS/line/df_kinLL.csv'
    df_kin=read_csv(fname)
    utme=list(df_kin['x97'])
    utmn=list(df_kin['y97'])
    DICT=list(df_kin['D'])
    subX=[44,50,51]
    for i in range(len(DICT)):
        cntyi=int(DICT[i]/100)
        if cntyi in subX:utme[i]=utme[i]-201
    return (utme,utmn,list(df_kin['R']),DICT)

def rd_kin():
    fname='/home/sespub/teds90_camx/REAS/line/LE-loc12.KIN'
    with open(fname) as text_file:
        d=[line.strip('\n').split()[0] for line in text_file]
    d=d[1:]
    cnty=[int(i[0:2]) for i in d]
    DICT=[i[0:4] for i in d]

    utme=[int(i[4:7]) for i in d]
    rd_typ=[int(i[-1]) for i in d]
    utmn=[int(i[7:11]) for i in d]
    subX=[44,50,51]
    for i in range(len(d)):
        if cnty[i] in subX:utme[i]=utme[i]-201
    return (utme,utmn,rd_typ,cnty)

def rd_EM():
    from scipy.io import FortranFile
    import numpy as np
    NVTYP=13;NVEH=NVTYP;NPOL=10;NREC=33012
    fname='/home/sespub/teds90_camx/REAS/line/cl102.bin'
    f=FortranFile(fname, 'r')
    EM=f.read_record(dtype=np.float32)
    f.close()
    EM=np.reshape(EM,[NREC,NPOL,NVEH])
    return (NVTYP,NPOL,NREC,EM)
def rd_BIN(NC,LTYP,N,M):
    from scipy.io import FortranFile
    import numpy as np
    fname='/home/sespub/teds90_camx/REAS/line/102LVOC.BIN'
    f=FortranFile(fname, 'r')
    VOCB=f.read_record(dtype=np.float32)
    f.close()
    VOCB=np.reshape(VOCB,[NC,LTYP,N,M])
    VOCB[:,0,:,:]=0.
    return VOCB
 
def rd_hwcsv():
    from pandas import read_csv 
    fname='105_LINE_HW.csv'
    df_t=read_csv(fname)
    df_t['DICT']=[int(i/100) for i in list(df_t['DICT'])]
    s1=list(set(df_t['DICT']))
    s1.sort()
    sdf2csv={x:y for x,y in zip(s1,s1)}
    sdf2csv.update({36:17,41:21,42:2})
    return (df_t,sdf2csv)
def rd_cems():
    from pandas import read_csv 
    fname='105_point_cems.csv'
    df_t=read_csv(fname)
    df_t['CP_NO']=[i+j for i,j in zip(list(df_t['C_NO']),list(df_t['NO_S']))]
    return (df_t)
def get_jjjhh():
    from include1 import get_beg_end,cal2jul,date_to_jd,jd_to_date
    import numpy as np
    beg,end=get_beg_end()
    Jbeg,Jend=cal2jul(beg),cal2jul(end)
    print (Jbeg,Jend)
    TBeg=Jbeg*100+20
    TEnd=Jend*100+23
    jd0=int(date_to_jd(int(beg/10000),int(beg/100)%100,beg%100))+1
    jd1=int(date_to_jd(int(end/10000),int(end/100)%100,end%100))+1
    juld0,juld1=[],[]
    hour0,hour1=[],[]
    for jd in range(jd0,jd1+1):
        year,mo,da=jd_to_date(jd)
        day=cal2jul(int(year*100*100+mo*100+da))
        for hh in range(24):
            now=day*100+hh
            if now<TBeg:continue
            if now>TEnd:break
            juld0.append(day)
            hour0.append(hh*10000)
            if hh<23:
                juld1.append(day)
                hour1.append((hh+1)*10000)
            else:
                juld1.append(day+1)
                hour1.append(0)
    nt=len(juld0)
    TFLAG=np.zeros(shape=(nt,2))#,dtype=int)
    TFLAG[:,0], TFLAG[:,1] =juld0,hour0
    jjjhh=[str(int(x%100000*100+y/10000)) for x,y in zip(TFLAG[:,0],TFLAG[:,1])]
    jd0=date_to_jd(int(beg/10000),(beg/100%100),(beg%100))
    return (nt,TFLAG,jjjhh,jd0)

def rd_ASnPRnCBM_A():
    from pandas import DataFrame, read_csv
    import subprocess
    ROOT='/'+subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/area/ASSIGN-A.TXT'
    df_asgn=read_csv(fname,header=None,delim_whitespace = True)
    df_asgn.columns=['NSC','PRO_NO']+[str(i) for i in range(len(df_asgn.columns)-2)]
    df_asgn.fillna(0,inplace=True)
    df_asgn.PRO_NO=['{:04d}'.format(int(m)) for m in df_asgn.PRO_NO]
    for i in range(len(df_asgn)):
        nsc=df_asgn.NSC[i]
        if not nsc[-1].isalpha():
            df_asgn.loc[i,'NSC']=nsc.strip()+'b'                
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/area/V_PROFIL.TXT'
    with open(fname) as text_file:
        d=[line[:41] for line in text_file]
    PRO_NO,SPE_NO,WT=[i[:4] for i in d],[int(i[11:14]) for i in d],[float(i[24:30]) for i in d]
    df_prof=DataFrame({'PRO_NO':PRO_NO,'SPE_NO':SPE_NO,'WT':WT})
    NC=20
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/line/CBM.DAT'
    with open(fname) as text_file:
        d=[line.strip('\n') for line in text_file]
    d=d[1:]
    SPE_NO,MW=[int(i[41:44]) for i in d],[float(i[57:63]) for i in d]
    BASE=[[i[63+j*6:63+(j+1)*6] for j in range(NC)] for i in d]
    d=BASE
    for i in range(len(d)):
        ii=d[i]
        for j in range(NC):
            s=ii[j].strip(' ')
            if len(s)==0:
                BASE[i][j]=0.
            else:
                BASE[i][j]=float(s)
    df_cbm=DataFrame({'SPE_NO':SPE_NO,'MW':MW,'BASE':BASE})
    return (df_asgn,df_prof,df_cbm)

def rd_ASnPRnCBM():
    from pandas import DataFrame
    import subprocess
    ROOT='/'+subprocess.check_output('pwd',shell=True).decode('utf8').strip('\n').split('/')[1]
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/line/ASSIGN-L.TXT'
    with open(fname) as text_file:
        d=[line.strip('\n') for line in text_file]
    VT,ET,PRO_NO=[i[:4] for i in d],[i[5:8] for i in d],[i[9:13] for i in d]
    df_asgn=DataFrame({'PRO_NO':PRO_NO,'VT':VT,'ET':ET})
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/line/PROFIL-L.TXT'
    with open(fname) as text_file:
        d=[line.strip('\n') for line in text_file]
    PRO_NO,SPE_NO,WT=[i[:4] for i in d],[int(i[11:14]) for i in d],[float(i[24:30]) for i in d]
    df_prof=DataFrame({'PRO_NO':PRO_NO,'SPE_NO':SPE_NO,'WT':WT})
    NC=20
    fname=ROOT+'/TEDS/teds10_camx/HourlyWeighted/line/CBM.DAT'
    with open(fname) as text_file:
        d=[line.strip('\n') for line in text_file]
    d=d[1:]
    SPE_NO,MW=[int(i[41:44]) for i in d],[float(i[57:63]) for i in d]
    BASE=[[i[63+j*6:63+(j+1)*6] for j in range(NC)] for i in d]
    d=BASE
    for i in range(len(d)):
        ii=d[i]
        for j in range(NC):
            s=ii[j].strip(' ')
            if len(s)==0:
                BASE[i][j]=0.
            else:
                BASE[i][j]=float(s)
    df_cbm=DataFrame({'SPE_NO':SPE_NO,'MW':MW,'BASE':BASE})
    return (df_asgn,df_prof,df_cbm)

def str2pair(L):
    o=['(',')',"['","']","'"]
    for old in o:
       L=[i.replace(old,'') for i in L]
    for i in range(len(L)):
        if ',' not in L[i]:
            L[i]=L[i]+','+L[i]
    i=L[0]
    try:
        L0=int(i.split(',')[0])
    except:
        ll=[(i.split(',')[0],i.split(',')[1]) for i in L]
        ll=[(i[0],i[1].replace(' ','')) for i in ll]
    else:
        ll=[(int(i.split(',')[0]),int(i.split(',')[1])) for i in L]
    return ll

def list2pairs(L):
    ll=[i.replace('[','').replace(']','') for i in L]
    L=[]
    for i in ll:
        l=[]
        for j in i.split('),'):
            [l.append(k) for k in str2pair([j])]
        L.append(l)
    return L

def WGS_TWD(df):
  import twd97
  from pandas import read_csv
  from pyproj import Proj
  import numpy as np
  ll=read_csv('TEDS10_AREA_WGS84.LL')
  Latitude_Pole, Longitude_Pole = 23.61000, 120.9900
  Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)
  pnyc = Proj(proj='lcc', datum='NAD83', lat_1=10, lat_2=40,
        lat_0=Latitude_Pole, lon_0=Longitude_Pole, x_0=0, y_0=0.0)
  x,y=pnyc(np.array(ll.lon),np.array(ll.lat), inverse=False)
  df.UTME=x+Xcent
  df.UTMN=y+Ycent
  return df

def tune_UTM(df):
#using CSC and XieHePP to calibrate the Map
  import numpy as np
  xiheIXY_Verdi=(67,126) #fallen in the sea
  xiheIXY_Target=(66,124)#calibrate with County border and seashore line
  CSCIXY_Verdi=(20,30) #fallen in the KSHarbor
  CSCIXY_Target=(21,31)
  rateXY=np.array([(xiheIXY_Target[i]-CSCIXY_Target[i])/(xiheIXY_Verdi[i]-CSCIXY_Verdi[i]) for i in range(2)])
  Xcent,Ycent= 248417-333.33*5,   2613022-3000. #tuning the coordinates
  df.UTME=[round((i-Xcent)*rateXY[0]+Xcent,-3) for i in df.UTME]
  df.UTMN=[round((i-Ycent)*rateXY[1]+Ycent,-3) for i in df.UTMN]
  return df
