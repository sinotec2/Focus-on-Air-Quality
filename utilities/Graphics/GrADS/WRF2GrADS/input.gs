'reinit'
'open input.ctl'

** need input data on height levels

'set mpdset hires'
'set display color white'
'run rgbset.gs'

say 'Create gif images as well (1=yes ; 0=no)'
pull ans
frame = 1

'q file'
rec=sublin(result,5)
_endtime=subwrd(rec,12)

runscript = 1
dis_t = 1

while(runscript)
'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)
say 'Time is ' _analysis

** Do 2D fields first
'c'
'set grads off'
'set gxout contour'
'set ccolor 1'
'set cint 5'
'd (mu+mub)/100.'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.9 8.35  MU'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

'c'
'set grads off'
'set gxout shaded'
'd tsk'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.7 8.35  Surface Theta (K,color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
'run cbar.gs'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

'c'
'set grads off'
'set gxout contour'
'set ccolor 1'
'set cint 50'
'd hgt'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.2 8.35  TERRAIN (m)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

'c'
'set grads off'
'set gxout grfill'
'set clevs       1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17'
'set ccols   0  56 57 58 59 49 47 45 39 37 36 34 22 23 24 29 25 27 27'
'd lu_index'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.7 8.35  LANDUSE (category)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
'run cbar.gs'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

'c'
'set grads off'
'set gxout grfill'
'set clevs       1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17'
'set ccols   0  56 57 58 59 49 47 45 39 37 36 34 22 23 24 29 25 27 27'
'd isltyp'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.7 8.35  SOIL (category)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
'run cbar.gs'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

'c'
'set grads off'
'set gxout grfill'
'set clevs       0 10 20 30 40 50 60 70 80 90 '
'set ccols   0  59 49 45 39 22 29 27 62 62 '
'd vegfra'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.7 8.35  Vegatation Fraction '
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
'run cbar.gs'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

** Plot soil temperature
runlevel = 1
dis_z = 1
while(runlevel)
'set z ' dis_z

'c'
'set grads off'
'set gxout contour'
'set ccolor 1'
'set cint 1'
'd tslb'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.2 8.35  Soil Temperature at soil level ' dis_z
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 1.5 8.0 WRF MASS INPUT'
if(ans)
'printim input'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_z=5 )
 runlevel=0
endif
dis_z = dis_z + 1
endwhile

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

