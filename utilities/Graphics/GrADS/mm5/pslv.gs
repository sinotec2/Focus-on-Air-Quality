'reinit'
'clear'
*  say '1:d1'
*  say '2:d4'
*  pull file
file = 1
date = 100802
while (date <= 100807)
  if(file=1)
   'open 'date'.ctl'
   'set lon 90.0 150.'
   'set lat 0.  50'
  else
   'open 'date'.ctl'
   'set lon 119.5 122.5'
   'set lat 21.5  25.7'
  endif
'set parea 0 11 0.5 8.2'
'set string 1 bc'
'set strsiz 0.15'
'set csmooth on'
'q hardware'
rec = sublin(result,2)
_cols = subwrd(rec,4)
if (_cols=256)
  'set rgb 30 0 80 0'
  'set rgb 31 0 110 0'
  'set rgb 32 0 150 0'
  'set rgb 33 0 200 0'
  'set rgb 34 0 250 0'
  'set rgb 35 150 255 0'
endif
'set mpdset hires'
'set map auto'
'set grid off'
t = 0
say ' delta -t (hr)'
*pull dt
dt = 1
while (t <= 120)
  'clear'
  t = t + dt
  hr = t
  'set t 't
* calculate the hour of day
  if (t>24)
  hr=t-24
  endif
  say 'Time = 't'  ('hr'hr 'iday'day) (quit by ^C enter)'
  rc = doa(date,hr)
   if (t>='24')
    break
   endif
endwhile
   'reinit'
  date = date + 1
endwhile
quit
return

*  Do  Streamlines and Isotachs

function doa(date,hr)
'clear'
'set map 9'
'set gxout shaded'
'set cint 200'
'set grads off'
*'d mag(u,v)'
*'d ter'

* 'set gxout barb' !nogood
* 'set gxout stream'
*'set gxout vector'
*'set ccolor 15'
*'set grads off'
*'d u;v'

'set gxout contour'
'set cint 1'
'set ccolor 1'
'set line 0 0'
'set grads off'
'd pslv'

*if (hr=1)
'draw string 5.5 8.30  Sea Level Pressure at 'date'/'hr'Z 01OBS'
*endif
'printim 'date'-'hr'd1.png x1000 y800 white'
*pull dummy
*enter for next step
return
