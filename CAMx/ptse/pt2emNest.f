!kuang@master ~/bin
!$ cat pt2emNest.f
      program pt2em !transform fort14 to fort13 for VERDI
      CHARACTER*4 MEM(10), MSPEC(10,50), MPTS(10)
      INTEGER MFID(60)
      PARAMETER (MP=80000)
      character*50 fort13, fort14
      DIMENSION X(MP),Y(MP),IX(MP),IY(MP),D(MP),H(MP)
      DIMENSION T(MP),V(MP)
      DIMENSION ILOC(MP,24), IJPS(MP,24), KPTS(MP,24)
      DIMENSION FLOW(MP,24),EFPLH(MP,24)
      DIMENSION IPOPT(6),QPTS(50,MP)
      DIMENSION QP(50,MP) ! EMISSION IN g-mole/HR
      parameter(MROWS=200,MCOLS=200)
      dimension tmp(MCOLS,MCOLS)
      narg=iARGc ()
      if(narg.ne.2) stop 'pt2emNest File14 Nest.in'
      call getarg(1,fort14)
      call getarg(2,fort13)
      DATA NUPTS /14/
      OPEN(NUPTS, FILE=trim(fort14),FORM='UNFORMATTED'
     ,  ,convert='BIG_ENDIAN',STATUS='UNKNOWN')
      read  (NUPTS)    MPTS, MFID, NSG, NSPEC, NBD, TBEG, NED, TEND
      read  (NUPTS) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
     $         NX, NY, NZ
     $, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
      read  (NUPTS) I1,I1,NX,NY
      read  (NUPTS) ((MSPEC(I,J),I=1,10),J=1,NSPEC)
      read  (NUPTS) NSEG, NOPTS
      read  (NUPTS) (X(K),Y(K),H(K),D(K),T(K),V(K),K=1,NOPTS)
!     do K=1,NOPTS
!       if(D(K).le.0)print*,K,X(K),Y(K),D(K)
!     enddo
!     s3top
      open(1,file=trim(fort13),status='unknown')
      call readIn(NX,NY,NZ,XORG,YORG,DELTAX,DELTAY)
      XORG=XORG*1000.
      YORG=YORG*1000.
      DELTAX=DELTAX*1000.
      DELTAY=DELTAY*1000.
      XLEN=XORG+NX*DELTAX
      YLEN=YORG+NY*DELTAY
      close(1)
      NZ=1
        fort13=trim(fort14)//'.'//trim(fort13)
      data NUEM1/13/
      OPEN(NUEM1, FILE=trim(fort13),FORM='UNFORMATTED'
     +  ,convert='BIG_ENDIAN',STATUS='UNKNOWN')
      DATA MEM  / 1HE, 1HM, 1HI, 1HS, 1HS, 1HI, 1HO, 1HN, 1HS, 1H /
      data plon,plat/120.99, 23.61/iutm,iproj,itzon/51,2,-8/
      data t1,t2/10.,40./
      write(NUEM1) MEM, MFID, itzon, NSPEC, NBD, TBEG, NED, TEND
      write(NUEM1) plon,plat,iutm,XORG,YORG,DELTAX,DELTAY,
     +             NX,NY,NZ, iproj,NVUP,t1,t2,DZMINU
      write(NUEM1)idum1,idum1,NX,NY
      write(NUEM1)((MSPEC(I,J),I=1,10),J=1,NSPEC)

        WRITE ( *,* ) NBD, TB  , JED, TE, NOPTS,NSPEC,NX,NY,NZ
      DO
        read  (NUPTS,end=680) NBD, TB  , JED, TE
        write (NUEM1) NBD, TB, JED, TE
        read  (NUPTS) NSEG, NOPTS
        WRITE ( *,* ) NBD, TB  , JED, TE
        IT=int(TB)+1
        read  (NUPTS)(ILOC(IP,IT),IJPS(IP,IT),KPTS(IP,IT),FLOW(IP,IT),
     $    EFPLH(IP,IT), IP=1,NOPTS)
        DO 500 L=1,NSPEC
          read  (NUPTS) NSEG,(MSPEC(J,L),J=1,10),
     $      (QPTS(L,IP), IP=1,NOPTS)
        tmp=0
        do IP=1,NOPTS
          if((X(IP)-XORG)*(X(IP)-XLEN).GT.0) cycle
          if((Y(IP)-YORG)*(Y(IP)-YLEN).GT.0) cycle
          I=(X(IP)-XORG)/DELTAX+1
          J=(Y(IP)-YORG)/DELTAY+1
        if(I.le.0.or.I.gt.MROWS) print*,I
        if(J.le.0.or.J.gt.MCOLS) print*,J
          tmp(I,J)=tmp(I,J)+QPTS(L,IP)
        enddo !IP
      write(NUEM1)NSG,(MSPEC(J,L),J=1,10),((tmp(I,J),I=1,NX),J=1,NY)
500     CONTINUE
      ENDDO
680   CONTINUE !next hour
      STOP
      end
      subroutine readIn(NX,NY,NZ,XORG,YORG,DELTAX,DELTAY)
      character fname*100,project*10
      do i=1,7
      read(1,*)
      enddo
      read(1,'(20x,a)') fname !line 8th
      read(fname,*) NX,NY,NZ
      write(*,'(a,3i10)')'                 CAMx grid size:',NX,NY,NZ
      read(1,'(20x,a)') fname
      read(fname,*)DELTAX,DELTAY
       write(*,'(a,2f10.3)')
     &                  '              CAMx grid spacing:',DELTAX,DELTAY
        read(1,'(20x,a)') fname
        read(fname,*) XORG,YORG,clonin,clatin,tlat1in,tlat2in
        write(*,'(a,2f10.3)')
     &                  '    CAMx LCP Origin (SW corner):',XORG,YORG
        write(*,'(a,4f10.3,/)')
     &  '    CAMx LCP Projection Params :',clonin,clatin,tlat1in,tlat2in
        return
        end
