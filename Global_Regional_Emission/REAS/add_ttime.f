Ckuang@114-32-164-198 /Users/TEDS
C$ cat ./REAS3.1/join_spec/add_ttime.f
       INCLUDE  '/Users/kuang/bin/PARAMS.CMD'
       INCLUDE  '/Users/kuang/bin/CHPARM.CMD'
       INCLUDE  '/Users/kuang/bin/CNTROL.CMD'
       INCLUDE  '/Users/kuang/bin/FILCON.CMD'
       INCLUDE  '/Users/kuang/bin/SEGTAB.CMD'
       INCLUDE  '/Users/kuang/bin/NETDEP.CMD'
       INCLUDE  '/Users/kuang/bin/BALANC.CMD'
       INCLUDE  '/Users/kuang/bin/LOCPTR.CMD'
       INCLUDE  '/Users/kuang/bin/MSCAL.CMD'
       character*4 NAMAV,MSPEC,MRUNID
      integer,parameter::fmax=300
      integer Itmp(4)
      CHARACTER*100 NAM0(fmax) ! input/output file names
      PARAMETER (NI=600,NJ=600)
      dimension MO3(10)
      character*4,allocatable:: SPNAME(:,:)
      integer,allocatable::ndate2(:),ndlast2(:),simtim(:)
      real,allocatable::ttime2(:),ttlast2(:)
      real,allocatable::A1(:,:)

      NUAV=41
      narg=iARGc ()
      if(narg.ne.2) stop 'input the filename, mon'
      do i=1,2
        call getarg(i,nam0(i))
      enddo
        open(11,file=trim(nam0(1)),
     +      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
      read(nam0(2),*)mon
        open(12,file=trim(nam0(1))//'_'//trim(nam0(2)),
     +      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
      nfile=1
      allocate(ndate2(nfile))
      allocate(ndlast2(nfile))
      allocate(ttime2(nfile))
      allocate(ttlast2(nfile))
      allocate(simtim(2*nfile))
      ird=1
        READ (IRD+10) NAMAV, MRUNID, NOSEG, NOSPEC,
     +    NDATE2(ird), TTIME2(ird),
     $    NDLAST2(ird), TTLAST2(ird)
         print*,NDATE2(ird), TTIME2(ird), NDLAST2(ird), TTLAST2(ird)
        allocate(SPNAME(10,NOSPEC))
        READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
        NOSEG=1
        READ (IRD+10) ((Itmp(j), J=1,4), I=1, NOSEG)
        READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
        NXY=NOXG*NOYG
        allocate(A1(NOSPEC,NXY))
      ird=2
       nam0(3)='EMISSIONS '
       print*,NAMAV
        do i=1,10
          NAMAV(i)=nam0(3)(i:i)//'   '
        enddo
       print*,NAMAV

        WRITE(IRD+10) NAMAV, MRUNID, NOSEG, NOSPEC,
     +    NDATE2(1), 0.,
     $    NDATE2(1)+1, 1.
        WRITE(IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
        WRITE(IRD+10) ((Itmp(j), J=1,4), I=1, NOSEG)
        WRITE(IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
      do IM=1,12
        READ (11,end=33) NDATE1, TAVE1, NDATE, TAVE
        print*,NDATE1, TAVE1, NDATE, TAVE
          DO  L=1,NOSPEC
            DO  K=1,NOZ
              READ(11)ISEG,(MRUNID(I),I=1,10),(A1(L,I),I=1,NXY)
            enddo
          enddo
        if (IM.eq.mon) then
          do ih=0,24
           h=real(ih)
           write(12)NDATE2(1)+int(ih/24), amod(h,24.), NDATE2(1)+int((ih+1)/24), amod(h+1,24.)
           DO  L=1,NOSPEC
             DO  K=1,NOZ
              write(12)iseg,(SPNAME(i,l),i=1,10),(A1(L,i),i=1,NXY)
             enddo
           enddo
         enddo
        endif
      enddo
33    stop
      end
