C     COMDECK.FILCON
C-----------------------------------------------------------------------
C
C     *** /FILCON/ CONTAINS ALL FILE CONTROL VARIABLES
C
      COMMON /FILCON/ NSPMAX, NAM(10), NID(60), MSPNAM(10,35),
     $ NUAQ  , NAMAQ (10), NBDAQ , BTAQ  , NEDAQ , ETAQ  ,
     $   NSAQ  , NSIAQ (35),
     $ NUBDY , NAMBDY(10), NBDBDY, BTBDY , NEDBDY, ETBDY ,
     $   NFRBDY,
     $   NSBDY , NSIBDY(35),
     $ NUCHP , NAMCHP(10),
     $ NUDB  , NAMDB (10), NBDDB , BTDB  , NEDDB , ETDB  ,
     $   NFRDB , TBDB  , TDDB  ,
     $ NUEM  , NAMEM (10), NBDEM , BTEM  , NEDEM , ETEM  ,
     $   NFREM ,
     $   NSEM  , NSIEM (35)
C
      COMMON /FILCON/
     $ NUMET , NAMMET(10), NBDMET, BTMET , NEDMET, ETMET ,
     $   NFRMET,
     $ NUPTS , NAMPTS(10), NBDPTS, BTPTS , NEDPTS, ETPTS ,
     $   NFRPTS,
     $   NSPTS , NSIPTS(35),
     $ NUTOP , NAMTOP(10), NBDTOP, BTTOP , NEDTOP, ETTOP ,
     $   NFRTOP, TBTOP , TDTOP ,
     $ NURWY , NAMRWY(10), NBDRWY, BTRWY , NEDRWY, ETRWY ,
     $   NFRRWY,
     $   NSRWY , NSIRWY(35),
     $ NUAV  , NAMAV (10), NUDEP
C
      COMMON /FILCON/
     $ NUCTL , NAMCTL(10),
     $ NUCON , NAMCON(10),
     $ NUTMP , NAMTMP(10), NBDTMP, BTTMP , NEDTMP, ETTMP ,
     $   NFRTMP,
     $ NUTER , NAMTER(10),
     $ NUCT  , NAMCT (10), NBDCT , BTCT  , NEDCT , ETCT  ,
     $   NFRCT ,
     $   NSCT  , NSICT (35),
     $ NUWND , NAMWND(10), NBDWND, BTWND , NEDWND, ETWND ,
     $   NFRWND,
     $ NUVAR , NAMVAR(10)
C
