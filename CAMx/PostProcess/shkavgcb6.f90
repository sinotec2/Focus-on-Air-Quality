!##v4.0-2013/10/6
!  **▒t▒XCB6▒AVOC▒▒▒ؼW▒[
!##v4.1-2013/12/14
!  **▒W▒[▒▒X▒▒▒▒PM2ND
!##v4.3-2014/11/20(pei)
!  **▒H4.1▒▒▒ק▒,▒]VERDI▒L▒k▒}▒▒PM2.5,▒אּPM25

   program shkavg
    integer,parameter::nlst=32,nvlst=62  !camx out▒Dvoc▒▒voc▒▒▒ؼ▒
    integer,parameter::nout=9  !shrink▒▒output▒▒▒ؼ▒
    real,allocatable::rval(:,:,:,:)    !rval(nx,ny,nz)
    real,allocatable::oconc(:,:,:,:) !oconc(nx,ny,nz,nspec)
    integer,allocatable::iv(:),iin(:),SEQ(:),SEQV(:) !
    real ridx(nout,nlst)
    real rvidx(nvlst)  !for voc
    character finp*60,fout*60
    character*4 name(10),note(60)
    character(len=4),allocatable::namvar(:,:),namspec(:,:)
    character*10 lstname(nlst)   !for non-voc
    character*10 lsvname(nvlst)  !for voc
    character aa10*10,A10(nout)*10
    character(len=4) outname(10,nout)
    logical,allocatable::lfind(:)
    real,allocatable::bt(:)
    integer,allocatable::ibd(:)
 !===▒DVOC
 !                O3  NO2  SO2  VOC PM25 PM10 PNO3,PSO4
    data A10/'O3','NO2','SO2','VOC','PM25','PM10','PNO3','PSO4','CO'/
    data ridx /   0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !NO
                  0.,  1.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !NO2
                  1.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !O3
                  0.,  0.,  1.,  0.,  0.,  0.,  0.,   0.,   0., &  !SO2
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !NH3
                  0.,  0.,  0.,  0.,0.58,  1.,  1.,   0.,   0., &  !PNO3Tsai & Cheng
                  0.,  0.,  0.,  0.,0.85,  1.,  0.,   1.,   0., &  !PSO4
                  0.,  0.,  0.,  0.,.774,  1.,  0.,   0.,   0., &  !PNH4
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !POA
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !PEC
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !FPRM
                  0.,  0.,  0.,  0.,  0.,  1.,  0.,   0.,   0., &  !CPRM
                  0.,  0.,  0.,  0.,  0.,  1.,  0.,   0.,   0., &  !CCRS
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !FCRS
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA1
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA2
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA3
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA4
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA5
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOA6
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !H2O2
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !NO3
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !N2O5
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !HNO3
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   1., &  !CO
                  0.,  0.,  0.,  0.,.312,  1.,  0.,   0.,   0., &  !NA
                  0.,  0.,  0.,  0.,.312,  1.,  0.,   0.,   0., &  !PCL
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !PNA
                  0.,  0.,  0.,  0.,  0.,  0.,  0.,   0.,   0., &  !PH2O
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOPA
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0., &  !SOPB
                  0.,  0.,  0.,  0.,  1.,  1.,  0.,   0.,   0./    !SOA7
 
 !#
 !#
    data lsvname/'HCO3', 'HO2', 'MEO2', 'ROR', 'CO', 'CH4', 'FACD', 'FORM', 'KET', 'MEOH', &
                 'MEPX', 'PAR', 'ECH4', 'XPAR', 'C2O3', 'AACD', 'ALD2', 'ALDX', 'ETH', 'ETHA',&
                 'ETHY', 'ETOH', 'GLY', 'GLYD', 'PACD', 'PAN', 'CXO3', 'ACET', 'MGLY', 'OLE', &
                 'PANX', 'PRPA', 'XPRP', 'OPO3', 'IOLE','ISPD', 'NTR', 'OPAN', 'OPEN', 'EPX2',&
                 'ISO2', 'EPOX', 'HPLD', 'INTR', 'ISOP', 'ISPX', 'XOPN','BZO2', 'BENZ','CRO',&
                 'TO2', 'CAT1', 'CRES', 'CRON', 'TOL', 'CRNO', 'CRN2', 'CRPX', 'CAO2','XLO2',&
                  'XYL','TERP'/
    data rvidx / 1, 1, 1, 1, 0, 0, 1, 1, 1, 1,&
                 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,&
                 2, 2, 2, 2, 2, 2, 3, 3, 3, 3,&
                 3, 3, 3, 4, 4, 4, 4, 4, 4, 5,&
                 5, 5, 5, 5, 5, 5, 5, 6, 6, 7,&
                 7, 7, 7, 7, 7, 7, 7, 7, 7, 8,&
                 8, 10/
 
 !##▒𪬪▒▒▒ ppm -> ppb ##
    ridx(1:3,:)=ridx(1:3,:)*1000.
    rvidx=rvidx*1000.
 
 !##species name list--non-voc
    lstname(1)   = 'NO'
    lstname(2)   = 'NO2'
    lstname(3)   = 'O3'
    lstname(4)   = 'SO2'
    lstname(5)   = 'NH3'
    lstname(6)   = 'PNO3'
    lstname(7)   = 'PSO4'
    lstname(8)   = 'PNH4'
    lstname(9)   = 'POA'
    lstname(10)  = 'PEC'
    lstname(11)  = 'FPRM'
    lstname(12)  = 'CPRM'
    lstname(13)  = 'CCRS'
    lstname(14)  = 'FCRS'
    lstname(15)  = 'SOA1'
    lstname(16)  = 'SOA2'
    lstname(17)  = 'SOA3'
    lstname(18)  = 'SOA4'
    lstname(19)  = 'SOA5'
    lstname(20)  = 'SOA6'
    lstname(21)  = 'H2O2'
    lstname(22)  = 'NO3'
    lstname(23)  = 'N2O5'
    lstname(24)  = 'HNO3'
    lstname(25)  = 'CO'
    lstname(26)  = 'NA'
    lstname(27)  = 'PCL' !Particulate Chloride
    lstname(28)  = 'PNA' !Peroxynitric acid (HNO4)
    lstname(29)  = 'PH2O'
    lstname(30)  = 'SOPA'
    lstname(31)  = 'SOPB'
    lstname(32)  = 'SOA7'
 
 !##species name list--voc
 
 !##species name for output
    outname='    '
    do j=1,nout
    do i=1,len_trim(A10(j))
      outname(i,j)(1:1)=A10(j)(i:i)
    enddo
    enddo
 !##
 
    narg=iARGc ()
    if(narg.NE.1) then
      WRITE(*,*) 'shkavg syntax error, should be: "shkavg input_file".'
      stop
    ENDIF
 
    call getarg(1,finp)
 
    ilen=0
    do i=2,50
      if(finp(i:i+8)=='.avrg.grd')then
        ilen=i-1
        fout=finp(1:ilen)//'.S.'//finp(ilen+7:ilen+11)
        exit
      endif
    enddo
 
    if(ilen==0)then
      write(*,*)'shkavrg syntax error'
      write(*,*)'▒▒▒ɦW▒▒▒.avrg.grdnn'
      stop
    endif
 
    open(11,file=trim(finp),form='unformatted',convert='BIG_ENDIAN')
    open(12,file=trim(fout),form='unformatted',convert='BIG_ENDIAN')
 
 !##Ū▒▒▒▒▒Y
    read(11)name,note,itzon,nvar,ibdate,btime,iedate,etime
    read(11)plon,plat,iutm,xorg,yorg,delx,dely,nx,ny,nz,iproj,istag,tlat1,tlat2,rdum
    read(11)ione,ione,nx,ny
    nt=(iedate-ibdate)*24+(etime-btime)
    allocate(namvar(10,nvar))
    allocate(namspec(10,nvar))
    read(11)((namspec(i,l),i=1,10),l=1,nvar)
    nt=0
    do
      read(11,end=99)
      do i=1,nvar*nz
        read(11)
      enddo
      nt=nt+1
    enddo
 99 rewind(11)
    do i=1,4
      read(11)
    enddo
    nspec=nvar
    nxy=nx*ny
    allocate(rval(nxy,nz,nspec,nt))
    allocate(oconc(nxy,nz,nout,nt))
    allocate(SEQ(nspec),SEQV(nspec),iv(nspec),iin(nspec),lfind(nspec))
    allocate(ibd(nt+1),bt(nt+1))
    nspec_nvoc=0
    nspec_voc=0
    do l=1,nspec
        do i=1,10
 !         j=1+(i-1)*4
          aa10(i:i)=namspec(i,l)(1:1)
        enddo
 
        lfind(l)=.false.
        iv(l)=-1
        iin(l)=0
        do i=1,nlst  !▒q▒Dvoc▒▒▒▒
          if(aa10.eq.lstname(i))then
            iv(l)=0  !▒▒Dvoc
            lfind(l)=.true.
            iin(l)=i
            nspec_nvoc=nspec_nvoc+1
            SEQ(nspec_nvoc)=l
            exit
          endif
        enddo
 
        if(.not.lfind(l))then  !▒qvoc▒▒▒▒
          do i=1,nvlst  !▒q▒Dvoc▒▒▒▒
            if(aa10==lsvname(i))then
              lfind(l)=.true.
              iv(l)=1  !▒▒Ovoc
              iin(l)=i
              nspec_voc=nspec_voc+1
              SEQV(nspec_voc)=l
              exit
            endif
          enddo
        endif
    enddo
 !##Time loop
    rval=0.
    oconc=0.
    do it=1,nt
      read(11,end=20,err=20)ibd(it),bt(it),ibd(it+1),bt(it+1)
      do l=1,nspec
        do k=1,nz
          read(11,end=20,err=20)ione,(namspec(ii,l),ii=1,10),(rval(i,k,l,it),i=1,nxy)
        enddo
      enddo
    enddo  !Time loop
 20 continue
    nt_actual=nt
    if(it.le.nt)then !if final, it must be nt+1
         nt_actual=it-2
         iedate=ibd(nt_actual)
         etime=bt(nt_actual)
         endif
 !       print*,'nt_actual',nt_actual,iedate,etime
    write(12)name,note,itzon,nout,ibdate,btime,iedate,etime
    write(12)plon,plat,iutm,xorg,yorg,delx,dely,nx,ny,nz,iproj,istag,tlat1,tlat2,rdum
    write(12)ione,ione,nx,ny
    write(12)((outname(i,l),i=1,10),l=1,nout)
    do it=1,nt_actual
      do ll=1,nout
        do kk=1,nz
          do ii=1,nxy
 !non-voc
           sumc=0
           do lnv=1,nspec_nvoc
             l=SEQ(lnv)
             sumc=sumc+rval(ii,kk,l,it)*ridx(ll,iin(l))
           enddo
           oconc(ii,kk,ll,it)=sumc
 !voc
          sumc=0
          do lnv=1,nspec_voc
            l=SEQV(lnv)
            sumc=sumc+rval(ii,kk,l,it)*rvidx(iin(l))
          enddo
          oconc(ii,kk,4,it)=sumc
        enddo
        enddo
      enddo
    enddo  !Time loop
 !voc
 
 !##▒g▒X
 
    do it=1,nt_actual
      write(12)ibd(it),bt(it),ibd(it+1),bt(it+1)
      do l=1,nout
        do k=1,nz
          write(12)ione,(outname(ii,l),ii=1,10),(oconc(i,k,l,it),i=1,nxy)
        enddo
      enddo
    enddo  !Time loop
    end
 