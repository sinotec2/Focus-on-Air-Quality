'reinit'
'open real_p.ctl'

** Need input data on p levels

'set mpdset hires'
'set display color white'
'run rgbset.gs'

say 'Create gif images as well (1=yes ; 0=no)'
pull ans
frame = 1

'q file'
rec=sublin(result,5)
_endtime=subwrd(rec,12)
_endlev=subwrd(rec,9)

runscript = 1
dis_t = 1

while(runscript)
dis_z = 1
'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)
say 'Time is ' _analysis

runlevel = 1
while(runlevel)
'set z ' dis_z
'q dims'
rec=sublin(result,4)
newz=subwrd(rec,6)
say 'Level is ' newz

** Looking for 850 mb  data
if (newz=850)
say 'Plotting'
'c'
'set grads off'
'set gxout shaded'
'set clevs 10 20 30 40 50 60 70 80 90 100'        
'set ccols 0 0 0  0 33 34 35 36 37 38  39'
'd rh'
'set gxout contour'
'set ccolor 4'
'set cthick 6'
'set cint 20'
'd z'
'set ccolor 2'
'set cthick 6'
'set cint 5'
'd tc'
'set strsiz .2'
'set string 1 l 6'
'draw string 1.7 8.35 ' newz ' mb Height (m,blue), T(C,red), RH(color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'run cbar.gs'
if(ans)
'printim realp'frame'.gif gif '
frame=frame+1
endif
pull dummy
endif

** Looking for 700 mb  data
if (newz=700)
say 'Plotting'
'c'
'set ccolor 4'
'set cthick 6'
'set cint 20'
'd z'
'set ccolor 2'
'set cthick 6'
'set cint 5'
'd tc'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35 ' newz ' mb Height (m,blue), T(C,red)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
if(ans)
'printim realp'frame'.gif gif '
frame=frame+1
endif
pull dummy
endif

** Looking for 500 mb  data
if (newz=500)
'c'
'set z 11'
'set ccolor 4'
'set cthick 6'
'set cint 40'
'd z'
'set ccolor 2'
'set cthick 6'
'set cint 5'
'd tc'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35 ' newz ' mb Height (m,blue), T(C,red)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
if(ans)
'printim realp'frame'.gif gif '
frame=frame+1
endif
pull dummy
endif

** Looking for 300 mb  data
if (newz=300)
'c'
'set z 15'
'define wspd=(sqrt(u*u + v*v))'
'set ccolor 4'
'set cthick 6'
'set cint 40'
'd z'
'set ccolor 3'
'set cthick 6'
'set cint 10'
'd wspd'
'set strsiz .2'
'set string 1 l 6'
'draw string 1.7 8.35 ' newz ' mb Height (m,blue), Wind Speed(m/sec,green)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
if(ans)
'printim realp'frame'.gif gif '
frame=frame+1
endif
pull dummy
endif

if ( dis_z=_endlev )
 runlevel=0
endif
dis_z = dis_z + 1
endwhile

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

