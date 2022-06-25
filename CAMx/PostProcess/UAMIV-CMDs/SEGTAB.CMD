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
