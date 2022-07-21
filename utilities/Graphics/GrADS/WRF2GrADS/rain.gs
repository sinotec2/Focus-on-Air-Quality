'reinit'
'open real_p.ctl'

** Need a real dataset that contain rainc and rainnc

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

'c'
'set grads off'
'set gxout shaded'
'set clevs .1 .2 .4 .8 1.6 3.2 6.4 12.8 25.6 51.6 '
'set ccols 0  33 34 35 36 37 38 39 7 8 2'
'd rainc+rainnc'
*'draw title Total Precip (color,mm)'
'set strsiz .2'
'set string 1 l 6'
'draw string 3.2 8.35 Total Precip (color,mm)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'run cbar.gs'
if(ans)
'printim raintotal'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

