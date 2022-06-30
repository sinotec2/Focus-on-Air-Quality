Ckuang@master /nas2/camxruns
C$ more ./2013/ICBC/bndextr/bndv5V.f
c this routine modify bc condition file
       INCLUDE  'PARAMS.CMD'
       INCLUDE  'CHPARM.CMD'
       INCLUDE  'CNTROL.CMD'
       INCLUDE  'FILCON.CMD'
       INCLUDE  'SEGTAB.CMD'
       INCLUDE  'NETDEP.CMD'
       INCLUDE  'BALANC.CMD'
       INCLUDE  'LOCPTR.CMD'
       INCLUDE  'MSCAL.CMD'
      integer Itmp(4),IND(4,300),NCEL(4)
      character*4,allocatable:: SPNAME(:,:)
      CHARACTER*60 NAM0(1) ! input file names
      character*4 fname(10)
      character note(60)*4,name*10
      real,allocatable::BC(:,:,:)
      real total(100)
      real ratio

      narg=iARGc ()
      if(narg.ne.1)stop

      call getarg(1,nam0(1))

      open(11,file=trim(nam0(1)),
     +     form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
      print*,trim(nam0(1))

      open(12,file=trim(nam0(1))//'.v5V',
     +     form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')

      READ (11) fname, note, NOSEG, NOSPEC, NDATE, TTIME, NDLAST, TTLAST
      allocate(SPNAME(10,NOSPEC))

C--REGION DESCRIPTION HEADER
      READ (11) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG,NOYG,NOZ,idproj,istag,tlat1,tlat2,rdum

C--SEGMENT DESCRIPTION HEADER
      READ (11) (Itmp(j), J=1,4)

C--SPECIES DESCRIPTION HEADER
      READ (11) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)

      DO N=1,4
       READ(11) NOSEG, NEDG, NCEL(N),((IND(N,J),i,i,i),J=1,NCEL(N))
      enddo

      write(12) fname, note, NOSEG, NOSPEC, NDATE, TTIME, NDLAST, TTLAST
      write(12) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG,NOYG,NOZ,idproj,istag,tlat1,tlat2,rdum
      write(12)1,1,NOXG,NOYG
      write(12)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      DO N=1,4
       WRITE(12)NOSEG,N,NCEL(N),((IND(N,J),0,0,0),J=1,NCEL(N))
      enddo

      NXY=NOXG*NOYG
      allocate(BC(NXY,NOZ,NOSPEC))

C--Time loop
      do while(.true.)
       read(11,end=20)i1,t1,i2,t2
       write(12)      i1,t1,i2,t2
       do L=1,NOSPEC
         do NEDG=1,4
           NC=NOYG !east and west side
           if(NEDG.ge.3) NC=NOXG !south and north side
           READ(11)  NOSEG, (SPNAME(I,L),I=1,10), NDG,
     $        ((BC(I,K,L), K=1,NOZ), I=1,NC)
c           do i=1,10
c             name(i:i)=SPNAME(I,L)(1:1)
c           enddo
c          !calculate total value to determine ratio
c           if(L.ge.1.and.L.le.60) then
c            do I=1,NC
c             do k=1,NOZ
c              total(L)=total(L)+BC(I,K,L)
c              total(100)=total(100)+BC(I,K,L)
c             enddo
c            enddo
c           endif

c           if(L.eq.14) then !PAR
            do I=1,NC
             do K=1,NOZ
              if(L.eq.14) BC(I,K,L)=BC(I,K,L)+0.04 !PAR
              if(L.eq.56) BC(I,K,L)=BC(I,K,L)+18.0 !FCRS
              if(L.eq.57) BC(I,K,L)=BC(I,K,L)+44.0 !CCRS
             enddo
            enddo
c           endif

c           if(L.ge.49.and.L.le.59) then
c            if(L.eq.49) ratio=0.081115 !PSO4
c            if(L.eq.50) ratio=0.065454 !PNO3
c            if(L.eq.51) ratio=0.042781 !PNH4
c            if(L.eq.52) ratio=0.000955 !SOA5
c            if(L.eq.53) ratio=0.000955 !SOA6
c            if(L.eq.54) ratio=0.036980 !POA
c            if(L.eq.55) ratio=0.015639 !PEC
c            if(L.eq.56) ratio=0.544487 !FCRS
c            if(L.eq.57) ratio=0.198287 !CCRS
c            if(L.eq.58) ratio=0.005294 !NA
c            if(L.eq.59) ratio=0.008055 !PCL
c            do I=1,NC
c             do K=1,NOZ
c              if(L.eq.57) BC(I,K,L)=BC(I,K,L)+ratio*200.0
c              if(L.eq.56) BC(I,K,L)=BC(I,K,L)+ratio*27.0
c              if(L.ne.56.and.L.ne.57) BC(I,K,L)=BC(I,K,L)+ratio*27.0
c             enddo
c            enddo
c           endif

           WRITE(12) NOSEG, (SPNAME(I,L),I=1,10), NDG,
     $        ((BC(I,K,L), K=1,NOZ), I=1,NC)
         enddo !NEDG
       enddo !L
      enddo !next time

20    close(11)
      close(12)

c      do L=1,60
c       write(*,*) L,total(L)
c      enddo

      end
