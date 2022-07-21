"reinit"
ispec=1
nm.1='SO2'
nm.2='PM10'
while(ispec<=1)
"open  1309_Hs.S.grd02LD"nm.ispec"D.ctl"
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
datep=substr(datep,4,12)
dd=substr(datep,1,2)
if (dd='18' | dd='19')
"set grads off"
"color 2 16 2 -kind rainbow"
"set strsiz 0.1 0.08"
aspec=nm.ispec"D"
"d "aspec
"set line 1 1"
"draw shp TWN_COUNTY.shp"
"cbar"
"set strsiz 0.2 0.16"
"draw string 2.2 10.5 "nm.ispec"(ppb) at "datep 
"printim "datep nm.ispec".png x850 y1100 white"
*pull dummy
"c"
endif
i=i+1
endwhile
"close 1"
ispec=ispec+1
endwhile
quit
return
