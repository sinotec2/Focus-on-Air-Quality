C
C    COMMON /BALANC/
C
C       -- USED FOR KEEPING TRACK OF MASS FLUXES IN AND OUT
C          OF THE MODELED REGION
C
      COMMON /BALANC/ BLFLOW(32,2,4), BUFLOW(32,2,4), TPFLOW(32,2), 
     $                PTFLOW(32), EFLOW(32), DPFLOW(32),
     $                BLFLCU(32,2,4), BUFLCU(32,2,4), TPFLCU(32,2), 
     $                PTFLCU(32), EFLCU(32), DPFLCU(32),
     $                TMAS(32), TMASM(32)
C
