      program bio2month

C     read teds bio data and transfer to 1~12 month
C     檔名areabio01~areabio12 為1～12月
C     欄位1-3   UTME座標(km),I3
C     欄位4     空白
C     欄位5-8   UTMN座標(km),I4
C     欄位9     空白
C     欄位10-19 isoprene當月份該網格排放總量(kg/month),F10.3
C     欄位20    空白
C     欄位21-30 monoterpene當月份該網格排放總量(kg/month),F10.3
C     欄位31    空白
C     欄位32-41 otherVOCs當月份該網格排放總量(kg/month),F10.3
C     欄位42    空白
C     欄位43-52 MBO當月份該網格排放總量(kg/month),F10.3

      integer m,utme,utmn
      real iso,mono,onmhc,mbo
      real miso(12),mmono(12),monmhc(12),mmbo(12),mtnmhc(12) !各月數值
      real piso(13),pmono(13),ponmhc(13),pmbo(13) !比例(12個月及全年)
      character mm*2
C     各月份比例可參考生物源技術手冊
      
      data piso /0.42,0.66,0.95,1.02,1.69,2.24,
     +           2.39,2.18,1.79,1.21,0.68,0.35,15.58/
      data pmono /0.64,0.79,1.01,1.12,1.56,1.84,
     +            1.89,1.94,1.65,1.26,0.95,0.62,15.27/
      data ponmhc /0.66,0.78,0.97,1.08,1.47,1.68,
     +             1.71,1.79,1.54,1.22,0.96,0.65,14.51/
      data pmbo /0.01,0.02,0.03,0.03,0.05,0.07,
     +           0.08,0.07,0.06,0.04,0.02,0.01,0.49/          
 
      do m=1,12
        write(mm,'(I2.2)')m
        open(20+m,file='bioemis.space.'//mm,status='unknown')
      enddo
      open(13,file='teds11_bio_twd97.csv',status='old')      
      read(13,*)

      do while(.true.)
         read(13,*,end=100) utme,utmn,tnmhc,iso,mono,onmhc,mbo
         do m=1,12
           miso(m)=iso*piso(m)/piso(13)*1000. !乘上該月份比例,單位換算kg
           mmono(m)=mono*pmono(m)/pmono(13)*1000.
           monmhc(m)=onmhc*ponmhc(m)/ponmhc(13)*1000.
           mmbo(m)=mbo*pmbo(m)/pmbo(13)*1000.
           mtnmhc(m)=miso(m)+mmono(m)+monmhc(m)
           write(m+20,60) utme,utmn,mtnmhc(m),miso(m),mmono(m),monmhc(m),mmbo(m)
60         format(T2,I6,T9,I7,T17,5F10.3)
         enddo
      enddo
100   continue

      do m=1,12
        close(20+m)
      enddo
      stop
      end
