i=2
cd $gfs/${DOM[$i]}/ndown
cp namelist.input23_loop namelist.input
  for cmd in "s/SYEA/$yea1/g" "s/SMON/$mon1/g" "s/SDAY/$day1/g" \
             "s/EYEA/$yea2/g" "s/EMON/$mon2/g" "s/EDAY/$day2/g" ;do
    sed -i $cmd namelist.input
  done
rm metoa_em
for d in 2 3;do
  dd=$(( $d - 1 ))
  for id in {0..10};do
    for j in $(ls ../../met_em.d0${d}.${dates[$id]}_*);do
      k=${j/d0${d}/d0${dd}}
      l=${k/..\/..\//}
      m=${l/met_/metoa_};ln -s $j $m;done;done;done
LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin:/opt/mpich/mpich-3.4.2-icc/lib /opt/mpich/mpich-3.4.2-icc/bin/mpirun ${MPI[$i]} /nas1/WRF4.0/WRFv4.3/WRFV4/main/real.exe >& /dev/null

ln -sf wrfinput_d02 wrfndi_d02

for id in {0..10};do ln -sf $gfs/${DOM[3]}/wrfout_d02_${dates[$id]}_00:00:00 wrfout_d01_${dates[$id]}_00:00:00;done

sed -i 's/interval_seconds                    = 10800/interval_seconds                    = 3600/g' namelist.input

#ndown.exe is intel version
LD_LIBRARY_PATH=/nas1/WRF4.0/WRFv4.3/WRFV4/LIBRARIES/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/lib:/opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/lib/release:/opt/intel/compilers_and_libraries_2020.0.166/linux/mpi/intel64/libfabric/lib /opt/intel_f/compilers_and_libraries_2020.0.166/linux/mpi/intel64/bin/mpirun -np 10 /nas1/WRF4.0/WRFv4.3/WRFV4/main/ndown.exe >& /dev/null

rm wrfout*

## restore the real and ndown results
cd $gfs/${DOM[$i]}
for f in wrfinput wrfbdy wrffdda wrflowinp;do
  mv ndown/${f}_d02 ${f}_d01
done
