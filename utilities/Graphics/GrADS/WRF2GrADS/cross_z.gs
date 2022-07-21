'reinit'
'open real_z.ctl'

** script needs z level data as input
** will create cross sections NS ; EW, in middle of domain

'set mpdset hires'
'set display color white'
'run rgbset.gs'

say 'Create gif images as well (1=yes ; 0=no)'
pull ans
frame = 1

'q file'
rec=sublin(result,5)
_endtime=subwrd(rec,12)
num_x=subwrd(rec,3)
num_y=subwrd(rec,6)
num_z=subwrd(rec,9)

dis_x=num_x/2
dis_y=num_y/2

runscript = 1
dis_t = 1
'set z 1 ' num_z
'set y ' dis_y

** DO EW cross section
while(runscript)
say 'Plotting EW cross section'
'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)
say 'Time is ' _analysis

'c'
'set grads off'
'set gxout shaded'
'set clevs 10 20 30 40 50 60 70 80 90 100'        
'set ccols 0 0 0  0 33 34 35 36 37 38  39'
'd rh'
'set gxout contour'
'set ccolor 1'
'set cthick 2'
'set cint 5'
'd tc'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35   E-W  Relative Humidity and T(C)'          
'set strsiz .15'
'set string 1 l 3'
'draw string 8.4 8.2 ' _analysis
'draw string 1.5 8.2 y=' dis_y
'run cbar.gs'
if(ans)
'printim crossEW'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

'reset'

runscript = 1
dis_t = 1
'set z 1 ' num_z
'set x ' dis_x


** DO NS cross section
say 'Plotting NS cross section'
while(runscript)
'set t ' dis_t
'q dims'
rec=sublin(result,5)
_analysis=subwrd(rec,6)
say 'Time is ' _analysis

'c'
'set grads off'
'set gxout shaded'
'set clevs 10 20 30 40 50 60 70 80 90 100'        
'set ccols 0 0 0  0 33 34 35 36 37 38  39'
'd rh'
'set gxout contour'
'set ccolor 1'
'set cthick 2'
'set cint 5'
'd tc'
'set strsiz .2'
'set string 1 l 6'
'draw string 2.7 8.35   N-S  Relative Humidity and T(C)'          
'set strsiz .15'
'set string 1 l 3'
'draw string 8.4 8.2 ' _analysis
'draw string 1.5 8.2 x=' dis_x
'run cbar.gs'
if(ans)
'printim crossNS'frame'.gif gif '
frame=frame+1
endif
pull dummy

if ( dis_t=_endtime )
 runscript=0
endif 
dis_t = dis_t + 1
endwhile

