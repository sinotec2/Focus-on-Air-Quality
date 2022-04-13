c ifort -extend_source -o ptem ptem.f 
C     *** READ PTSOURCE PACKETS AND CREATE THE FILE
	include 'param.inc'
	include 'paramsK.puf'
      include 'comparm.puf'
      include 'filnam.puf'
      include 'flags.puf'
      include 'grid.puf'
      include 'puff.puf'
      include 'pt1.puf'
      include 'pt2.puf'
      real n2
      logical cem(400)
      common /trans/npt2file,em2dat(mxp4,mxpt2)
      common /opdat/op(370,24,120),NOPTSbase,cem
      common /sndat/s2(370,24,120),n2(370,24,120)
      common /TVdat/TM(370,24,120),VS(370,24,120)
      character PCS*4,CNO*8
      DATA NUPTS /14/
      data ibdat2(1)/2017365/ ibtim2(1)/16/ !UTC 
      data iedat2(1)/2018365/ ietim2(1)/23/
      data label2(1)/' CEMS'/StackBaseElev/0/

c      narg=iARGc ()
c      if(narg.ne.2) stop 'ptem_PWR ibdat2 iedat2(yyyyjjj)'
c      do i=1,2
c        call getarg(i,CNO(i))
c      enddo
      read(*,*)ical,ibeg,iend
      write(CNO,'(I8)')ical
      open(1,file='/home/sespub/power/p'//CNO//'.csv',
     + STATUS='UNKNOWN')
      open(13,file='/home/sespub/power/g'//CNO//'.csv',
     + STATUS='UNKNOWN')
      call juldate(ibeg)
      ibdat2(1)=ibeg
      call juldate(iend)
      iedat2(1)=iend
      i=1
      NOPTSbase=100
      Xcent= 248417-333.33*5
      Ycent= 2613022-3000.
      read(1,*)
      do 
        read(1,*,end=100)PID(i)(1:12),H(i),D(i),T(i),V(i),X(i),Y(i)
        X(i)=X(i)-Xcent
        Y(i)=Y(i)-Ycent
        if (abs(X(i))>83*3000/2.)cycle
        if (abs(Y(i))>137*3000/2.)cycle
        T(i)=T(i)+273
        i=i+1
      enddo
100   close(1)
      NOPTSbase=i-1
      open(NUPTS,file='ptemarb_pwr.dat',STATUS='UNKNOWN')

c	call deletePT(NOPTSbase)
c	call addPT(NOPTSbase)

c	
        npt2file=NOPTSbase

       
c	time independent data
        do ii=1,NOPTSbase
        cid2(ii)(1:12)=PID(ii)(1:12)
c			PRINT*,cid2(ii),PID(ii)
        tiem2(1,ii)=X(ii)/1000.		!in Km
        tiem2(2,ii)=Y(ii)/1000.		!in Km
        tiem2(3,ii)=H(ii)			!in m
        tiem2(4,ii)=D(ii)			!in m
        tiem2(5,ii)=StackBaseElev	!in m
        tiem2(6,ii)=0				!Building Flag (y/n)1/0
		tiem2(7,ii)=0				!Building Flag (y/n)1/0
		tiem2(8,ii)=V(ii)                       !Building Flag (y/n)1/0
	enddo
        call WrtCalEms(0,ibdat2(1),ibtim2(1),iedat2(1),ietim2(1))
c	time dependent data
        call rd_op(CNO)
c	g-mole/HR -> g/s
	istrt=ibdat2(1)*100+ibtim2(1)
	istop=iedat2(1)*100+ietim2(1)
	do 177 id=1,1	!istrt,istop
	if(mod(id,100).gt.23) goto 177
	ibdat=ibdat2(1)
	ibtim=ibtim2(1)
	iedat=iedat2(1)
	ietim=ietim2(1)
        call WrtCalEms(1,ibdat,ibtim,iedat,ietim)
177	continue
	stop
	end
	subroutine WrtCalEms(iwrite,ibdat,ibtim,iedat,ietim)
	include 'paramsK.puf'
      include 'comparm.puf'
      include 'filnam.puf'
      include 'flags.puf'
      include 'grid.puf'
      include 'puff.puf'
      include 'pt1.puf'
      include 'pt2.puf'
	include 'param.inc'

      real xmwem2x(mxspec),flow(400),ems_tmp(20),n2
      character*12 cslst2x(mxspec),vrs2
      character line*100
      logical cem(400),old_gas
c

c    EM2DAT(nse2+4,npt2) - real array - Time-varying PTEMARB source

	common /trans/npt2file,em2dat(mxp4,mxpt2)
      common /opdat/op(370,24,120),NOPTSbase,cem
      common /sndat/s2(370,24,120),n2(370,24,120)
      common /TVdat/TM(370,24,120),VS(370,24,120)
	data iunit/14/ NoutFile/1/ iv54/54/ vrs2/'  2.1'/
	data fname2/'PTEMARB'/ iutmz2x/51/ mbdw/0/
	nse2=8
cSO2 SO4 NOX HNO3 NO3 PMS1(fine),PMS2(10)PMS3(coarse)
c1   2   3   4    5   6          7       8
	cslst2x(1)= 'SO2'
	cslst2x(2)= 'SO4'
	nse2=8
cSO2 SO4 NOX HNO3 NO3 PMS1(fine),PMS2(10)PMS3(coarse)
c1   2   3   4    5   6          7       8
	cslst2x(1)= 'SO2'
	cslst2x(2)= 'SO4'
	cslst2x(3)= 'NOX'
	cslst2x(4)= 'HNO3'
 	cslst2x(5)= 'NO3'
 	cslst2x(6)= 'PMS1'
 	cslst2x(7)= 'PMS2'
 	cslst2x(8)= 'PMS3'
	xmwem2x(1)=64
	xmwem2x(2)=96
	xmwem2x(3)=46
	xmwem2x(4)=63
	xmwem2x(5)=62
	xmwem2x(6)=1
	xmwem2x(7)=1
	xmwem2x(8)=1
	do i=1,NoutFile
	read(vrs2,'(f12.0)')rvrs2
	ivrs2(i)=NINT(10.*rvrs2)
         if(ivrs2(i).LT.iv54) then
            nwords=10
         else
            nwords=8
         endif
	if(iwrite.eq.1) goto 1000
        open(1,file='/home/cpuff/2018/ptem/head.txt',status='unknown')
        do
        read(1,'(A100)',end=98)line(1:)
        write(iunit,'(A)') trim(line(1:))
        enddo
98      close(1)
        iyb=int(ibdat/1000)
        ijb=mod(ibdat,1000)
        iye=int(iedat/1000)
        ije=mod(iedat,1000)
        write(iunit,'(8I5)')iyb,ijb,ibtim,0,iye,ije,ietim,3600
        write(iunit,*)npt2file,8
c --- Header Record #2/3 - Species list, and
c --- Header Record #3/4 - Molecular weights of each emitted species
         write(iunit,*)(cslst2x(n),n=1,nse2)
         write(iunit,*)(xmwem2x(n),n=1,nse2)
		ibsrc2(i)=1
		iesrc2(i)=npt2file
		npt2=npt2file
            do k=ibsrc2(i),iesrc2(i)
               ii=MIN(k,npt2)
               write(iunit,101)cid2(ii)(1:12),(tiem2(n,ii),n=1,7),0. !nwords)
101            format(A15,4F10.3,10F3.0)
            enddo
        return

1000    do ii=ibsrc2(i),iesrc2(i)
          area= 3.14/4.*tiem2(4,ii)**2
          flow(ii)=em2dat(2,ii)*273./em2dat(1,ii)*area
        enddo
        do idat=ibdat,iedat
        idend=365
        if(mod(int(idat/1000),4).eq.0)idend=366
        if(mod(idat,1000).gt.idend.or.mod(idat,1000).eq.0)cycle
        iy=int(idat/1000)
        id=mod(idat,1000)
        do itim=0,23 !UTC
          if (idat.eq.ibdat.and.itim.lt.ibtim)cycle
          if (idat.eq.iedat.and.itim.gt.ietim)cycle
          write(iunit,'(8I5)')iy,id,itim,0,iy,id,itim,3600
          jjj=id
          jhr=mod(itim+8,24)+1
          do ii=ibsrc2(i),iesrc2(i)
cSO2 SO4 NOX HNO3 NO3 PMS1(fine),PMS2(10)PMS3(coarse)
c3   4   5   6    7   8          9       10
                ems_tmp(1)=TM(jjj,jhr,ii)
                ems_tmp(2)=VS(jjj,jhr,ii)
                tsp=op(jjj,jhr,ii)
                ems_tmp(3)=s2(jjj,jhr,ii)
                ems_tmp(5)=n2(jjj,jhr,ii)
                ems_tmp(4)=tsp*1.80
                ems_tmp(8)=tsp*0.35
                ems_tmp(9)=tsp*0.20
                ems_tmp(10)=tsp*(1-0.35-0.2)
                sume=s2(jjj,jhr,ii)+n2(jjj,jhr,ii)+tsp
                if(sume.ne.0.and.ems_tmp(1).lt.T(ii)*0.8)ems_tmp(1)=T(ii)
                if(sume.ne.0.and.ems_tmp(2).lt.V(ii)*0.5)ems_tmp(2)=V(ii)
            zero=0
            write(iunit,102)cid2(ii)(1:12),(ems_tmp(n),n=1,2),zero,zero,(ems_tmp(n),n=3,nwords)
102     format(A12,2F6.1,15(1PG11.4E2))
        enddo
        enddo
      enddo
	enddo !ifile
	return
	end
c-------------------------------------------------------------
      subroutine juldate(idate)
      dimension nday(12)
      data nday/31,28,31,30,31,30,31,31,30,31,30,31/
c
c-----Entry point
c
      iyear = idate/10000
      imonth = (idate - iyear*10000)/100
      iday = idate - iyear*10000 - imonth*100
      IF(IDAY.GT.NDAY(IMONTH).OR.IDAY.LE.0) THEN
        IDATE=-1
        RETURN
      ENDIF
c
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29

      mday = 0
      do 10 n = 1,imonth-1
        mday = mday + nday(n)
 10   continue
      jday = mday + iday
      idate = iyear*1000 + jday
c
      return
      end

      subroutine rd_op(CNO)
	include 'paramsK.puf'
      include 'pt2.puf'
      real n2,NOx,NOX_GPS
      integer YYYYMMDDHH,ymdh
      character a12*12,path*200,CNO*8,P_NO*4,PID*12
      logical cem(400),old_gas
      common /opdat/op(370,24,120),NOPTSbase,cem
      common /sndat/s2(370,24,120),n2(370,24,120)
      common /TVdat/TM(370,24,120),VS(370,24,120)
      cem=.False.
      op=0.
      s2=0.
      n2=0.
      TM=0.
      VS=0.
      read(13,*)
      do
        SO2_GPS=0.
        NOX_GPS=0.
        PM_GPS=0.
!CP_NO,TEMP,VEL,CO_GPS,NMHC_GPS,NOX_GPS,PM25_GPS,PM_GPS,SOX_GPS,DateHr
        read(13,*,end=9,err=10)PID,T,VEL,dum,dum,NOX_GPS,dum,PM_GPS,SO2_GPS,ymdh
        ip=0
        do ii=1,NOPTSbase
          if(PID.eq.cid2(ii)(1:12)) then
            ip=ii
          endif
        enddo
          if(ip.ne.0) then
            ical=ymdh/100-20000000
            call juldate(ical)
            jjj=mod(ical,1000)
            ihr=mod(ymdh,100)+1
            op(jjj,ihr,ip)=abs(PM_GPS) !g/s
            n2(jjj,ihr,ip)=abs(NOX_GPS) !g/s
            s2(jjj,ihr,ip)=abs(SO2_GPS) !g/s
            TM(jjj,ihr,ip)=amin1(600.,abs(T))+273.
            if(VEL.eq.0)VEL=tiem2(8,ii)
            VS(jjj,ihr,ip)=VEL
          endif
      enddo
9     close(13)
      do j=1,3
        op(jjj+j,:,:)=op(jjj,:,:)
        n2(jjj+j,:,:)=n2(jjj,:,:)
        s2(jjj+j,:,:)=s2(jjj,:,:)
        TM(jjj+j,:,:)=TM(jjj,:,:)
        VS(jjj+j,:,:)=VS(jjj,:,:)
      enddo
      return
10    print*,PID,T,VEL,dum,dum,NOX_GPS,dum,PM_GPS,SO2_GPS,ymdh
      return
      end

 
