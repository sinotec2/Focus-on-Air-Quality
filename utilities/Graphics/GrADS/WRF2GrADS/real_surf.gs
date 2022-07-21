'reinit'
'open real_cart.ctl'

** need input data on model levels

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

'define tf=(40+tc)*9/5-40'   

'c'
'set grads off'
'set gxout shaded'
'set clevs -20 -15 -10 -5  0  5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80'
'set ccols   0  51  53 55 57 58 59 49 47 45 39 37 36 34 22 23 24 25 27 29 29'
'set z 1'
'd tf'
'set gxout contour'
'set ccolor 1'
'set cthick 7'
'set cint 4'
'd slvl'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35 Surfcae T (F, color), SLP (mb)'
'set strsiz .15'
'set string 1 l 3'
'draw string 7.5 8.0 ' _analysis
'run cbar.gs'
if(ans)
'printim surface'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

