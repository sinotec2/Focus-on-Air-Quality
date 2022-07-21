'reinit'
'open bwave.ctl'
** 
** script needs height level input data
** will look for .25 and 2 km data to plot

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
dis_t = 11

'set xlab off'
'set ylab off'

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

** Looking for 0.25 km data
if (newz=0.25)
say 'Plotting'
'c'
'set grads off'
'set gxout shaded'
'd theta'
'set gxout contour'
'd p'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0 8.35   Pressure (mb,lines), Theta (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 4.0 8.0 ' newz '  km '
'run cbar.gs'
if(ans)
'printim bwave'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'set clevs   -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8  9 10 '
'set ccols 0 54 55 56 58 59 4  49 39 37 35 21 22 23 24 67 68 69 '
'd w*100.'
'set strsiz .2'
'set string 1 l 6'
'draw string 5.0.7 8.35   W (cm/s)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 4.0 8.0 ' newz '  km '
'run cbar.gs'
if(ans)
'printim bwave'frame'.gif gif '
frame=frame+1
endif
pull dummy
endif
** Looking for 2 km data
if (newz=2.0)
say 'Plotting'
'c'
'set grads off'
'set gxout shaded'
'd theta'
'set gxout contour'
'd p'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0 8.35   Pressure (mb,lines), Theta (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 4.0 8.0 ' newz '  km '
'run cbar.gs'
if(ans)
'printim bwave'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'set clevs   -6 -5 -4 -3 -2 -1  0  1  2  3  4  5  6  7  8  9 10 '
'set ccols 0 54 55 56 58 59 4  49 39 37 35 21 22 23 24 67 68 69 '
'd w*100.'
'set strsiz .2'
'set string 1 l 6'
'draw string 5.0 8.35   W (cm/s)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'draw string 4.0 8.0 ' newz '  km '
'run cbar.gs'
if(ans)
'printim bwave'frame'.gif gif '
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

