cat ~/bin/multavrg.f
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
      integer itmp(4),nti(2)
      character*4,allocatable:: SPNAME(:,:)
      CHARACTER*60 NAM0(fmax) ! input/output file names
      character*4 fname(10)
      character note(60)*4,names*10
      logical O3,GRD
      integer,allocatable::ndate2(:),ndlast2(:)
      real,allocatable::ttime2(:),ttlast2(:)
      real,allocatable:: A1(:,:,:,:),tim(:,:)
      real,allocatable:: tm(:,:,:)
      integer,allocatable:: yyjul(:,:)
      real SCR(40000),r(4),mult
      NUAV=41
      narg=iARGc ()
      if(narg.ne.2)stop  'Multiply avrg_File mult'

      do i=1,narg
        call getarg(i,nam0(i))
      enddo
      narg=2
      read(nam0(2),*)mult
      nam0(2)=trim(nam0(1))//trim(nam0(2))
      do i=1,narg
          open(i+10,file=trim(nam0(i)),
     +      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
        print*,trim(nam0(i))
      enddo
      nfile=narg-1
      iout=narg+10

      allocate(ndate2(nfile))
      allocate(ndlast2(nfile))
      allocate(ttime2(nfile))
      allocate(ttlast2(nfile))
      DO IRD=1,nfile
        READ (IRD+10) fname, note, NOSEG, NOSPEC,
     +    NDATE2(ird), TTIME2(ird),
     $    NDLAST2(ird), TTLAST2(ird)
       enddo
      allocate(SPNAME(10,NOSPEC))
       ndate=minval(ndate2)
       ndlast=maxval(ndlast2)
       ttime=minval(ttime2)
       ttlast=maxval(ttlast2)
       numHr=(ndlast-ndate)*24+(ttlast-ttime)

       do ird=1,nfile
C
C--REGION DESCRIPTION HEADER
        READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
!       print*, XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY

!       if(ird.eq.1)then
!         write(*,*) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
!    $      NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
!       endif
C
C--SEGMENT DESCRIPTION HEADER
        READ (IRD+10) (Itmp(j), J=1,4)
!       print*, (Itmp(j), J=1,4)
C
C--SPECIES DESCRIPTION HEADER
        nti(IRD)=0
        READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
        print*, ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
        do
          READ (ird+10,END=30,err=30)i1,t1,i2,t2
!       print*,i1,t1,i2,t2
          DO  L=1,NOSPEC
            DO  K=1,NOZ
              READ (ird+10,END=30,err=30)
            enddo !k
          enddo !l
        nti(IRD)=nti(IRD)+1
        enddo !it
C
C         FIRST, WRITE TIME INTERVAL
C
30    rewind(IRD+10)
      do i=1,4!skip the header
              READ(10+ird)
      enddo
      ENDDO ! next IRD input file
      NXY=NOXG*NOYG
      NT=nti(1)!(NDLAST-NDATE)*24+(TTLAST-TTIME)
      allocate(A1(NXY,NOZ,NOSPEC,NT))
      allocate(tm(NXY,NOZ,NOSPEC))
      allocate(yyjul(2,NT),tim(2,NT))
      do  ird=1,nfile
        icount=0
        do it=1,NT
          READ (ird+10,END=33,err=33) yyjul(1,it),tim(1,it), yyjul(2,it),tim(2,it)
          DO  L=1,NOSPEC
            DO  K=1,NOZ
              READ(10+ird,err=33)ISEG,(MSPEC(I,L),I=1,10),A1(:,k,l,it)
            enddo !k
          enddo !l
          icount=icount+1
        enddo !it
      enddo !ird
      goto 34
33    print*,'end of file'
34    if(NT.ne.icount) stop 'NT not right'
      A1=A1*mult
      ird=narg+10
      write(narg+10) fname, note, NOSEG, NOSPEC, NDATE, TTIME,
     $  NDLAST, TTLAST
      write(narg+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
       write(narg+10)1,1,NOXG,NOYG
       write(narg+10)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      do it=1,NT
      write(ird)(yyjul(i,it),tim(i,it),i=1,2)
      DO  L=1,NOSPEC
       DO  K=1,NOZ
        write(ird)ISEG,(SPNAME(I,L),I=1,10),A1(:,k,l,it)
       enddo !k
      enddo !l
      enddo !it
      end
