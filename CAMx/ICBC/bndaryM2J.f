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
      integer itmp(4),IND(4,300),NCEL(4)
      character*4,allocatable:: SPNAME(:,:)
      CHARACTER*60 NAM0(fmax) ! input/output file names
      character*4 fname(10)
      character note(60)*4,names*10
      logical O3,GRD
      integer,allocatable::ndate2(:),ndlast2(:)
      real,allocatable::ttime2(:),ttlast2(:)
      real,allocatable:: BC(:,:,:),tim(:,:)
      real,allocatable:: tm(:,:,:)
      integer,allocatable:: yyjul(:,:),tbeg(:),tend(:)
      real SCR(40000),r(4)
      NUAV=41
      narg=iARGc ()
      if(narg.ne.1)stop
     + 'bndary to bndary.JJJ/yyjjj'

      do i=1,narg
        call getarg(i,nam0(i))
      enddo
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
     $    NOXG, NOYG, NOZ
     $                  ,idproj,istag,tlat1,tlat2,rdum

C
C--SEGMENT DESCRIPTION HEADER
        READ (IRD+10) (Itmp(j), J=1,4)
C
C--SPECIES DESCRIPTION HEADER
        READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      DO 100 N=1,4
       READ(11) NOSEG, NEDG, NCEL(N),((IND(N,J),i,i,i),J=1,NCEL(N))
100    CONTINUE

        nt=0
        do
          READ (ird+10,END=30,err=30)i1,t1,i2,t2
          if(nt.eq.0) then
          i0=i1
          t0=t1
          endif
!       print*,i1,t1,i2,t2
          DO  L=1,NOSPEC
            DO  K=1,4
              READ (ird+10,END=30,err=30)
            enddo !k
          enddo !l
        nt=nt+1
        enddo !it
C
C         FIRST, WRITE TIME INTERVAL
C
30    rewind(IRD+10)
      do i=1,8!skip the header
              READ(10+ird)
      enddo
      NXY=NOXG*NOYG
      allocate(BC(NXY,NOZ,NOSPEC))
      allocate(tm(NXY,NOZ,NOSPEC))
       open(12,file=trim(nam0(1))//'M',
     + form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
       jjj=19365
       jjn=21001
       NOZ2=11
       btime=TTIME
       etime=TTIME
      write(12) fname, note, NOSEG, NOSPEC, jjj, btime,
     $  jjn, etime
      write(12) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $  NOXG, NOYG, NOZ2
     $                  ,idproj,istag,tlat1,tlat2,rdum
       write(12)1,1,NOXG,NOYG
       write(12)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      DO N=1,4
       WRITE(12)NOSEG,N,NCEL(N),((IND(N,J),0,0,0),J=1,NCEL(N))
      enddo
       nend=24
       if(jjj.eq.NDLAST)nend=etime
       do it=1,1
          READ (11,END=33,err=33)
          WRITE(12) jjj,btime, jjn,etime
         DO L=1,NOSPEC
         DO NEDG=1,4
            nc=NOYG
            if(NEDG.gt.2)nc=NOXG
            READ(11) NOSEG, (SPNAME(I,L),I=1,10), NDG,
     $        ((BC(I,K,L), K=1,NOZ), I=1,NC)
            WRITE (12) NOSEG, (SPNAME(I,L),I=1,10), NDG,
     $        ((BC(I,K,L), K=1,NOZ2), I=1,NC)
         enddo
         enddo
        enddo !it
        do L=1,NOSPEC*4+1
          backspace(11)
        enddo
        close(12)
      goto 34
33    print*,'end of file'
34    close(11)
      end

