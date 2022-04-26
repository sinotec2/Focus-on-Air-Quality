---
layout: default
title:  程式庫之編譯
parent:   NetCDF Relatives
grand_parent: Utilities
last_modified_date: 2022-04-26 16:14:13
---
# NC相關程式庫之編譯
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## HDF
```bash
source /opt/intel/bin/compilervars.sh intel64
source /opt/intel_f/bin/compilervars.sh intel64
FC=ifort FCFLAG='-auto -warn notruncated_source -Bstatic -static-intel -O3 -unroll -stack_temps -safe_cray_ptr -convert big_endian -assume byterecl -traceback -xHost -qopenmp' CC=icc ../configure --prefix=/opt/hdf/hdf5_intel
```

```bash
FC=gfortran ./configure --enable-fortran --with-zlib=/usr/lib64 --prefix=/opt/hdf/hdf5_gcc
```

