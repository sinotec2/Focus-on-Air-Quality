cat /home/kuang/bin/cbin_avrg.ser.f
INCLUDE  'PARAMS.CMD'
INCLUDE  'CHPARM.CMD'
INCLUDE  'CNTROL.CMD'
INCLUDE  'FILCON.CMD'
INCLUDE  'SEGTAB.CMD'
INCLUDE  'NETDEP.CMD'
INCLUDE  'BALANC.CMD'
INCLUDE  'LOCPTR.CMD'
INCLUDE  'MSCAL.CMD'
character*4 NAMAV,MSPEC,MRUNID
integer,parameter::fmax=300
integer Itmp(4)
CHARACTER*100 NAM0(fmax) ! input/output file names
PARAMETER (NI=200,NJ=200)
DIMENSION A1(NI*NJ)
dimension MO3(10)
character*4,allocatable:: SPNAME(:,:)
integer,allocatable::ndate2(:),ndlast2(:),simtim(:)
real,allocatable::ttime2(:),ttlast2(:)

NUAV=41
narg=iARGc ()
c      if(narg.lt.3) stop 'cbin_avrg File1 File2 File3... CombineFile'
if(narg.gt.fmax+1) stop 'File too many'

do i=1,narg
 call getarg(i,nam0(i))
enddo

do i=1,narg
 if(i.eq.narg)then
   open(i+10,file=trim(nam0(i)),
+      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
 else
   open(i+10,file=trim(nam0(i)),
+      form='unformatted',convert='BIG_ENDIAN',STATUS='old')
 endif
 print*,trim(nam0(i))
enddo
nfile=narg-1
iout=narg+10

allocate(ndate2(nfile))
allocate(ndlast2(nfile))
allocate(ttime2(nfile))
allocate(ttlast2(nfile))
allocate(simtim(2*nfile))

DO IRD=1,nfile
 READ (IRD+10) NAMAV, MRUNID, NOSEG, NOSPEC,
+    NDATE2(ird), TTIME2(ird),
$    NDLAST2(ird), TTLAST2(ird)
 simtim(2*ird-1)=NDATE2(ird)*100+TTIME2(ird)
 simtim(2*ird  )=NDLAST2(ird)*100+TTLAST2(ird)
enddo
allocate(SPNAME(10,NOSPEC))
print*,minval(simtim),maxval(simtim)
NDATE=minval(simtim)/100
NDLAST=maxval(simtim)/100
TTIME=mod(minval(simtim),100)
TTLAST=mod(maxval(simtim),100)
write(narg+10) NAMAV, MRUNID, NOSEG, NOSPEC, NDATE, TTIME,
$  NDLAST, TTLAST

do ird=1,nfile
C
C--REGION DESCRIPTION HEADER
 READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
$    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU

 NXY=NOXG*NOYG
 IF(NXY.GT.NI*NJ) STOP ' EXCEED DIMENSION'
C--SEGMENT DESCRIPTION HEADER
 NOSEG=1
 READ (IRD+10) ((Itmp(j), J=1,4), I=1, NOSEG)
C--SPECIES DESCRIPTION HEADER
 READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
ENDDO ! next IRD input file
C
C         FIRST, WRITE TIME INTERVAL
C


write(narg+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
$  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
write(narg+10)((Itmp(j) , J=1,4), I=1, NOSEG)
write(narg+10)((SPNAME(I,J), I=1,10), J=1,NOSPEC)
do ird=1,nfile
 do while(.true.)
   READ (10+ird,end=33) NDATE1, TAVE1, NDATE, TAVE
   NDATE=NDATE1
   TAVE=TAVE1+1
   if(TAVE.eq.24) then
   NDATE=NDATE1+1
   TAVE=0
   endif
   write(narg+10)NDATE1, TAVE1, NDATE, TAVE
   write(*,*)ird,NDATE1, TAVE1, NDATE, TAVE  !!
   DO  L=1,NOSPEC
     DO  K=1,NOZ
       READ(10+ird)ISEG,(MRUNID(I),I=1,10),(A1(I),I=1,NXY)
       write(narg+10)iseg,(SPNAME(i,l),i=1,10),(A1(i),i=1,NXY)
     enddo
   enddo
 enddo
33      continue
enddo
end
