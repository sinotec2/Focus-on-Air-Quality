function main(args)
'reinit'
say "temps.gs " args
* Get arguments
if (args='?')
 say 'temps.gs requires 5 argument: hh apm day month year'
 say 'hh = hour'
 say 'apm = AM or PM'
 say 'day = day'
 say 'month = month'
 say 'year = year'
 return
else
 hh=subwrd(args,1);if(hh='');hh="";endif
 apm=subwrd(args,2);if(hh='');apm="";endif
 day=subwrd(args,3);if(hh='');day="";endif
 month=subwrd(args,4);if(hh='');month="";endif
 year=subwrd(args,5);if(hh='');year="";endif
 endif


'draw string 2.2 10.5 title Current Temperatures as of 'hh' 'apm' 'day' 'month' 'year
"printim tmp.png x850 y1100 white"
quit
return

