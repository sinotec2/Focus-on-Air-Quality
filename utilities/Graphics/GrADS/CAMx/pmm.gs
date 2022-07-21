"reinit"
ispec=1
nm.1='PM25'
nm.2='PM10'
while(ispec<=2)
"open  1309_Hs.S.grd02LT"nm.ispec".ctl"
"q file 1"
timestring=sublin(result,5) ;*5th line of the result
hrs=subwrd(timestring, 12) ;*12th word of the dimension string
"set mpdraw off"
"set grid off"
"set gxout shaded"
i=1
while (i<=hrs)
"set t "i
"q dims"
timestring=sublin(result,5) ;*5th line of the result
datep=subwrd(timestring, 6) ;*6th word of the time string
datep=substr(datep,6,12)
"set grads off"
"color 0 80 5 -kind rainbow"
"set strsiz 0.1 0.08"
aspec=nm.ispec
"d "aspec
"set line 1 1"
"draw shp TWN_COUNTY.shp"
"cbar"
"set strsiz 0.2 0.16"
"draw string 2.2 10.5 "nm.ispec"(ug/M3) at "datep 
"printim "datep nm.ispec".png x850 y1100 white"
*pull dummy
"c"
i=i+1
endwhile
"close 1"
ispec=ispec+1
endwhile
quit
return
