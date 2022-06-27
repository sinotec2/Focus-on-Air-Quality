c this routine calculate maximun of average of fields, and OP AS A ARG FILE
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
      character*4 note(60)
      integer,allocatable::ndate2(:),ndlast2(:)
      integer SDATE,EDATE
      real,allocatable::ttime2(:),ttlast2(:)
      real,allocatable:: A1(:,:,:,:),tm(:,:,:)

      NUAV=41
      narg=iARGc ()
      if(narg.ne.1)stop  'input avrg_file '
      do i=1,narg
        call getarg(i,nam0(i))
      enddo
      narg=2
      nam0(2)=trim(nam0(1))//'M'
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
       do ird=1,nfile
C
C--REGION DESCRIPTION HEADER
        READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
!      print*, XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
!    $      NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU

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
      READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
!       print*, ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
        nt=0
      do
        READ (ird+10,END=30,err=30)i1,t1,i2,t2
!       print*,i1,t1,i2,t2
        DO  L=1,NOSPEC
          DO  K=1,NOZ
            READ(10+ird,err=30)
          enddo !k
        enddo !l
        nt=nt+1
      enddo !it
C
C         FIRST, WRITE TIME INTERVAL
C
30    rewind(IRD+10)
      do i=1,4
        read(IRD+10)
      enddo
      ENDDO ! next IRD input file
      NXY=NOXG*NOYG
      allocate(tm(NXY,NOZ,NOSPEC))
      allocate(A1(NXY,NOZ,NOSPEC,NT))
      ird=1
      do it=1,nt
        READ (ird+10,END=31,err=31)i1,t1,i2,t2
        DO  L=1,NOSPEC
          DO  K=1,NOZ
            READ(10+ird,err=31)ISEG,(SPNAME(I,L),I=1,10),A1(:,k,l,it)
          ENDDO
        ENDDO
      ENDDO
      print*,'normal end'
      goto 32
31    print*,'wrong NT'
32    continue
      NOZ=11
      SDATE=19365
      EDATE=21001
      TTIME=TTIME2(1)
      print*,NDATE2(1),NDLAST2(1),SDATE,EDATE
      write(iout) fname, note, NOSEG, NOSPEC, SDATE, TTIME,
     $ EDATE, TTIME
      print*,NDATE2(1),NDLAST2(1),SDATE,EDATE
      write(narg+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
      write(iout)1,1,NOXG,NOYG
      write(iout)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      write(iout) SDATE, TTIME, EDATE, TTIME
      DO  L=1,NOSPEC
       DO  K=1,NOZ
        write(iout)ISEG,(SPNAME(I,L),I=1,10),(A1(I,k,l,1),I=1,NXY)
       enddo !k
      enddo !l
      end
