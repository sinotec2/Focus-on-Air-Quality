cat /Users/kuang/bin/avrg2jul.f
c this routine calculate all time average of AVRG fields, and OP AS A ARG FILE
       INCLUDE  'PARAMS.CMD'
       INCLUDE  'CHPARM.CMD'
       INCLUDE  'CNTROL.CMD'
       INCLUDE  'FILCON.CMD'
       INCLUDE  'SEGTAB.CMD'
       INCLUDE  'NETDEP.CMD'
       INCLUDE  'BALANC.CMD'
       INCLUDE  'LOCPTR.CMD'
       INCLUDE  'MSCAL.CMD'
      integer,parameter::fmax=300
      integer,parameter::MXSPEC=40
      integer itmp(4)
      character*4,allocatable:: SPNAME(:,:)
      CHARACTER*60 NAM0(fmax) ! input/output file names
      character*4 fname(10)
      character note(60)*4,names*10
      logical O3,GRD 
      integer,allocatable::ndate2(:),ndlast2(:)
      real,allocatable::ttime2(:),ttlast2(:)
      real,allocatable:: A1(:,:,:,:),tim(:,:)
      real,allocatable:: tm(:,:,:)
      integer,allocatable:: yyjul(:,:),tbeg(:),tend(:)
      real SCR(40000),r(4)
      NUAV=41
      narg=iARGc ()
      if(narg.ne.1)stop  
     + 'avrg to avrg.JJJ/avrg.jjj'

      do i=1,narg
        call getarg(i,nam0(i))
      enddo
      call system('mkdir -p '//trim(nam0(1))//'.JJJ')
      do i=1,narg
          open(i+10,file=trim(nam0(1)),
     +      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
        print*,trim(nam0(i))
      enddo
      narg=2
      nfile=narg-1
      iout=narg+10
      IRD=1
        READ (IRD+10) fname, note, NOSEG, NOSPEC,
     +    NDATE, TTIME, NDLAST, TTLAST
      allocate(SPNAME(10,NOSPEC))
       ird=1
C
C--REGION DESCRIPTION HEADER
        READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
C
C--SEGMENT DESCRIPTION HEADER
        READ (IRD+10) (Itmp(j), J=1,4)
C
C--SPECIES DESCRIPTION HEADER
        READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
        nt=0
        do 
          READ (ird+10,END=30,err=30)i1,t1,i2,t2
!       print*,i1,t1,i2,t2
          if(nt.eq.0) then
          i0=i1
          t0=t1
          endif

          DO  L=1,NOSPEC
            DO  K=1,NOZ
              READ (ird+10,END=30,err=30)
            enddo !k
          enddo !l
        nt=nt+1
        enddo !it
C
C         FIRST, WRITE TIME INTERVAL
C
30    rewind(IRD+10)
      do i=1,4!skip the header
              READ(10+ird)
      enddo
      NXY=NOXG*NOYG
      iyb=NDATE/1000
      iye=NDLAST/1000
      jjb=mod(NDATE,1000)
      jje=mod(NDLAST,1000)
      nday=365
      if(mod(iyb,4).eq.0)nday=366  
      NTi=((iye-iyb)*nday+(jje-jjb))*24+(TTLAST-TTIME)+1
      if(nt.ne.nti)then
      print*, nt,nti
        print*,'time not right!'
        NDATE=i0
        TTIME=t0
        NDLAST=i1
        TTLAST=t1
        endif

      allocate(A1(NXY,NOZ,NOSPEC,0:24))
      allocate(tm(NXY,NOZ,NOSPEC))
      allocate(yyjul(2,0:23),tim(2,0:23))
      do jjj=NDATE,NDLAST
       ii=mod(jjj,1000)
       if(ii.gt.nday.or.ii.eq.0)cycle
       write(names(1:5),'(I5.5)')jjj
       open(12,file=trim(nam0(1))//'.JJJ/'//names(1:5),
     + form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
        btime=0
        etime=0
        jjn=jjj+1
        if(ii.eq.nday)jjn=iye*1000+1
        if(jjj.eq.NDATE)btime=TTIME
        if(jjj.eq.NDLAST)etime=TTLAST
        if(jjj.eq.NDLAST)jjn=jjj
      write(12) fname, note, NOSEG, NOSPEC, jjj, btime,
     $  jjn, etime
      write(12) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
       write(12)1,1,NOXG,NOYG
       write(12)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
       nend=24
       if(jjj.eq.NDLAST)nend=int(etime)
       do it=int(btime),nend
          READ (11,END=33,err=33) yyjul(1,it),tim(1,it), yyjul(2,it),tim(2,it)
          if(it.lt.24)then
           if(yyjul(1,it).ne.jjj.or.tim(1,it).ne.it)then
            print*,jjj,it
            stop 'time not right'
          endif
          endif

          WRITE(12) yyjul(1,it),tim(1,it), yyjul(2,it),tim(2,it)
          DO  L=1,NOSPEC
            DO  K=1,NOZ
              READ(11,err=33)ISEG,(SPNAME(I,L),I=1,10),(A1(i,k,l,it),i=1,NXY)
              WRITE(12)ISEG,(SPNAME(I,L),I=1,10),(A1(i,k,l,it),i=1,NXY)
            enddo !k
          enddo !l
          WRITE(*,*)yyjul(1,it),tim(1,it), yyjul(2,it),tim(2,it)
        enddo !it
        do L=1,NOSPEC*NOZ+1
          backspace(11)
        enddo        
        print*,'backspace'
        close(12)
      enddo !jjj
      goto 34
33    print*,'end of file'
34    close(11)
      end
