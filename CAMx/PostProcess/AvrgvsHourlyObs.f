C
C  SET PARAMETERS FOR DIMENSIONS IN COMMON BLOCKS
C
C
C     COMDECK.CHPARM
C-----------------------------------------------------------------------
C
C     ***  /CHPARM/ CONTAINS CHEMISTRY PARAMETERS
C
      COMMON /CHPARM/ NSMAX,
     $  MSPEC(10,32), LREAC(32), LSSIC(32), LSSBC(32),
     $     BDSL (32), BDSU (32), BDNL (32), BDNU (32), DVRES(32)
C
      COMMON /CHPARM/ NRMAX,
     $  RKN  (90), RK   (90), LPHOT(90), LTDEP(90),
     $  ACTEN(90), TREF (90), TRINV(90), LATDEP(40)
C
      COMMON /CHPARM/ NCMAX,
     $  MCOEF(10,10), CVAL(10)
C
      LOGICAL  LREAC, LSSIC, LSSBC
      LOGICAL LPHOT, LTDEP
C
C     COMDECK.CNTROL
C------------------------------------------------------------------------
C
C     *** /CNTROL/ CONTAINS MANY CONTROL PARAMETERS OF GLOBAL INTEREST
C
C--DIMENSIONS AND REGION DESCRIPTORS USED A LOT
C
      COMMON /CNTRLd/ NOZ   , NOZP1 , NOZM1 , NOSEG , NOSPEC, NORS  ,
     $                NREACT, NCOEF ,
     $                KBEG  , KBUP  ,
     $                DELTAX, DELTAY, DZSURF
C
C--LOGICAL CONTROL FLAGS
C
      COMMON /CNTROL/ LCHEM , LANYPH, LANYTD, LANYSI, LANYSB,
     $                LPHFAC, LREST , LSINK , LPTS  , LRWY  ,
     $                LTEMP , LTERR , LCVAR
C
      LOGICAL LCHEM , LANYPH, LANYTD, LANYSI, LANYSB,
     $        LPHFAC, LREST , LSINK , LPTS  , LRWY  ,
     $        LTEMP , LTERR , LCVAR
C
C--TIME CONTROLS
C
      COMMON /CNTROL/ NDATE , TTIME , NDLAST, TTLAST,
     $                TSLIN , NSTEPS, TSLICE,
     $                TIAVE , TAVE1 , TAVE  ,
     $                TIINST, TINST1, TINST
C
C--INTEGRATION CONTROLS AND HANDY VARIABLES
C
      COMMON /CNTROL/ MAXITR, RERROR, DTMIN ,
     $                XKXY  , IPSPTR, LPSNOW,
     $                DELTXY, DELTZ3,
     $                DEFRUF, DEFVEG,
     $                FRDARK,
     $                ELAPSO,
     $                EL    , USTAR , DIFRES
C
      LOGICAL  LPSNOW
C
C--TRACE AND INTERNAL FILE UNIT NUMBERS
C
      COMMON /CNTROL/ NUTRC , NUII  ,
     $                NUBONR, NUBONW, NUCONR, NUCONW,
     $                NUCUMR, NUCUMW, NUSEGR, NUSEGW
C
C--TRACE OPTIONS AND CURRENT LOCATION INDICATORS
C
      COMMON /CNTROL/ IISEG, ISTEP, ICELL, JCELL, KCELL, LCELL,
     $                IPRINT(6)
C
C--DESCRIPTIVE STUFF
C
      COMMON /CNTRL1/ MRUNID(60),     XUTM  , YUTM  , NZONE ,
     $                XORG  , YORG  , NOXG  , NOYG  , NOZG  ,
     $                NVLOW , NVUP  , DZMINL, DZMINU, NDTREF
C
C         MRUNID    A  RUN ID
C         XUTM      R  REFERENCE ORIGIN
C         YUTM      R  REFERENCE ORIGIN
C     COMDECK.FILCON
C-----------------------------------------------------------------------
C
C     *** /FILCON/ CONTAINS ALL FILE CONTROL VARIABLES
C
      COMMON /FILCON1/ NSPMAX, NAM(10), NID(60), MSPNAM(10,35),
     $ NUAQ  , NAMAQ (10), NBDAQ , BTAQ  , NEDAQ , ETAQ  ,
     $   NSAQ  , NSIAQ (35),
     $ NUBDY , NAMBDY(10), NBDBDY, BTBDY , NEDBDY, ETBDY ,
     $   NFRBDY,
     $   NSBDY , NSIBDY(35),
     $ NUCHP , NAMCHP(10),
     $ NUDB  , NAMDB (10), NBDDB , BTDB  , NEDDB , ETDB  ,
     $   NFRDB , TBDB  , TDDB  ,
     $ NUEM  , NAMEM (10), NBDEM , BTEM  , NEDEM , ETEM  ,
     $   NFREM ,
     $   NSEM  , NSIEM (35)
C
      COMMON /FILCON2/
     $ NUMET , NAMMET(10), NBDMET, BTMET , NEDMET, ETMET ,
     $   NFRMET,
     $ NUPTS , NAMPTS(10), NBDPTS, BTPTS , NEDPTS, ETPTS ,
     $   NFRPTS,
     $   NSPTS , NSIPTS(35),
     $ NUTOP , NAMTOP(10), NBDTOP, BTTOP , NEDTOP, ETTOP ,
     $   NFRTOP, TBTOP , TDTOP ,
     $ NURWY , NAMRWY(10), NBDRWY, BTRWY , NEDRWY, ETRWY ,
     $   NFRRWY,
     $   NSRWY , NSIRWY(35),
     $ NUAV  , NAMAV (10), NUDEP
C
      COMMON /FILCON3/
     $ NUCTL , NAMCTL(10),
     $ NUCON , NAMCON(10),
     $ NUTMP , NAMTMP(10), NBDTMP, BTTMP , NEDTMP, ETTMP ,
     $   NFRTMP,
     $ NUTER , NAMTER(10),
     $ NUCT  , NAMCT (10), NBDCT , BTCT  , NEDCT , ETCT  ,
     $   NFRCT ,
     $   NSCT  , NSICT (35),
     $ NUWND , NAMWND(10), NBDWND, BTWND , NEDWND, ETWND ,
     $   NFRWND,
     $ NUVAR , NAMVAR(10)
C
C     COMDECK.SEGTAB
C------------------------------------------------------------------------
C
C     *** /SEGTAB/ CONTAINS VALUES OF SEGMENT TABLE ENTRIES
C                     FOR A PARTICULAR SEGMENT.
C
C                   THESE VALUES ARE SET BY SUBROUTINE SEGSET.
C
      COMMON /SEGTAB/
     $   IORGX,  IORGY,  NOX  ,  NOY  ,
     $   NPMAX,  NOPTS,  NXY  ,  NXYZ ,  NXYZS,  NXYS ,
     $   NBON ,  JSBON,  NCON ,  JSCON,
     $   NCUM ,  JSCUM,  NSCR ,  JSSCR,
     $   ZREF ,  WXMAX,  WYMAX,
     $   WAVW ,  WAVE ,  WAVS ,  WAVN ,
     $   DTMAX,  DT   ,  NDT  ,  ISEQ ,
     $   LEXW ,  LEXE ,  LEXS ,  LEXN ,
     $   JINDW,  JINDE,  JINDS,  JINDN,
     $   JBCW ,  JBCE ,  JBCS ,  JBCN ,
     $   JCTOP,  JCUM ,  JCUMV,
     $   JDBD ,  JDBE ,  JDB1 ,  JDB2 ,
     $   JTOPD,  JTOPE,  JTOP1,  JTOP2,
     $   JWX  ,  JWY  ,  JTEMP,  JRUF ,  JVEG ,
     $   JQT  ,  JQR  ,  JCARM,
     $   JIJPS,  JKPTS,  JQPTS,
     $   JCONC,  JCVAR
C
      EQUIVALENCE (IZREF ,ZREF ), (IWXMAX,WXMAX), (IWYMAX,WYMAX)
      EQUIVALENCE (IWW,WAVW), (IWE,WAVE), (IWS,WAVS), (IWN,WAVN)
      EQUIVALENCE (IDTMAX,DTMAX), (IDT   ,DT   )
C
      LOGICAL LEXW, LEXE, LEXS, LEXN
C
      DIMENSION ISTAB(65)
      EQUIVALENCE (ISTAB, IORGX)
C
C    COMMON /BALANC/
C
C       -- USED FOR KEEPING TRACK OF MASS FLUXES IN AND OUT
C          OF THE MODELED REGION
C
      COMMON /BALANC/ BLFLOW(32,2,4), BUFLOW(32,2,4), TPFLOW(32,2), 
     $                PTFLOW(32), EFLOW(32), DPFLOW(32),
     $                BLFLCU(32,2,4), BUFLCU(32,2,4), TPFLCU(32,2), 
     $                PTFLCU(32), EFLCU(32), DPFLCU(32),
     $                TMAS(32), TMASM(32)
C
C     COMDECK.LOCPTR
C--------------------------------------------------------------------
C
C     *** /LOCPTR/ CONTAINS POINTERS TO LOCAL VARIABLES
C                   USED BY THE INTEGRATION ROUTINES
C
      COMMON /LOCPTR/ NLPTR,
     $  JTH   , JTHNEW, JTHAVG, JHT   , JHTNEW, JHTAVG,
     $  JVD   , JSRC  , JR    ,
     $  JHS1  , JHCS1 , JWS1  , JCS1  , JAS1  , JDELS1,
     $  JAER  , JFACT , JCON  , JCONT , JXKZ  , JFLUX ,
     $  JWZ   , JTHEDG, JWAV  , JDHDT , JDUM  ,
     $  JA    , JB    , JC    , JY    , JX    ,
     $  JCTEST, JZ    , JAOMEG,
     $  JHOLD , JRATE , JYGF  , JGA   , JGF   , JDC
C
      DIMENSION  JLPTR(40)
      EQUIVALENCE (JLPTR,JTH)
C
C     COMDECK.MSCAL
C------------------------------------------------------------------------
C
C     *** /MSCAL/ CONTAINS METEOROLOGICAL SCALARS
C        THEY ARE READ OR CALCULATED IN MSREAD
C
      COMMON /MSCAL/ TGRADB, TGRADA, CE    , FRKEND, H2O   , ATMPRS,
     $               KKAER , AEFACT,
     $               ATFACT, QFACT , TMBEG , TMEND , FRKBEG, FRKDEL,
     $               LDARK ,
     $               FACTRK, METNAM(10,6)
C
      LOGICAL LDARK
      DIMENSION SCAL(6)
      EQUIVALENCE (SCAL, TGRADB)
C

c-----------------------------------------------------------------------
      CHARACTER*60 NAM0(5),FNAME ! input/output file names
      PARAMETER (NI=200,NJ=200,MXSP=90)
      COMMON /MTRX/A1(NI,NJ,MXSP),MTX(0:14)
      parameter(NPOL=14,LDATE=366)
      integer nst
      real,allocatable::x(:),y(:),C(:,:,:,:),B(:,:,:,:)
      real H(24)
      DIMENSION IDATE(LDATE)
      character date*4,YR*2,imo*2,namSt*2,ANAM
      CHARACTER CH_nm*2,A2*2,A3*3
      dimension PM(4),ovm(2,0:11),novm(2,0:11)

      CHARACTER NAMPOL(0:NPOL)*3,NAMMOD(0:NPOL)*10,myr*4
      character*12,allocatable::StNam(:)
      character*4 a4
      character cn
      character*500 aline
      logical lexist
      logical,allocatable::lsteff(:)  

      DATA NAMPOL/'TMP','SO2','CMO','OZN','PMT',
     +  'NOX','P25','NO2','THC','NMH','WSP','WDR','TM2','WST','WPT'/
      DATA NAMMOD/'TEMP_K','SO2','CO','O3','PM10',
     +  'NOX','PM25','NO2','VOC','VOC','UWIND_MpS','VWIND_MpS',
     +  'T2_K','U10_MPS','V10_MPS'/
      PARAMETER (NSP=6)  ! SP. NUM
      integer,allocatable::ISQ(:)     ! STATION COORDINATES (M)

      DATA NUAV/41/

      CHARACTER AD(12)*2
      DATA AD/'31','28','31','30','31','30','31','31'
     +  ,'30','31','30','31'/

      COMMON /BIGV/SPNAM(10,MXSP)
      CHARACTER SPNAM*4,names*10
      LOGICAL LAVRG, LMET3D,LMET2D,LCALMET
      character*4 nam3d(60),MRUNID
      character*4 nam2d(60),CALMET(6)

      open(111,file='abi_inp.txt',status='old')
      read(111,*)nam0(3)
      read(111,*)nam0(1),nam0(2)
      close(111)

      cn=','
      icha=0
      do i=1,60
          if(nam0(3)(i:i).eq.'S') icha=i-2
      enddo
      if(icha.eq.0) then
      do i=1,60-5
        if(nam0(3)(i:i+4).eq.'.avrg')icha=i-1
      enddo
      endif
      if(icha.eq.0) then
      do i=60,1,-1
        if(nam0(3)(i:i).eq.'.')then
          icha=i-1
          exit
        endif
      enddo
      endif

      if(icha.eq.0)then
        write(*,*)'Error00 ',nam0(3)
        stop
      endif

      YR=NAM0(1)(1:2)
      READ(YR,'(I2)')iyr

      READ(NAM0(1)(1:2),*)IYB
      READ(NAM0(1)(3:4),*)IMB
      READ(NAM0(1)(5:6),*)IDB
      READ(NAM0(1)(7:8),*)IHB
      READ(NAM0(2)(1:2),*)IYE
      READ(NAM0(2)(3:4),*)IME
      READ(NAM0(2)(5:6),*)IDE
      READ(NAM0(2)(7:8),*)IHE
      IF(MOD(IYE,4).EQ.0)AD(2)='29'
      JdateB=IYB*100*100+IMB*100+IDB
      JdateE=IYE*100*100+IME*100+IDE
      IF(JdateB*100+IHB.GT.JdateE*100+IHE)then
        write(*,*)'Error, BEGIN TIME->END TIME',jdateB,jdateE
        stop
      ENDIF

      do j=1,60
        if(nam0(3)(j:j).ne.' ')IEND=J
      enddo

      NAM0(4)='BIG_ENDIAN'
      print*,nam0(3)(1:IEND)
      open(NUAV,file=nam0(3)(1:IEND),
     +  form='unformatted',convert=NAM0(4),STATUS='OLD')

      data nam3d    /'3','D','M','E','T',55*' '/
      data nam2d    /'2','D','M','E','T',55*' '/
      data CALMET   /'C','A','L','M','E','T'/

 
      READ (NUAV,END=998) NAMAV, MRUNID, NOSEG, NOSPEC, NDATEe, TTIME,
     $  NDLAST, TTLAST
      NOSEG=1
      do i=1,5
      LMET2D=.false.
      if(MRUNID(i).ne.nam2d(i)) exit
        LMET2D=.true.
      enddo
      do i=1,5
      LMET3D=.false.
      if(MRUNID(i).ne.nam3d(i)) exit
        LMET3D=.true.
      enddo
      LCALMET=.false.
      do i=1,60-6+1
        ipas=1
        do j=i,i+5
          if(MRUNID(j).ne.CALMET(j-i+1))then
            ipas=0
            exit
          endif
        enddo
        if(ipas.eq.1)then
          LCALMET=.true.
          exit
        endif
      enddo
      if(LMET3D.or.LCALMET)LMET3D=.true.
      write(*,*)'nospec=',nospec  !!
      ICAL=JdateB
      CALL juldate(ICAL)
      IBEG=ICAL*100+IHB
      IEND=NDLAST*100+TTLAST
      print*,NDATEe, TTIME,NDLAST, TTLAST,ibeg
      IF(IEND.LT.IBEG) STOP 'REQUIRE BEGINING TIME TOO LATE'
      ICAL=JdateE
      CALL juldate(ICAL)
      IEND=ICAL*100+IHE
      IBEG=NDATEe*100+TTIME
      print*,NDATEe, TTIME,NDLAST, TTLAST,iend
      IF(IEND.LT.IBEG) STOP 'REQUIRE ENDING TIME TOO EARLY'

C**   
      open(21,file='sta_list.txt',
     +  status='old')
      read(21,*)
      nst=0
      do while(.true.)
        read(21,100,end=51)ii,a4,i1,i2,iflag
!       print*,            ii,a4,i1,i2,iflag
        if(iflag.eq.1)then
          nst=nst+1
        endif
      enddo
100   format(i3,5x,a4,t16,i7,t25,i7,t33,i1)
51    continue
c-----Allocate
      allocate(x(nst))
      allocate(y(nst))
      allocate(C(nst,0:24,0:NPOL,ldate)) !0 for temp
      allocate(B(nst,0:24,0:NPOL,ldate))
      allocate(stnam(nst))
      allocate(isq(nst))
      allocate(lsteff(nst))

      i=0
      rewind(21)
      read(21,*)
      do while(.true.)
        read(21,100,end=52)ii,a4,i1,i2,iflag
        if(iflag.eq.1)then
          i=i+1
          StNam(i)(1:4)=a4
          if(i1.lt.0) then
            write(StNam(i)(5:8),'(A1,I3.3)')'-',-i1/1000
          else
            write(StNam(i)(5:8),'(A1,I3.3)')'_',i1/1000
          endif
          if(i2.lt.0) then
            write(StNam(i)(9:12),'(A1,I3.3)')'-',-i2/1000
          else
            write(StNam(i)(9:12),'(A1,I3.3)')'_',i2/1000
          endif
          x(i)=real(i1)
          y(i)=real(i2)
          isq(i)=ii
        endif
        if(ii.eq.999)then
          x(i)=sum(x(:))/nst
          y(i)=sum(y(:))/nst
        endif
      enddo
52    close(21)
      print*,'num of stations: ',i,nst
      IID=0
      DO 98 JDATE=JdateB,JdateE
        ICAL=JDATE
        CALL juldate(ICAL)
        IF(ICAL.LE.0) GOTO 98
        IID=IID+1
        IF(IID.GT.LDATE) STOP 'IID.GT.LDATE'
        IDATE(IID)=JDATE
98    CONTINUE
      MDATE=IID
	print*,MDATE,(IDATE(i),i=1,MDATE)

c-----
C--REGION DESCRIPTION HEADER
      READ (NUAV) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
      NXY=NOXG*NOYG
      IF(NXY.GT.NI*NJ) STOP ' EXCEED DIMENSION'
      IF(NOX.GT.NI) STOP ' EXCEED DIMENSION X'
      IF(NOY.GT.NJ) STOP ' EXCEED DIMENSION Y'
C
C--SEGMENT DESCRIPTION HEADER
      READ (NUAV) ((Idum,J=1,4), I=1, NOSEG)
C
C--SPECIES DESCRIPTION HEADER
      if(NAM0(4)(1:1).eq.'L')
     .  READ (NUAV) ((MSPEC(I,J), I=1,10), J=1,NOSPEC)
      if(NAM0(4)(1:1).eq.'B')
     .  READ (NUAV) ((SPNAM(I,J), I=1,10), J=1,NOSPEC)
      MTX=0
      data MTX /   3,0 ,    0 ,   0 ,   0 ,   0 ,  
     +  0 ,  0 ,   0,     4,    5,    6,7,5,6/ !(u &v)
      do j=1,nospec
            MTXL=-1
        do i=1,10
          names(i:i)=spnam(i,j)(1:1)
        enddo
        do L=0,NPOL
          if(trim(names).eq.trim(NAMMOD(L))) then
            MTX(L)=j
            exit
          endif
        enddo
        do  L=0,NPOL
          if(MTX(L).eq.j) MTXL=L
        enddo
        write(*,*)(spnam(i,j),i=1,10),MTXL  !!
      enddo
	print*,MTX

c      PRINT*,'PASS1'
      PRINT*,'PASS2',NOZ
      do while(.true.)
        READ (NUAV,END=998) NDATE1, TAVE1, NDATEe, TAVE
        julhr=MOD(NDATE1,1000)*100+TAVE1
        DO  L=1,NOSPEC
          READ (NUAV)ISEG,(MSPEC(I,L),I=1,10),
     +      ((A1(I,J,L),I=1,NOXG), J=1,NOYG)
          IF(NOZ.GE.2) THEN
            DO K=2,NOZ
              READ (NUAV)
            ENDDO !LOOP K
          ENDIF
        ENDDO !LOOP SPECIES

        idate1=NDATE1 !endding time and date
        call caldate(idate1)
        IF(idate1*100+TAVE1.LT.IDATE(1)*100+IHB)then  !NOT YET
        write(*,*)NDATE1, TAVE1, NDATEe, TAVE, 'not yet'
          cycle
        ELSEIF(idate1*100+TAVE.GT.IDATE(MDATE)*100+IHE+1)then  !END OF REQUIREMENT
        write(*,*)NDATE1, TAVE1, NDATEe, TAVE ,'exiting 1'
          exit
        endif

        K=0
        idate1=NDATE1 !endding time and date
        call caldate(idate1)
        DO I=1,MDATE
          IF(idate1.EQ.IDATE(I)) K=I
        ENDDO
        IF(K.eq.0) then
        print*,idate1
        stop 'not search K'
        endif
        IH=nint(TAVE1)
c        print*,IH
        IF(K.EQ.1.AND.IH.LT.IHB)then  !NOT YET
          cycle
        elseIF(julhr.GT.IEND)then  !!END OF REQUIREMENT
        write(*,*)NDATE1, TAVE1, NDATEe, TAVE ,'exiting 2'
          exit
        endif
        write(*,*)NDATE1, TAVE1, NDATEe, TAVE

        do jst=1,nst
          XD=X(jst)
          YD=Y(jst)
          IX=(XD-XORG)/DELTAX+1
          IY=(YD-YORG)/DELTAY+1
          if((IX-1)*(IX-(NOXG)).GE.0)cycle
          if((IY-1)*(IY-(NOYG)).GE.0)cycle
          Xo=(IX-1)*DELTAX+XORG
          Yo=(IY-1)*DELTAY+YORG
          XRf=(Xd-Xo)/DELTAX
          YRf=(Yd-Yo)/DELTAY
          if((.not.LMET3D).and.(.not.LMET2D)) then
            DO L=1,8
	      if(MTX(L).eq.0)cycle
              B(JST,IH,L,K)=StVal(IX,IY,L,XRf,YRf)
            ENDDO
          else
            if(LMET3D)then
              B(JST,IH, 0,K)=StVal(IX,IY,0,XRf,YRf)-273.
              uum=StVal(IX,IY,10,XRf,YRf)
              vvm=StVal(IX,IY,11,XRf,YRf)
            elseif(LMET2D)then
              B(JST,IH, 0,K)=StVal(IX,IY,12,XRf,YRf)-273.
              uum=StVal(IX,IY,13,XRf,YRf)
              vvm=StVal(IX,IY,14,XRf,YRf)
            endif
              call UV2WsWd(uum,vvm,WSm,WDm)
              B(JST,IH,10,K)=WSm
              B(JST,IH,11,K)=WDm
          endif
        enddo !NST
      enddo  !next hour
998   CLOSE(NUAV)
	print*,'closing',NUAV,'LMET3D=',LMET3D,'LMET2D=',LMET2D
      lsteff=.true.
      do j=1,nst
        if(abs(maxval(B(j,:,:,:))).eq.0.)then
          lsteff(j)=.false.  
        else
          iii=iii+1
        endif
      enddo
      print*,lsteff

c-----
      DO IYM=IYB*100+IMB,IYE*100+IME
        IY=IYM/100
        write(YR,'(I2.2)')IY
        myr='20'//YR
        IF(MOD(IY,4).EQ.0)AD(2)='29'
        IM=MOD(IYM,100)
        if(IM.lt.1.or.IM.gt.12) cycle
        IMO=CHAR(IM/10+48)//CHAR(MOD(IM,10)+48)
        do jst=1,nst
          if(.not.lsteff(jst))then  
            cycle
          endif
         if(isq(jst).ne.999) then
          write(A3,'(i3.3)')isq(jst)
          WRITE(*,*)'o:/users/4139/epa/'
     +      //myr//'/hs'//YR//IMO//AD(IM)//'.'//A3

          Open(1,file=
     +      '/st1/data/epa/'//myr//'/HS'//YR//IMO//AD(IM)//'.'
     +      //A3,STATUS='OLD',iostat=iio)
          if(iio.ne.0)then
            Open(1,file=
     +        '/st1/data/epa/'//myr//'/hs'//YR//IMO//AD(IM)//'.'
     +        //A3,STATUS='OLD',err=99)
           endif
 11       if (isq(jst) .lt. 600) then
            read(1,*,end=99)ist,ANAM, ipollu,idat2,(H(I),i=1,24)
          else
            read(1,*,end=99)ist,      ipollu,idat2,(H(I),i=1,24)
          endif
	  idat2=mod(idat2,1000000)
	  if(sum(H).eq.0)print*,ist,ANAM,ipollu,idate2
  5       format(I3,9x,i2,4x,i6,24(1x,f6.0))
          IF(IST.NE.isq(JST)) then
                print*,IST,'.NE.',isq(JST),idat2
                STOP 'Error01'
          endif
          IGG=1
          DO K=0,NPOL
	    KK=K
	    IF(K.eq.0)KK=14 ! temp_c
	    IF(K.eq.6)KK=33 ! NO ->PM2.5
            IF(IPOLLU.EQ.KK) IGG=0
          ENDDO
C         write(*,5)ist, ipollu,idat2,(H(I),i=1,24)

          IF(IGG.EQ.1) GOTO 11
          IF(IDAT2.LT.IDATE(1)    ) GOTO 11
          IF(IDAT2.GT.IDATE(MDATE)) GOTO 11
          M=0
          DO I=1,MDATE
            IF(IDAT2.EQ.IDATE(I)) M=I
          ENDDO
          if(M.eq.0)then
            print*,IDAT2
            stop
          endif
          K=IPOLLU
	  IF(K.eq.14)K=0 ! temp_c
	  IF(K.eq.33)K=6 ! NO ->PM2.5
          DO I=1,24
            ih=i-1
            if(h(i).lt.0..and.K.ne.0)then
              C(JST,ih,K,M)=-99.
            else
              if(K.eq.10) then
		C(JST,ih,K,M)=H(I)
	      else
              C(JST,ih,K,M)=H(I)
		endif
            endif
          ENDDO
          GOTO 11
99        CLOSE(1)
         else ! st=999 (average among all station)
          DO M=1,MDATE
          DO K=1,11
          do ih=0,23
           jss=0
           sumb=0
           sumc=0
           do jj=1,nst-1
            if(.not.lsteff(jj))cycle
            if(C(jj,ih,K,M).le.0) cycle       
            jss=jss+1 
            sumc=sumc+C(jj,ih,K,M)
            sumb=sumb+B(jj,ih,K,M)
           enddo !jj
           if(jss.eq.0) then
            C(JST,ih,K,M)=0.
            B(JST,ih,K,M)=0.
           else
            C(JST,ih,K,M)=sumc/jss
            B(JST,ih,K,M)=sumb/jss
           endif
          enddo 
          enddo 
          enddo 
         endif
        ENDDO !NEXT STATION
      ENDDO !NEXT MONTH
        if(.not.LMET2D)B(:,:,10,:)=B(:,:,10,:)/1.26 !(50/10)^(1/7)
c**   calculate the day-average
      do i=1,nst
        do l=0,NPOL
          do ld=1,ldate
            ic=0
            ib=0
            do ih=0,23
              if(C(i,ih,l,ld).gt.0) ic=ic+1
              if(B(i,ih,l,ld).gt.0) ib=ib+1
            enddo
            if(ic*ib.le.0) cycle
            C(i,24,l,ld)=sum(C(i,0:23,l,ld),mask=C(i,0:23,l,ld).gt.0)/ic
            B(i,24,l,ld)=sum(B(i,0:23,l,ld),mask=B(i,0:23,l,ld).gt.0)/ib
          enddo
        enddo
      enddo
      l=3 !ozone daily max
      do i=1,nst
        do ld=1,ldate
          C(i,24,l,ld)=maxval(C(i,0:23,l,ld))
          B(i,24,l,ld)=maxval(B(i,0:23,l,ld))
        enddo
      enddo

C**
C**   WRITE THE TIME SERIES FILE
C**
      ICAL=IDATE(1)
      CALL juldate(ICAL)
      IY=ICAL/1000.
      JULI=ICAL-IY*1000.
      IH=JULI/100
      ID=(JULI-IH*100.)/10
      IN= JULI-IH*100.-ID*10.
      IH=IH+48
      ID=ID+48
      IN=IN+48
      OPEN(1,FILE='ovm_'//nam0(3)(1:icha)//'.csv',STATUS='UNKNOWN')
      OPEN(2,FILE='ovd_'//nam0(3)(1:icha)//'.csv',STATUS='UNKNOWN')
      OPEN(11,FILE='ovm.dat',STATUS='UNKNOWN')  
      OPEN(12,FILE='ovd.dat',STATUS='UNKNOWN')  
      WRITE(11,201)nst,'NAME','JuliHr','CalDat',(NAMPOL(K),K=1,11),
     +  (NAMPOL(K),K=1,11)
      WRITE(12,201)nst,'NAME','JuliHr','CalDat',(NAMPOL(K),K=1,11),
     +  (NAMPOL(K),K=1,11)
      aline='ID,NAME,JuliHr,CalDat,TMP,SO2,CMO,OZN,PMT,NOX,P25,NO2,'//
     +  'THC,NMH,WSP,WDR,TMP,SO2,CMO,OZN,PMT,NOX,P25,NO2,NMH,THC,'//
     +  'WSP,WDR'
      write(1,'(a200)')aline
      write(2,'(a200)')aline

201   FORMAT(I3,A4,a8,1x,a6,22(4X,A3))

      DO J=1,NST
c----
        if(.not.lsteff(j))then  
          cycle
        endif

        DO M=1,MDATE
          ICAL = IDATE(M)
          CALL juldate(ICAL)
          IY=ICAL/1000.
          ICAL=ICAL-IY*1000.
          DO I=0,23
            IF(M.EQ.1.AND.I.LT.IHB) GOTO 202        !NOT YET
            IF(M.EQ.MDATE.AND.I.GT.IHE) GOTO 202    !!END OF REQUIREMENT
            JULI=ICAL*100.+I
            WS=C(J,I,10,M) *1.26 !(50/10)^(1/7)
            WD=C(J,I,11,M)
c            WD=180-WD
            IF(WD.LT.0)WD=WD+360
            if(wd.gt.360.)then
              wd=-99.
            endif
c               nox reset at 3:00
             hi=C(J,i,6,M)
            if(hi.lt.0..and.i.eq.3)then
              C(J,i,5,M)=(C(j,i-1,5,m)+C(j,i+1,5,m))/2.
              C(J,i,6,M)=(C(j,i-1,6,m)+C(j,i+1,6,m))/2.
              C(J,i,7,M)=(C(j,i-1,7,m)+C(j,i+1,7,m))/2.
            endif
c-----PPM->PPB
            if(c(j,i,8,m).eq.0.)then  !THC
              c(j,i,8,m)=-99.
            else
              C(J,I,8,M)=C(J,I,8,M)*1000.
            endif
            if(c(j,i,9,m).eq.0.)then  !NMHC
              c(j,i,9,m)=-99.
            else
              C(J,I,9,M)=C(J,I,9,M)*1000.
            endif
            if(I.eq.23) then
            WRITE(12,300)ISQ(J),StNam(J),JULI,mod(IDATE(M),10000),24,
     +        (C(J,24,K,M),K=1,9),WS
     +        ,WD,(B(J,24,K,M),K=1,8)
            WRITE(2,200)
     +        ISQ(J),cn,StNam(J),cn,JULI,cn,mod(IDATE(M),10000),24,
     +        (cn,C(J,24,K,M),K=0,9),cn,WS,cn
     +        ,WD,(cn,B(J,24,K,M),K=0,11)
            endif
            WRITE(11,300)ISQ(J),StNam(J),JULI,mod(IDATE(M),10000),i,
     +        (C(J,I,K,M),K=1,9),WS
     +        ,WD,(B(J,I,K,M),K=1,8)
            WRITE(1,200)
     +        ISQ(J),cn,StNam(J),cn,JULI,cn,mod(IDATE(M),10000),i,
     +        (cn,C(J,I,K,M),K=0,9),cn,WS,cn
     +        ,WD,(cn,B(J,I,K,M),K=0,11)
300        FORMAT(I3,A12,I8,1x,I4.4,i2.2,7F7.1,2f8.0,9f7.1,f8.0)
200        FORMAT(I3,a1,A12,a1,I8,a1,I4.4,i2.2,24(a1,F9.1))
202        CONTINUE
          ENDDO !NEXT HR
        ENDDO !LOOP FOR DAY
      ENDDO ! LOOP FOR STATION
      close(1)
      close(2)
      close(12)
      if(.not.(LMET3D.or.LMET2D)) then
      write(*,*)'Running abi_camx.exe...'
      result=system('abi_camx.x '//nam0(3)(1:icha))
      endif

      if(LMET3D.or.LMET2D) then
      OPEN(12,FILE='ovmMET.dat',STATUS='UNKNOWN')  
      WRITE(12,201)nst,'NAME','JuliHr','CalDat',(NAMPOL(0),
     +  (NAMPOL(K),K=10,11),KK=1,2)
      DO J=1,NST
c-----
        if(.not.lsteff(j))then  
          cycle
        endif

        DO M=1,MDATE
          ICAL = IDATE(M)
          CALL juldate(ICAL)
          IY=ICAL/1000.
          ICAL=ICAL-IY*1000.
          DO I=0,23
            IF(M.EQ.1.AND.I.LT.IHB) GOTO 203        !NOT YET
            IF(M.EQ.MDATE.AND.I.GT.IHE) GOTO 203    !!END OF REQUIREMENT
            JULI=ICAL*100.+I
            WS=C(J,I,10,M)
            WD=C(J,I,11,M)
c            WD=180-WD
            IF(WD.LT.0)WD=WD+360
            if(wd.gt.360.)then
              wd=-99.
            endif
            WRITE(12,300)ISQ(J),StNam(J),JULI,mod(IDATE(M),10000),i,
     +      C(J,I,0,M),WS,WD,B(J,I,0,M),(B(J,I,K,M),K=10,11)
203        CONTINUE
        ENDDO !I
        ENDDO !M
        ENDDO !J
        close(12)
        result=system('abi_met.x '//nam0(3)(1:icha))
      endif

      OPEN(1,FILE='avg_'//nam0(3)(1:icha)//'.csv',STATUS='UNKNOWN')
      DO M=1,MDATE
      DO I=0,23
        ovm=0.    
        novm=0.    
        if(maxval(B(:,I,:,M)).eq.0.)cycle
        IF(M.EQ.1.AND.I.LT.IHB) cycle        !NOT YET
        IF(M.EQ.MDATE.AND.I.GT.IHE) cycle    !END OF REQUIREMENT
      DO J=1,NST
            WS=C(J,I,10,M)
            WD=C(J,I,11,M)
            theta=(270.-WD)/180.*3.14159
            C(J,I,10,M)=WS*cos(theta)
            C(J,I,11,M)=WS*sin(theta)
            WS=B(J,I,10,M)
            WD=B(J,I,11,M)
            theta=(270.-WD)/180.*3.14159
            B(J,I,10,M)=WS*cos(theta)
            B(J,I,11,M)=WS*sin(theta)
      ENDDO
      DO J=1,NST
c-----
      if(.not.lsteff(j))cycle
      DO K=0,11
          ovm(2,K)=ovm(2,K)+B(J,I,K,M)
          novm(2,K)=novm(2,K)+1
          if(K.lt.10.and.c(J,I,K,M).lt.0)cycle
          ovm(1,K)=ovm(1,K)+c(J,I,K,M)
          novm(1,K)=novm(1,K)+1
      ENDDO
      ENDDO
        DO L=1,2
        DO K=0,11
          if(novm(L,K).eq.0) cycle
          ovm(L,K)=ovm(L,K)/novm(L,K)
        enddo
              call UV2WsWd(ovm(L,10),ovm(L,11),WS,WD)
              ovm(L,10)=WS
              ovm(L,11)=WD
        enddo
        idatehr=mod(IDATE(M),10000)*100+i      
            WRITE(1,301)idatehr,
     +        ((cn,ovm(L,K),K=0,11),L=1,2)
301        FORMAT(i6.6,24(a1,F9.1))
      ENDDO
      ENDDO
      DO I=0,23
        ovm=0.    
        novm=0.    
      DO M=1,MDATE
        if(maxval(B(:,I,:,M)).eq.0.)cycle
        IF(M.EQ.1.AND.I.LT.IHB) cycle        !NOT YET
        IF(M.EQ.MDATE.AND.I.GT.IHE) cycle    !END OF REQUIREMENT
      DO J=1,NST
c-----
      if(.not.lsteff(j))cycle
      DO K=0,11
          ovm(2,K)=ovm(2,K)+B(J,I,K,M)
          novm(2,K)=novm(2,K)+1
          if(K.lt.10.and.c(J,I,K,M).lt.0)cycle
          ovm(1,K)=ovm(1,K)+c(J,I,K,M)
          novm(1,K)=novm(1,K)+1
      ENDDO
      ENDDO
      ENDDO
        DO L=1,2
        DO K=0,11
          if(novm(L,K).eq.0) cycle
          ovm(L,K)=ovm(L,K)/novm(L,K)
        enddo
              call UV2WsWd(ovm(L,10),ovm(L,11),WS,WD)
              ovm(L,10)=WS
              ovm(L,11)=WD
        enddo
            WRITE(1,301)i,
     +        ((cn,ovm(L,K),K=0,11),L=1,2)
      ENDDO
      close(1)
      END
c-------------------------------------------------------------
      subroutine juldate(idate)
      dimension nday(12)
      data nday/31,28,31,30,31,30,31,31,30,31,30,31/
c
c-----Entry point
c
      iyear = idate/10000
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29

      imonth = (idate - iyear*10000)/100
      iday = idate - iyear*10000 - imonth*100
      IF(imonth.gt.12.or.imonth.eq.0.or.
     +   IDAY.GT.NDAY(IMONTH).OR.IDAY.LE.0) THEN
        IDATE=-1
        RETURN
      ENDIF
c
      mday = 0
      do 10 n = 1,imonth-1
        mday = mday + nday(n)
 10   continue
      jday = mday + iday
      idate = iyear*1000 + jday
c
      return
      end
c----------------------------------------------------------------
      function StVal(IX,IY,L,XRf,YRf)
      PARAMETER (NI=200,NJ=200,MXSP=90)
      COMMON /MTRX/A1(NI,NJ,MXSP),MTX(0:14)
      DIMENSION A(4)
!            1   2    3    4   5    6     7   8 
!           O3  NO2  SO2  VOC PM25 PM10   NO PM2ND (L=8,after shrink
!     DATA NAMPOL/'SO2','CMO','OZN','PMT','NOX',
!    +'P25','NO2','THC','NMH','WSP','WDR'/
      K=1
      ISP=MTX(L) !L=0, for temp_K in 3dMET file(location 3)
!3d   1ZGRID_M   2PRESS_MB   3TEMP_K   4HUMID_PPM   5UWIND_MpS
!6VWIND_MpS
!2d   1TSURF_K   2SNOWCOVER   3PRATE_MMpH   4CLOUD_OD   5U10_MpS
!   6V10_MpS   7T2_K   8SWSFC_WpM2   9PBL_WRF_M  10PBL_OB70_M
      if(ISP.eq.0) then
        StVal=0.
        return
      endif
      A=0
      DO I=IX,IX+1
        DO J=IY,IY+1
            A(K)=A1(I,J,ISP)
          K=K+1
        ENDDO
      ENDDO
      u11=a(1)*(1.-YRf)+a(2)*YRf
      u12=a(3)*(1.-YRf)+a(4)*YRf
      StVal=U11*(1.-XRf)+U12*XRf
      return
      end
c---------------------------------------------------------------------
      subroutine caldate(idate)
c  
c-----CAMx v3.10 020410
c  
c     CALDATE converts date from Julian (YYJJJ) format to calender
c     (YYMMDD) format
c                            
c     Copyright 1996, 1997, 1998, 1999, 2000, 2001, 2002
c     ENVIRON International Corporation
c            
c     Modifications:  
c        none
c  
c     Input arguments:  
c        idate               julian date (YYJJJ)  
c              
c     Output arguments:  
c        idate               calender date (YYMMDD)  
c              
c     Routines Called:  
c        none
c              
c     Called by:  
c        AREAPREP  
c        BNDPREP
c        CNCPREP
c        DRYDEP
c        PIGPREP
c        RDPTHDR
c        READZP
c        STARTUP
c
      dimension nday(12)
      data nday/31,28,31,30,31,30,31,31,30,31,30,31/
c
c-----Entry point
c
c-----If it is already in calender date, return
c
      if (idate.gt.100000) goto 9999
      iyear = idate/1000
      jday = idate - iyear*1000
c
      nday(2) = 28
      if (mod(iyear,4).eq.0) nday(2) = 29
      mday = 0
      do 10 imonth = 1,12
        mday = mday + nday(imonth)
        if (mday.ge.jday) go to 20
 10   continue
 20   iday = jday - (mday - nday(imonth))
      idate = iyear*10000 + imonth*100 + iday
c
 9999 return
      end
	subroutine UV2WsWd(wu,wv,ws,wd)
      pi=acos(-1.)
      ws=sqrt(wu**2+wv**2)
      if (ws.eq.0)then
          wd=0.
          return
      endif
      ang=wv/ws
      if (abs(ang).le.10e-5) then
         ang=0
      endif
      if (wu.ge.0 .and. wv.ge.0) then
         wd=asin(ang)*180./pi-90.
      endif
      if (wu.lt.0 .and. wv.ge.0) then
         wd=-asin(ang)*180./pi+90.
      endif
      if (wu.lt.0 .and. wv.lt.0) then
         wd=asin(-ang)*180./pi+90.
      endif
      if (wu.ge.0 .and. wv.lt.0) then
         wd=-asin(-ang)*180./pi-90.
      endif
          WD=-WD-180.
          if(WD.lt.0) WD=WD+360.
	return
	end
