      integer,allocatable::ISQ(:)     ! STATION COORDINATES (M)
      real,allocatable::x(:),y(:),var(:,:,:,:)
      character, allocatable:: A4(:)*4
      integer, allocatable::lstn(:)
      character stn*8, fmt*100
      parameter(NPOL=11,LDATE=366)
      CHARACTER NAMPOL(0:NPOL)*3,myr*4
      DATA NAMPOL/'TMP','SO2','CMO','OZN','PMT',
     +  'NOX','P25','NO2','OZ8','NMH','WSP','WDR'/
C** 
      open(21,file='cwb_epa.csv',
     +  status='old')
      read(21,*)
      nst=0
      do while(.true.)
        read(21,*,end=51)
        nst=nst+1
      enddo
100   format(i3,5x,a4,t16,i7,t25,i7,t33,i1)
51    continue
c-----Allocate
      allocate(x(nst))
      allocate(y(nst))
      allocate(isq(nst))
      allocate(A4(nst))
      allocate(lstn(nst))

      rewind(21)
      read(21,*)
      do i=1,nst
        read(21,*,end=52)isq(i),x(i),y(i)
        if(isq(i).gt.460000)isq(i)=mod(isq(i)/10,1000)
      enddo
52    close(21)
      open(1,file='ovm.dat',status='unknown')
      itime=0
      lstn=0
      read(1,300,end=98)
      DO 
        read(1,300,end=98)is
        js=0
        do i=1,nst
          if(is.eq.isq(i))then
            js=i
            exit
          endif
        enddo
        if(js.eq.0) then
        print*,is
        stop 'stn not found'
        endif
        if(lstn(js).eq.0)lstn(js)=1
       itime=itime+1
      enddo
98    rewind(1)
      
      ntime=(itime)/sum(lstn) !first line
      if(ntime*sum(lstn).ne.itime)stop 'line missing'
      allocate(var(2,9,nst,ntime)) 
      open(21,file='stn2grads.dat',form='unformatted',
     &status='unknown' ,access='stream')
      read(1,*)
      iss=0
      DO js=1,nst
        if(lstn(js).eq.0)cycle
      DO it=1,ntime 
        read(1,300,end=99)is,A4(js),Jul,ical,
     & (var(1,j,js,it),j=1,9),ws,wd,(var(2,j,js,it),j=1,8)
300     FORMAT(I3,A4,8x,I8,1x,I6,7F7.1,2f8.0,9f7.1,f8.0)
          var(1,8,js,it)=amax1(0.,var(1,9,js,it))
        do j=1,8
          var(1,j,js,it)=amax1(0.,var(1,j,js,it))
        enddo
      ENDDO !LOOP FOR DAY
        iss=iss+1
        k=int(alog10(real(iss)))+1
        write(fmt,'(A,I1,A)')'(A4,I',k,',A1,I3.3,A4)'
!       write(*,trim(fmt))'nst.',iss,'=',is,A4(js)
      ENDDO ! LOOP FOR STATION
!ozone 8 hour average
      j=3 !for ozone
      var(:,9,:,:)=0
      DO js=1,nst
        if(lstn(js).eq.0)cycle
      DO iom=1,2
      DO it=4,ntime-4
        do it2=it-3,it+4
          var(iom,9,js,it)=var(iom,9,js,it)+var(iom,j,js,it2)/8.
        ENDDO
      ENDDO
      ENDDO !LOOP FOR DAY
      ENDDO ! LOOP FOR STATION

      nlev=1
      nflag=1
      Atime=0
      itime=0
      ifreq=3
      DO it=1,ntime,ifreq
      DO JS=1,NST
      if(lstn(js).eq.0)cycle
      write(stn,'(I3.3,A4)')isq(JS)!,A4(JS)
      !if(it.eq.1)print*,stn
      write(21)stn,y(JS),x(JS),Atime,nlev,nflag,((var(i,j,js,it),i=1,2),j=1,9)
!     print*,stn,y(JS),x(JS),Atime,nlev,nflag,((var(i,j,js,it),i=1,2),j=1,8)
      ENDDO ! LOOP FOR STATION
      write(21)stn,0.0,0.0,0.0,0,0
      itime=itime+1
      ENDDO !LOOP FOR DAY
99    print*,itime, ifreq
      close(1)
      close(21)
      stop
      end


