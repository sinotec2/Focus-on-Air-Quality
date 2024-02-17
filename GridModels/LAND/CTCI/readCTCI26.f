
      parameter(minX=86,maxX=520,minY=2422,maxY=2872)
      integer UTME,UTMN,DICT
      real D2,D3,D5,D5A,D5B,D5C,D7,D7A,D7B,D7C,D7D,D8,D9,D10,D11,D12,D13
      real D14,D18,D103,D106,D108,D99
      REAL Area(26+2,minX:maxX,minY:maxY)     !27 ele; 28 population
      REAL LandUse(minX:maxX,minY:maxY)       !18 ele; 19 population
      real ele(35,55),AA(17),f(27,77,137)
      PARAMETER (XORG2=23.6,YORG2=2291.8,DELTA=9.,NCOL2=46,NROW2=70)
      parameter (m1=NCOL2*NROW2,NX0=41,NY0=56,NX1=77,NY1=77)
      DIMENSION Kusgs24(NCOL2,NROW2)
      character A1*1
      dimension NX(2),NY(2),IDX(2),IX0(2),IY0(2)
      data NX/41,77/NY/56,137/IDX/9,3/
      data IX0/67,133/IY0/2363,2411/

!       D2      . .
!       D3      ...(M*M)
!       D4      ...(M*M)
        open(1,file='land.txt',status='unknown')
        goto 4
!       find the max and min boundaries
        mnutme=9999
        mxutme=-9999
        mnutmn=9999
        mxutmn=-9999
        read(1,*)
1       read(1,*,end=2,err=2)UTME,UTMN,DICT
     +D2,D3,D5,D5A,D5B,D5C,D7,D7A,D7B,D7C,D7D,D8,D9,D10,D11,D12,D13,
     +D14,D18,D103,D106,D108,D99
        mnutme=min0(mnutme,utme)
        mxutme=max0(mxutme,utme)
        mnutmn=min0(mnutmn,utmn)
        mxutmn=max0(mxutmn,utmn)
        goto 1
2       close(1)
        write(*,*)mnutme,mxutme,mnutmn,mxutmn

4       continue
        do j=minX,maxX
        do k=minY,maxY
        do i=1,28
        Area(i,j,k)=0.
        enddo
        Area(1,j,k)=1000000.
        area(27,j,k)=-1
        enddo
        enddo
!       begin to mapping the area
      open ( 1,file='taiwan1km.dat',status='unknown')
11      read(1,*,end=12)i,j,elev
        ii=int(i/1000+0.5)
        jj=int(j/1000+0.5)
        if((ii-minX)*(ii-maxX).le.0.and.(jj-minY)*(jj-maxY).le.0)then
      Area(27,ii,jj)=elev
       !print*,ii,jj,elev
        endif
        goto 11
12    close(1)

        DO I=1,17
        AA(I)=0
        ENDDO
        open(1,file='land.txt',status='unknown')
        read(1,*)
10      read(1,*,end=20,err=13)UTME,UTMN,DICT,D2,AA(1),D5,(AA(I),I=2,4),
     +D7,(AA(I),I=5,8),D8,D9,AA(10),D11,AA(12),AA(13),
     +D14,D18,(AA(I),I=14,17)
C     +D2,D3,D5,D5A,D5B,D5C,D7,D7A,D7B,D7C,D7D,D8,D9,D10,D11,D12,D13,
C     +D14,D18,D103,D106,D108, D99
c                       .. .. ..(....)
13      SUM=0
        DO I=1,17
                SUM=SUM+AA(I)
        ENDDO
        IF(SUM.EQ.0) GOTO 10
        RAT=1000000./SUM
        DO I=1,17
                AA(I)=AA(I)*RAT
        ENDDO
!population
        Area(28,UTME,UTMN)=D2

!habitized area
        Area(21,UTME,UTMN)=AA(1)+AA(14)+AA(15)
!       D3+D103+D106 !........ ,.. ..

!crop lands
        Area(20,UTME,UTMN)=AA(12)       !D12    !IRRI.CROP ..
        Area(14,UTME,UTMN)=AA(2)        !D5A    !..............
        Area(18,UTME,UTMN)=AA(4)        !D5C    !...
        Area(17,UTME,UTMN)=AA(3)        !D5B    !..
        Area(15,UTME,UTMN)=AA(17)       !D99    !(....)
        Area(13,UTME,UTMN)=AA(6)+AA(7)+AA(8)    !D7C+D7D !..+..

!forests 11~15
        Area(7,UTME,UTMN)=AA(6)+AA(7)!.. ..
        Area(10,UTME,UTMN)=+AA(8)       !D7D    !..
      elev=Area(27,UTME,UTMN)
        if(elev.le.1500) then
                Area(6,UTME,UTMN)=AA(5) !D7A    !.................
        elseif(elev.le.2500) then
                Area(5,UTME,UTMN)=AA(5) !D7A
        else
                Area(4,UTME,UTMN)=AA(5) !D7A
        endif
!water bodies
        Area(1,UTME,UTMN)=AA(16)        !D108   !..
!       if(elev.le.0) Area(1,UTME,UTMN)=1000*1000       !sea
        Area(2,UTME,UTMN)=0             !ice 
        Area(3,UTME,UTMN)=AA(10)        !D10    !........
        Area(23,UTME,UTMN)=AA(13)       !D13    !..

        goto 10
20      close(1)
        print*,'OK'
c       population check
        SUM=0
        do j=minX,maxX
        do k=minY,maxY
        sum=sum+Area(28,j,k)
        enddo
        enddo

        rat=23069345/sum
        do j=minX,maxX
        do k=minY,maxY
        LandUse(j,k)=1
        Area(28,j,k)=Area(28,j,k)*rat
        enddo
        enddo

        do j=minX+1,maxX-1
        do k=minY+1,maxY-1
        if(AREA(1,J,K).eq.1000000) then
        SUM=0
        do i=1,26
        sum2=0
        do jj=j-1,j+1
        do kk=k-1,k+1
                SUM=SUM+AREA(I,JJ,KK)
                SUM2=SUM2+AREA(I,JJ,KK)
        ENDDO
        enddo
        AREA(i,J,K)=sum2/9
        enddo
        endif
        enddo
        enddo
        open(1,file='area.lu')
        do j=minX,maxX
        do k=minY,maxY
                sum=0
                sum2=0
                do i=1,26
                        sum=sum+area(i,j,k)
                        if(i.gt.1)sum2=sum2+area(i,j,k)
                enddo
                if(sum2.eq.0.and.area(27,j,k).gt.500) then
                area(1,j,k)=0.
                sum=0
                do i=2,26
                  area(i,j,k)=(area(i,j-1,k)+area(i,j+1,k)
     &                        +area(i,j,k-1)+area(i,j,k+1))/4
                  sum=sum+area(i,j,k)
                enddo
                endif
                if(sum.eq.0) stop 'err'
                do i=1,26
                        area(i,j,k)=area(i,j,k)/sum
                enddo
                write(1,'(2I5,26F6.3)')j,k,(area(i,j,k),i=1,26)
        enddo
        enddo
        close(1)

        open(1,file='lu-ctci.dat')
        do j=minX+1,maxX-1
        do k=minY+1,maxY-1
        amax=-1
        lu=1
        do i=1,26
                if(AREA(i,J,K).ge.amax) then
                        amax=AREA(i,J,K)
                        lu=i
                endif
        enddo
        LandUse(j,k)=lu
        if(lu.ne.1)write(1,*)j*1000+500,k*1000+500,lu
        enddo
        enddo   
        close(1)
        
        do n=1,2
        do i=1,NX(n)
        do j=1,NY(n)
        IX=IX0(n)+(i-1)*IDX(n)
        IY=IY0(n)+(j-1)*IDX(n)
        do k=1,27
        f(k,i,j)=0
        enddo
        do ii=IX,IX+(IDX(n)-1)
        do jj=IY,IY+(IDX(n)-1)
          if((ii-minX)*(ii-maxX).lt.0) then
          if((jj-minY)*(jj-maxY).lt.0) then
            do k=1,27
              f(k,i,j)=f(k,i,j)+area(k,ii,jj)
            enddo
          endif
          endif
        enddo
        enddo
        sum=0
        f(27,i,j)=f(27,i,j)/IDX(n)/IDX(n)
        do k=1,26
        sum=sum+f(k,i,j)
        enddo
        if(sum.eq.0) then
        f(1,i,j)=1
        do k=2,26
          f(k,i,j)=0
        enddo
        else
        do k=1,26
          f(k,i,j)=f(k,i,j)/sum
        enddo
        endif
        enddo   !j
        enddo   !j

        write(A1,'(I1)')n
        open(1,file='landuse26.bin'//A1,convert='big_endian',
     +form='unformatted',status='unknown')
        write(1)'LUCAT26 '
        write(1)(((f(k,i,j),i=1,NX(N)),j=1,NY(N)),k=1,26)
        write(1)'TOPO    '
        write(1)((f(27,i,j),i=1,NX(N)),j=1,NY(N))
        close(1)
        open(1,file='area.lu'//A1)
        do j=1,NX(n)
        do k=1,nY(n)
        write(1,'(2I5,26F6.3)')j,k,(f(i,j,k),i=1,26)
        enddo
        enddo
        close(1)
        if(n.eq.2) then
                open(1,file='habitT.ctci.dat')
        do j=1,NX(n)
        do k=1,nY(n)
        IX=(IX0(n)+(j-1)*IDX(n))*1000.+500
        IY=(IY0(n)+(k-1)*IDX(n))*1000.+500
                if(f(21,j,k).gt.0.1) then
                        write(1,'(2I8,26F6.3)')IX,IY,(f(i,j,k),i=1,26)
                endif
        enddo
        enddo
        close(1)
        endif
        enddo   !n
        
30      continue
        print*,UTME,UTMN,DICT,D2,AA(1),D5,(AA(I),I=2,4),
     +D7,(AA(I),I=5,8),D8,D9,AA(10),D11,AA(12),AA(13),
     +D14,D18,(AA(I),I=14,17)
        end

