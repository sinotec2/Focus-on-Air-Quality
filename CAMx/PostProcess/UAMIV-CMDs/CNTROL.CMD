C     COMDECK.CNTROL
C------------------------------------------------------------------------
C
C     *** /CNTROL/ CONTAINS MANY CONTROL PARAMETERS OF GLOBAL INTEREST
C
C--DIMENSIONS AND REGION DESCRIPTORS USED A LOT
C
      COMMON /CNTROL/ NOZ   , NOZP1 , NOZM1 , NOSEG , NOSPEC, NORS  ,
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
      COMMON /CNTROL/ MRUNID(60),     XUTM  , YUTM  , NZONE ,
     $                XORG  , YORG  , NOXG  , NOYG  , NOZG  ,
     $                NVLOW , NVUP  , DZMINL, DZMINU, NDTREF
C
C         MRUNID    A  RUN ID
C         XUTM      R  REFERENCE ORIGIN
C         YUTM      R  REFERENCE ORIGIN
