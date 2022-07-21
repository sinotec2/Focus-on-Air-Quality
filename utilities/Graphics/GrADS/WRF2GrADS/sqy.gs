'reinit'
'open sqy.ctl'

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

'set xlab off'
'set ylab off'

while(runscript)

'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)

say 'Time is ' _analysis
'c'
'set grads off'
'set gxout shaded'
'd qvapor*1000.0'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0 8.35   Water Vapor (g/kg)'
'set strsiz .15'
'set string 1 l 3'
'draw string 8.5 8.1 ' _analysis
'run cbar.gs'
if(ans)
'printim sqy'frame'.gif gif '
frame=frame+1
endif
pull dummy
'c'
'set grads off'
'set gxout shaded'
'd qcloud*1000.0'
'set gxout contour'
'set cmin 0.01'
'd qrain*1000.0'
'set strsiz .2'
'set string 1 l 6'
'draw string 4.0.7 8.35   Cloud (color) and rain (g/kg)'
'set strsiz .15'
'set string 1 l 3'
'draw string 8.5 8.1 ' _analysis
'run cbar.gs'
if(ans)
'printim sqy'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

