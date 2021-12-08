
# input df, index cols(list), value cols name(str)
# return matrix, index lists (in cols order)
def DF2Mat(dd,idx_lst,vname):
  import sys
  import numpy as np
  from pandas import DataFrame
  ret_lst, num_lst=[],[]
  for c in idx_lst:
    lst=eval('list(set(dd.'+c+'))');lst.sort()
    n=len(lst)
    ret_lst.append(lst);num_lst.append(n)
    dct={lst[i]:i for i in range(n)}
    dd['i'+c]=[dct[i] for i in dd[c]]
  mat=np.zeros(shape=num_lst)
  s='mat['+''.join(['dd.i'+c+'[:],' for c in idx_lst]).strip(',')+']=dd.'+vname+'[:]' 
  exec(s,locals())
  return mat, ret_lst

