cp OMI-Aura_L3-OMI_MINDS_NO2d_2006m0228_v01-01-2022m0218t102329.nc OMI-Aura_L3-OMI_MINDS_NO2d_2006m0301_v01-01-2022m0218t102329.nc
cp OMI-Aura_L3-OMI_MINDS_NO2d_2006m0303_v01-01-2022m0218t102329.nc OMI-Aura_L3-OMI_MINDS_NO2d_2006m0302_v01-01-2022m0218t102329.nc
cp OMI-Aura_L3-OMI_MINDS_NO2d_2008m0927_v01-01-2022m0218t110347.nc OMI-Aura_L3-OMI_MINDS_NO2d_2008m0928_v01-01-2022m0218t110347.nc
cp OMI-Aura_L3-OMI_MINDS_NO2d_2008m0930_v01-01-2022m0218t110347.nc OMI-Aura_L3-OMI_MINDS_NO2d_2008m0929_v01-01-2022m0218t110347.nc
cp OMI-Aura_L3-OMI_MINDS_NO2d_2008m0930_v01-01-2022m0218t110350.nc OMI-Aura_L3-OMI_MINDS_NO2d_2008m0929_v01-01-2022m0218t110347.nc
cp OMI-Aura_L3-OMI_MINDS_NO2d_2016m0529_v01-01-2022m0218t115718.nc OMI-Aura_L3-OMI_MINDS_NO2d_2016m0530_v01-01-2022m0218t115718.nc
y=15;m=06;k=0;for l in {0..9};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}${l}*);f2=${f/2015/2016};do cp $f $f2;done
y=15;m=06;k=0;for l in {0..9};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}${l}*);f2=${f/2015/2016};cp $f $f2;done
cp OMI-Aura_L3-OMI_MINDS_NO2d_2016m0601_v01-01-2022m0218t114927.nc OMI-Aura_L3-OMI_MINDS_NO2d_2016m0531_v01-01-2022m0218t114927.nc
f=OMI-Aura_L3-OMI_MINDS_NO2d_2016m0610_v01-01-2022m0218t115721.nc
cp $f $f2
f2=${f/0610/0611}
f=OMI-Aura_L3-OMI_MINDS_NO2d_2016m0613_v01-01-2022m0218t115719.nc
f2=${f/0613/0612}
cp $f $f2
y=17;m=03;k=1;for l in {3..4};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}2*);f2=${f/0312/031$l};cp $f $f2;done
y=17;m=03;k=1;for l in 5 6;do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}7*);f2=${f/0317/031$l};cp $f $f2;done
cp OMI-Aura_L3-OMI_MINDS_NO2d_2019m1111_v01-01-2022m0218t124446.nc OMI-Aura_L3-OMI_MINDS_NO2d_2019m1112_v01-01-2022m0218t124446.nc
f=OMI-Aura_L3-OMI_MINDS_NO2d_2021m1229_v01-01-2022m0218t131919.nc
f2=${f/1229/1230}
cp $f $f2
f=OMI-Aura_L3-OMI_MINDS_NO2d_2022m1129_v01-01-2022m1204t132007.nc
f2=${f/1129/1130}
 1152  cp $f $f2
y=21;m=12;for l in {01..31};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}${l}*);f2=${f/2021/2022};cp $f $f2;done
y=21;m=12;for l in {01..31};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${l}*);f2=${f/2021/2022};cp $f $f2;done
f=OMI-Aura_L3-OMI_MINDS_NO2d_2021m1230_v01-01-2022m0218t131933.nc
f2=${f/m1230/m1231}
cp $f $f2
f=${f2/2021/2022}
cp $f2 $f
y=21;m=04;k=0;for l in {1..9};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}${l}*);f2=${f/2021m/2022m};cp $f $f2;done
y=21;m=04;k=1;for l in {0..4};do f=$(ls OMI-Aura_L3-OMI_MINDS_NO2d_20${y}m${m}${k}${l}*);f2=${f/2021m/2022m};cp $f $f2;done
