
import twd97
Latitude_Pole, Longitude_Pole = 23.61000, 120.990
Xcent, Ycent = twd97.fromwgs84(Latitude_Pole, Longitude_Pole)

def twdIJ1(xv,yv):
  return (int((xv-Xcent)/1000)+int(83*3/2))*1000+int((yv-Ycent)/1000)+int(137*3/2)

def terrainXYINC(pth,STR):
  from pandas import read_csv, DataFrame
  import os

  WEB='/Library/WebServer/Documents/'
  CGI='/Library/WebServer/CGI-Executables/isc/'
  OUT='>> '+pth+'isc.out'
  geninp='/opt/local/bin/gen_inp.py'
  WAITM='/opt/local/bin/wait_map.cs'
  CSV=WEB+'terr_results/TWN_1X1REC.csv'
  reg='GRIDCART'
  

  inam=STR.index(reg)
  inp=STR[(inam+len(reg)):].split()
  snamo=inp[0]
  fname=pth+snamo+'.zip'

  #read the others
  inc='XYINC'
  iinc=STR.index(inc)
  inp=STR[(iinc+len(inc)):].lstrip()
  x0,nx,dx,y0,ny,dy=(int(float(inp.split()[i])) for i in range(6))
  inp0='%s %s %s %s %s %s' %(x0,nx,dx,y0,ny,dy)
  inp=inp0.replace(' ','_')
  df=read_csv(CSV)
  #df['inp']=['%s %s %s %s %s %s' %(i,j,k,l,m,n) for i,j,k,l,m,n in zip(df.x0,df.nx,df.dx,df.y0,df.ny,df.dy)]
  if inp not in list(df.inp) or not os.path.isfile(WEB+'terr_results/'+inp+'/'+snamo+'.REC'):
    x0,nx,dx,y0,ny,dy=(int(float(inp.split('_')[i])) for i in range(6))
    centIJ=str(twdIJ1(x0+nx*dx/2,y0+ny*dy/2))
    pathIJ=centIJ
    path=snamo
    DD={}
    for s in 'pathIJ,centIJ,path,x0,y0,nx,ny,dx,dy,inp'.split(','):
      eval('DD.update({"'+s+'":['+s+']})',locals())
    df=df.append(DataFrame(DD),ignore_index=True,sort=True)
    df.drop_duplicates(inplace=True)  

    cmd ='cd '+pth+';'
    cmd+='sed s/test/'+snamo+'/g '+WEB+'trj_results/aermap.inp_template>aermap.inp;'
    os.system(cmd)
    cmd ='cd '+pth+';'
    cmd+= geninp+' '+pth+snamo+' '+inp0+' >>geninp.out & disown'
    rst=os.system(cmd)

    n=90
    while rst==0 and n<100:
      cmd='sleep 5s'
      os.system(cmd)
      if os.path.isfile(fname):break
      n+=1

    cmd ='cd '+pth+';'
    cmd+= WAITM+' '+pth+' '+inp+' & disown'
    rst=os.system(cmd)
    df.set_index('pathIJ').to_csv(CSV)
  else:
    terr_path=list(df.loc[df.inp==inp,'path'])[0]
    path=WEB+'terr_results/'+inp+'/'+terr_path
    cmd ='cd '+pth+';'
    cmd+='for i in $(ls '+path+'*);do j=$(echo $i|cut -d"/" -f7);ln -f ../../terr_results/'+inp+'/$j .;done'+OUT
    os.system(cmd)
    snamo=terr_path.split('/')[-1].replace('.REC','')
  return snamo
