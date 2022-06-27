cPick up selected days of avrg. file
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
character*4,allocatable:: SPNAME(:,:)
character*10,allocatable:: SPN(:)
integer itmp(4)
CHARACTER*60 NAM0(fmax) ! input/output file names
character*4 fname(10)
character*4 note(60)
character*10 airq,spec

PARAMETER (NI=200,NJ=200)
real,allocatable::A1(:,:,:)

NUAV=41
narg=iARGc ()
if(narg.lt.1) stop 'pick_avrg File1 JULHR1 JULHR2 OutSpec' 
do i=1,narg
 call getarg(i,nam0(i))
enddo
if(narg.gt.1) then
read(nam0(2),*)JUL1
read(nam0(3),*)JUL2
else
 JUL1=1
 JUL2=1
endif
if(narg.gt.3) then
 read(nam0(4),*)LpickB
 if(narg.eq.5) then
   read(nam0(5),*)LpickE
   spec=trim(nam0(4))//'-'//trim(nam0(5))
 else
   LpickE=LpickB
   spec=trim(nam0(4))
 endif
endif

narg=2
if(JUL1.eq.1.and.JUL2.eq.1)narg=1       
nam0(2)=trim(nam0(1))//'_'//trim(nam0(2))//'-'//trim(nam0(3))//'_'//trim(spec)
do i=1,narg
   open(i+10,file=trim(nam0(i)),
+      form='unformatted',convert='BIG_ENDIAN',STATUS='unknown')
 print*,trim(nam0(i))
enddo
nfile=1
iout=narg+10

DO IRD=1,nfile
 READ (IRD+10) fname, note, NOSEG, NOSPEC,
+    NDATE2, TTIME2,
$    NDLAST2, TTLAST2
enddo
if(LpickB.eq.0) LpickB=1
if(LpickE.eq.0) LpickE=1
allocate(SPNAME(10,NOSPEC))
allocate(SPN(NOSPEC))
ndate=(ndate2)
ndlast=(ndlast2)
ttime=(ttime2)
ttlast=(ttlast2)
nd1=ndate*100+ttime
nd2=ndlast*100+ttlast
if(JUL1.ge.nd1.and.JUL2.le.nd2) goto 15
ic_beg=ndate
ic_end=ndlast
call caldate(ic_beg)
call caldate(ic_end)
print*,'BEG & END jules:',ndate,ndlast
print*,'BEG & END dates:',ic_beg,ic_end
print*,'BEG & END times:',int(ttime),int(ttlast)
 print*,(fname(i)(1:1),i=1,10),(note(i)(1:1),i=1,60)
15      continue !OK input JUL1 and JUL2
do ird=1,nfile
C
C--REGION DESCRIPTION HEADER
 READ (IRD+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
$    NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
 if(ird.eq.1)then
 print*, XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY
   write(*,*) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
$      NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
 endif
 READ (IRD+10) ((Itmp(j), J=1,4), I=1, NOSEG)
 READ (IRD+10) ((SPNAME(I,J), I=1,10), J=1,NOSPEC)
ENDDO ! next IRD input file
if(.not.(JUL1.ge.nd1.and.JUL2.le.nd2))then
 do J=1,NOSPEC
   do I=1,10
     SPN(J)(i:i)=SPNAME(I,J)(1:1)
   enddo 
 enddo 
 write(*,'(999(I4,A))')(J,trim(SPN(J)),J=1,NOSPEC)
stop
endif
 NXY=NOXG*NOYG
allocate(A1(NXY,NOZ,NOSPEC))
 NNSPEC=LpickE-LpickB+1
write(narg+10) fname, note, NOSEG, NNSPEC,JUL1/100,real(mod(JUL1,100)),
$  JUL2/100, real(mod(JUL2,100))
write(narg+10) XUTM, YUTM, NZONE, XORG, YORG, DELTAX, DELTAY,
$  NOXG, NOYG, NOZ, NVLOW, NVUP, DZSURF, DZMINL, DZMINU
write(narg+10)1,1,NOXG,NOYG
write(narg+10)((SPNAME(I,J), I=1,10), J=LpickB,LpickE)

do ird=1,nfile
 do while(.true.)
   READ (10+ird,end=33) NDATE1, TAVE1, NDATE, TAVE
   write(*,*)'read',NDATE1, TAVE1,NDATE,TAVE
   DO  L=1,NOSPEC
     DO  K=1,NOZ
       READ(10+ird)ISEG,(SPNAME(I,L),I=1,10),(A1(I,K,L),I=1,NXY)
     enddo
   enddo
   nd1=NDATE1*100+TAVE1
if(JUL1.gt.nd1)cycle 
if(JUL2.lt.nd1)exit 
NC1=NDATE1
call caldate(NC1)
   write(*,*)ird,NDATE1, TAVE1,NC1
   write(narg+10)NDATE1, TAVE1, NDATE, TAVE
   DO  L=LpickB,LpickE
     DO K=1,NOZ
       write(narg+10)1,(SPNAME(i,l),i=1,10),(A1(I,K,L),I=1,NXY)
     enddo
   enddo
 enddo
33      continue
enddo
end
subroutine caldate(idate)
dimension nday(12)
data nday/31,28,31,30,31,30,31,31,30,31,30,31/
if (idate.gt.100000) goto 9999
iyear = idate/1000
jday = idate - iyear*1000
nday(2) = 28
if (mod(iyear,4).eq.0) nday(2) = 29
mday = 0
do 10 imonth = 1,12
 mday = mday + nday(imonth)
 if (mday.ge.jday) go to 20
10   continue
20   iday = jday - (mday - nday(imonth))
idate = iyear*10000 + imonth*100 + iday
9999 return
end
