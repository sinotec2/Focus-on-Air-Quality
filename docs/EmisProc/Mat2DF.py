
# input any ranks of matrix a
# return df which columns is [col_1,col_2 ... col_ndim, val]
def Mat2DF(a):
  import sys
  import numpy as np
  from pandas import DataFrame
  ndim=a.ndim
  if ndim<2:sys.exit('ndim too small, no need to convert')
  H,T,C,N='[', ']', ':,', 'None,'
  ranks=[]
  for n in range(ndim):
    s=H
    for i in range(ndim):
      m=N
      if i==n:m=C
      s+=m    
    ranks.append(s.strip(',')+T)
  DD={}
  for i in range(ndim):
    var=np.zeros(shape=a.shape,dtype=int)
    var[:]=eval('np.array([j for j in range(a.shape[i])],dtype=int)'+ranks[i],locals())
	DD['col_'+str(i+1)]=var[:].flatten()
  DD['val']=a.flatten()
  return DataFrame(DD)

