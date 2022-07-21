'reinit'
'open hill2d.ctl'

** need normal model level data

'set display color white'
'run rgbset.gs'

say 'Create gif images as well (1=yes ; 0=no)'
pull ans
frame = 1

'q file'
rec=sublin(result,5)
_endtime=subwrd(rec,12)

runscript = 1
dis_t = 19

'set xlab off'
'set ylab off'
'set z 1 35 '

while(runscript)

'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)

say 'Time is ' _analysis
'c'
'set grads off'
'set gxout shaded'
'd theta'
'set gxout contour'
'd u'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0 8.35   Theta (color), u(m/s)'
'set strsiz .15'
'set string 1 l 3'
'draw string 8.5 8.1 ' _analysis
'run cbar.gs'
if(ans)
'printim hill2d'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd theta'
'set gxout contour'
'd w'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0.7 8.35   Theta (color), w (m/s)'
'set strsiz .15'
'set string 1 l 3'
'draw string 8.5 8.1 ' _analysis
'run cbar.gs'
if(ans)
'printim hill2d'frame'.gif gif '
frame=frame+1
endif
pull dummy
dis_t = dis_t + 6
if ( dis_t>_endtime )
 runscript=0
endif 

endwhile

