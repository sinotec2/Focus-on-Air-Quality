C     COMDECK.LOCPTR
C--------------------------------------------------------------------
C
C     *** /LOCPTR/ CONTAINS POINTERS TO LOCAL VARIABLES
C                   USED BY THE INTEGRATION ROUTINES
C
      COMMON /LOCPTR/ NLPTR,
     $  JTH   , JTHNEW, JTHAVG, JHT   , JHTNEW, JHTAVG,
     $  JVD   , JSRC  , JR    ,
     $  JHS1  , JHCS1 , JWS1  , JCS1  , JAS1  , JDELS1,
     $  JAER  , JFACT , JCON  , JCONT , JXKZ  , JFLUX ,
     $  JWZ   , JTHEDG, JWAV  , JDHDT , JDUM  ,
     $  JA    , JB    , JC    , JY    , JX    ,
     $  JCTEST, JZ    , JAOMEG,
     $  JHOLD , JRATE , JYGF  , JGA   , JGF   , JDC
C
      DIMENSION  JLPTR(40)
      EQUIVALENCE (JLPTR,JTH)
C
