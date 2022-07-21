'reinit'
'open qss.ctl'

** script needs height level input data
** will look for .75 , 1.5. 4 and 8 km data to plot

'set display color white'
'set xlab off'
'set ylab off'
'run rgbset.gs'


say 'Create gif images as well (1=yes ; 0=no)'
pull ans
frame = 1

'q file'
rec=sublin(result,5)
_endtime=subwrd(rec,12)
_endlev=subwrd(rec,9)

runscript = 1
dis_t = 2

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

found_level = 0
** Looking for right level to plot
if (newz=0.75)
 found_level=1
endif
if (newz=1.5)
 found_level=1
endif
if (newz=4.0)
 found_level=1
endif
if (newz=8.0)
 found_level=1
endif
if (found_level)
say 'Plotting'
'c'
'set grads off'
'set gxout shaded'
'd theta'
'set gxout contour'
'd p'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35   pressure (mb,lines), Theta (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 6.5 8.0 ' _analysis
'draw string 2.5 8.0 ' newz ' km'
'run cbar.gs'
if(ans)
'printim qss'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd w'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.7 8.35   W (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 6.5 8.0 ' _analysis
'draw string 2.5 8.0 ' newz ' km'
'run cbar.gs'
if(ans)
'printim qss'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd qvapor*1000.0'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.2 8.35   QVAPOR (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 6.5 8.0 ' _analysis
'draw string 2.5 8.0 ' newz ' km'
'run cbar.gs'
if(ans)
'printim qss'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd qcloud*1000.0'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.2.7 8.35   QCLOUD (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 6.5 8.0 ' _analysis
'draw string 2.5 8.0 ' newz ' km'
'run cbar.gs'
if(ans)
'printim qss'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd qrain*1000.0'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.2.7 8.35   QRAIN (color)'
'set strsiz .15'
'set string 1 l 3'
'draw string 6.5 8.0 ' _analysis
'draw string 2.5 8.0 ' newz ' km'
'run cbar.gs'
pull dummy
if(ans)
'printim qss'frame'.gif gif '
frame=frame+1
endif
endif

if ( dis_z=_endlev )
 runlevel=0
endif
dis_z = dis_z + 1
endwhile


dis_t = dis_t + 2
if ( dis_t>_endtime )
 runscript=0
endif 

endwhile

