C     COMDECK.MSCAL
C------------------------------------------------------------------------
C
C     *** /MSCAL/ CONTAINS METEOROLOGICAL SCALARS
C        THEY ARE READ OR CALCULATED IN MSREAD
C
      COMMON /MSCAL/ TGRADB, TGRADA, CE    , FRKEND, H2O   , ATMPRS,
     $               KKAER , AEFACT,
     $               ATFACT, QFACT , TMBEG , TMEND , FRKBEG, FRKDEL,
     $               LDARK ,
     $               FACTRK, METNAM(10,6)
C
      LOGICAL LDARK
      DIMENSION SCAL(6)
      EQUIVALENCE (SCAL, TGRADB)
C
