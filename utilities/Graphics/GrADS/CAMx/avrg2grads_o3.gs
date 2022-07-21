function main(args)
'reinit'
say "avrg2grads.gs " args
* Get arguments
if (args='?' | args='')
 say '2d daily-mean AVRG file to grads_shaded plot'
 say 'avrg2grads FILE SPEC day'
 say 'FILE: avrg format file'
 say 'SPEC: speciate name'
 say 'day1: designated date'
 say 'day2: designated date'
 return
else
 FILE=subwrd(args,1)
 SPEC=subwrd(args,2)
 day1=subwrd(args,3)
 day2=subwrd(args,4)
endif
"open "FILE SPEC".ctl"
"q file 1"
timestring=sublin(result,5) ;*5th line of the result
hrs=subwrd(timestring, 12) ;*12th word of the dimension string
rec = sublin(result,7)
spnm=subwrd(rec,4)
spun=subwrd(rec,5)

"set mpdraw off"
"set grads off"
"set grid off"
"set gxout shaded"
alg2=math_log10(2)
alg3=math_log10(3)
alg5=math_log10(5)
"set gxout stat"
ymx0=-9999
ymn0=9999
i=1
while (i<=hrs)
"set t "i
"q dims"
timestring=sublin(result,5) ;*5th line of the result
datep=subwrd(timestring, 6) ;*6th word of the time string
datep=substr(datep,1,2) L substr(datep,4,12)
dd=substr(datep,4,2)
hh=substr(datep,1,2)
if (dd>=day1 & dd<=day2 )
if (hh='11' | hh='13' | hh='15' | hh='17')
"d "SPEC
data = sublin(result,8)
ymx = subwrd(data,5)
ymn = subwrd(data,4)
if(ymx0 < ymx);ymx0=ymx;endif
if(ymn0 > ymn);ymn0=ymn;endif
endif
endif
i=i+1
endwhile
ymn=ymn0
ymx=ymx0
if(ymn < 0);ymn=0;endif
alg=math_log10(ymx-ymn)
nlg=math_int(alg)
aaa=alg-nlg
div=math_pow(10,(nlg-1))
mdiv=5*div
if(aaa < alg5);mdiv=3*div;endif
if(aaa < alg3);mdiv=2*div;endif
if(aaa < alg2);mdiv=1*div;endif
say aaa','alg2','alg5','mdiv','nlg','div
*ymn=math_int(ymn/mdiv)*mdiv
ymn=mdiv
i=2
while (i<=hrs)
"set t "i
"q dims"
timestring=sublin(result,5) ;*5th line of the result
datep=subwrd(timestring, 6) ;*6th word of the time string
datep=substr(datep,1,2) L substr(datep,4,12)
hh=substr(datep,1,2)
dd=substr(datep,4,2)
if (dd>=day1 & dd<=day2 )
if (hh='11' | hh='13' | hh='15' | hh='17')
"set grads off"
"color " ymn" " ymx" " mdiv" -kind rainbow"
"set strsiz 0.1 0.08"
"d O3"
"set line 1 1"
"draw shp TWN_COUNTY.shp"
"cbar"
"set strsiz 0.2 0.16"
"draw string 2.2 10.5 O3(ppb) at "datep 
"printim "datep SPEC".png x1000 y1200 white"
"c"
endif
endif
i=i+2
endwhile
"close 1"
quit
return
function int(num)
  outnum = ''
  i = 1
  while(i <= strlen(num))
    char = substr(num,i,1)
    if(char = ".")
      break
    else
      outnum = outnum%char
      i = i+1
    endif
  endwhile

return outnum
