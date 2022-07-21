      program abi_camx
      integer,external::jd
      integer sjd,ejd
      integer hh  !處理總時數
      integer,allocatable::id_sta(:)
      integer icha,m(6),istd(2,7),nstd(7)
      real,allocatable::obs(:,:,:),sim(:,:,:)
      real,allocatable::mb1(:),ob1(:,:),ge1(:,:)
      real mb2,ob2(6),ge2(6),std(2,7) !std for ob/ge and SOPNV
      character*2 atmp(8)
      character*40 inp
      character*14,allocatable::sta_name(:)
      character root*60,LPAS(2,7)*1
      logical WithData(100)

      call getarg(1,root)
      icha=0
      do i=1,60
        if(root(i:i).eq.' ')then
          icha=i-1
          exit
        endif
      enddo
      if(icha.eq.0)then
        write(*,*)'root not found. '
        stop
      endif

      open(11,file='abi_inp.txt',status='old')
      read(11,*)inp
      read(11,'(4a2,1x,4a2)')(atmp(i),i=1,8)

      read(atmp(1),'(i2)')isyy
      read(atmp(2),'(i2)')ismm
      read(atmp(3),'(i2)')isdd
      read(atmp(4),'(i2)')ishh
      read(atmp(5),'(i2)')ieyy
      read(atmp(6),'(i2)')iemm
      read(atmp(7),'(i2)')iedd
      read(atmp(8),'(i2)')iehh

      sjd=jd(isyy,ismm,isdd)
      ejd=jd(ieyy,iemm,iedd)
c      hh=(iedd-isdd)*24+(iehh-ishh+1)
      ann=365
      if(mod(isyy,4).eq.0)ann=366
      hh=((ieyy-isyy)*ann+(ejd-sjd))*24+(iehh-ishh+1)

      if(hh.le.0)then
        write(*,*)'Running hours less than 0.',hh
        stop
      endif

      open(13,file='ovm.dat',status='old')
      ista=100
      allocate(id_sta(ista+1))
      allocate(sta_name(ista+1))
      allocate(mb1(ista+1))
      allocate(ob1(7,ista+1))
      allocate(ge1(7,ista+1))
      sta_name='*'
      hh=0
      read(13,*)
      DO
      read(13,*,end=121)
      hh=hh+1
      ENDDO
121   rewind(13)  
      allocate(obs(hh,6,ista+1))
      allocate(sim(hh,6,ista+1))
      read(13,*)
      ii=0
        do ih=1,hh
!      S        O&PMT       PMf       N        V
            read(13,'(i3,t4,a14,
     + t31,f7.1, t45,2f7.1, t66,f7.1, t73,f7.1,t88,f8.0,
     + t110,f7.1,t124,2f7.1,t147,f7.1,t152,f7.1,f8.0)')
     +        ii,sta_name(ii),
     +        (obs(ih,j,ii),j=1,6),(sim(ih,k,ii),k=1,6) !SOPPNV
        enddo

      mb1=0.
      mb2=0.
      ob1=0.
      ob2=0.
      ge1=0.
      ge2=0.
        WithData(ii)=.false.
      ns=0
      do ii=1,100
        if(sum(obs(:,:,ii))*sum(sim(:,:,ii)).eq.0) cycle
        WithData(ii)=.true.
        ns=ns+1
      enddo
      print*,'total station=',ns
c-----計算mb
      idays=ejd-sjd+1
      ii2=0
      do ii=1,ista
        if(.not.WithData(ii).or.sta_name(ii).eq.'*')cycle
        ii1=0
        do id=1,idays
          if(id.eq.1)then
            i1=1
            i2=24-ishh
          else
            i1=i2+1
            i2=min0(i1+23,hh)
          endif
          r1=maxval(obs(i1:i2,2,ii))
          if(r1.lt.40.)cycle !note O3>40
          if(r1.le.0.)cycle
            ii1=ii1+1
            ii2=ii2+1
            r2=maxval(sim(i1:i2,2,ii))            
            mb1(ii)=mb1(ii)+(r2-r1)/r1
            mb2=mb2+(r2-r1)/r1
        enddo
        if(ii1.gt.0)mb1(ii)=int(mb1(ii)/real(ii1)*100.)/100.
      enddo
      if(ii2.gt.0)mb2=int(mb2/real(ii2)*100.)/100.
c-----計算ob,ge
      do isp=1,6
        i2=0
        do ii=1,ista
        if(.not.WithData(ii).or.sta_name(ii).eq.'*')cycle
          i1=0
          do ih=1,hh
            r1=obs(ih,isp,ii)
            if(isp.eq.2.and.r1.lt.40.)then
              cycle
            elseif(isp.eq.1.and.r1.lt.1.)then  !so2小於1ppb(偵測極限)不納入計算
              cycle
            elseif(isp.eq.6.and.r1.lt.50.)then  !NMHC小於50ppb(偵測極限)不納入計算
              cycle
            elseif(r1.le.0.)then
              cycle
            endif
            i1=i1+1
            i2=i2+1
            r2=sim(ih,isp,ii)
            if(r1.le.0)stop 'r1.eq.0'
            ob1(isp,ii)=ob1(isp,ii)+(r2-r1)/r1
            ob2(isp)=ob2(isp)+(r2-r1)/r1
            ge1(isp,ii)=ge1(isp,ii)+abs(r2-r1)/r1
            ge2(isp)=ge2(isp)+abs(r2-r1)/r1
          enddo
          ob1(isp,ii)=ob1(isp,ii)/real(i1)
          ge1(isp,ii)=ge1(isp,ii)/real(i1)
        enddo
        ob2(isp)=int(ob2(isp)/real(i2)*100.)/100.
        ge2(isp)=int(ge2(isp)/real(i2)*100.)/100.
      enddo

c-----寫出
      open(12,file='abi_'//root(1:icha)//'.txt')
      write(12,'(a)')
     +'STA NAME  MB_O3  OB_O3  GE_O3 OB_PMT GE_PMT OB_PMf GE_PMf OB_NO2'
     +//' GE_NO2 OB_HC  GE_HC   OB_SO2 GE_SO2'
      data std/0.40,0.80,  0.15,0.35,  0.50,1.50, 0.50,1.50,0.40,0.80, 0.40,0.80,
     + 0.10, -1.0/
      data m/2,3,4,5,6,1/ !output sequence
      i=ista+1
      sta_name(i)='all'
      id_sta(i)=1000
      do l=1,6 !SOPNV
        ob1(l,i)=ob2(l)
        ge1(l,i)=ge2(l)
      enddo
      mb1(i)=mb2
      istd=0
      nstd=0
      do i=1,ista+1
        if(i.le.ista.and..not.WithData(i))cycle
        if(sta_name(i).eq.'*')cycle
      LPAS=' ' 
      do l=1,6 !SOPPNV
        if(isnan(ob1(l,i)).or.isnan(ge1(l,i)))cycle !NaN
        if(abs(ob1(l,i)).le.std(1,l)) LPAS(1,l)='*'
        if(abs(ge1(l,i)).le.std(2,l)) LPAS(2,l)='*'
        if(l.ge.5.and.l.le.6) then !NV
          if(ob1(l,i).ge.-0.4.and.ob1(l,i).le.0.5) LPAS(1,l)='*'
        endif
        nstd(l)=nstd(l)+1
      enddo
        if(mb1(i)-1.ne.mb1(i).and.abs(mb1(i)).le.std(1,7))LPAS(1,7)='*'
        do l=1,7
        do k=1,2
          if(LPAS(k,l).eq.'*')istd(k,l)=istd(k,l)+1
        enddo
        enddo
        if(mb1(i)-1.ne.mb1(i))nstd(7)=nstd(7)+1
        if(sta_name(i).ne.'')then
       write(12,'(i3,1x,a4,13(f6.2,A1))')i,sta_name(i)(1:4),mb1(i),
     + LPAS(1,7),
     +  (ob1(m(l),i),LPAS(1,m(l)),ge1(m(l),i),LPAS(2,m(l)),l=1,6)
        if(i.eq.ista+1)then
      write(12,'(a)')
     +'Attainment MB_O3 OB_O3  GE_O3 OB_PMT GE_PMT OB_PMf GE_PMf OB_NO2'
     +//' GE_NO2 OB_HC  GE_HC  OB_SO2  GE_SO2'
        ssum=0
        nsum=0
        do l=1,7
          nsum=nsum+nstd(l)
        do k=1,2
          ssum=ssum+istd(k,l)
         ob1(l,i)=real(istd(1,l))/real(nstd(l))*100.
         ge1(l,i)=real(istd(2,l))/real(nstd(l))*100.
        enddo
        enddo
         ge1(7,i)=ssum*100./real(nsum*2.)
        write(12,'(1x,14(f6.1,A1))')ge1(7,i),'%',ob1(7,i),
     +  '%',(ob1(m(l),i),'%',ge1(m(l),i),'%',l=1,6)
        endif
        endif
      enddo
      end

c-----------------------------------------------------------
      FUNCTION JD(YY,MM,DD)
C-----PURPOSE: 輸入年月日，輸出太陽日
      INTEGER JD,YY,MM,DD
      INTEGER DAYS(12),DAYS2(12)

      DATA DAYS /1,32,60,91,121,152,182,213,244,274,305,335/
      DATA DAYS2 /31,28,31,30,31,30,31,31,30,31,30,31/

      IF(MOD(YY,4).EQ.0)THEN
        DAYS2(2)=29
        DAYS(3)=61
        DAYS(4)=92
        DAYS(5)=122
        DAYS(6)=153
        DAYS(7)=183
        DAYS(8)=214
        DAYS(9)=245
        DAYS(10)=275
        DAYS(11)=306
        DAYS(12)=336
      ELSE
        DAYS2(2)=28
        DAYS(3)=60
        DAYS(4)=91
        DAYS(5)=121
        DAYS(6)=152
        DAYS(7)=182
        DAYS(8)=213
        DAYS(9)=244
        DAYS(10)=274
        DAYS(11)=305
        DAYS(12)=335
      ENDIF

C-----Check
      IF(DD.GT.DAYS2(MM).OR.MM.GT.12.OR.YY.GT.99)THEN
        write(*,'('' Julian day converting error!'',3(1x,i2.2))')
     +    yy,mm,dd
        stop
      ENDIF

      JD=DAYS(MM)+DD-1
      RETURN
      END FUNCTION



