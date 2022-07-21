"reinit"
"open  1309_Hs.S.grd02LO3.ctl"
"q file 1"
timestring=sublin(result,5) ;*5th line of the result
hrs=subwrd(timestring, 12) ;*12th word of the dimension string
"set mpdraw off"
"set grads off"
"set grid off"
"set gxout shaded"
i=2
while (i<=hrs)
"set t "i
"q dims"
timestring=sublin(result,5) ;*5th line of the result
datep=subwrd(timestring, 6) ;*6th word of the time string
datep=substr(datep,1,2) L substr(datep,4,12)
hh=substr(datep,1,2)
dd=substr(datep,4,2)
if (dd='18' | dd='19')
if (hh='11' | hh='13' | hh='15' | hh='17')
"color 40 160 10 -kind rainbow"
"set strsiz 0.1 0.08"
"d O3"
"draw shp TWN_COUNTY.shp"
"cbar"
"set strsiz 0.2 0.16"
"draw string 2.2 10.5 O3(ppb) at "datep 
"printim "datep".png x850 y1100 white"
"c"
endif
endif
i=i+2
endwhile
"close 1"
quit
return
