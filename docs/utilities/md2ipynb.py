import numpy as np
import sys, json

fname=sys.argv[1]
fnameO=fname.replace('md','ipynb')
with open(fname,'r') as f:
  l=[i for i in f]
nln=len(l)
for n in range(nln):
  for b in ['{:6d}  ','{:6d} \n','{:6d}\n']:
    s=b.format(n)
    for m in range(nln):
      if s in l[m]:l[m]=l[m].replace(s,'')
idx=[i for i in range(len(l)) if l[i][:3]=='```']
ncells=len(idx)//2
if len(idx)%2 !=0 : sys.exit('wrong pair in code quotations')

beg,end=[idx[i*2]+1 for i in range(ncells)], [idx[i*2+1] for i in range(ncells)]
mbeg,mend=[0],[beg[0]-1]
mbeg+=[i+1 for i in end[0:]]
mend+=beg[1:]
nmarks=ncells
if end[-1]<nln:
  nmarks+=1
  mend+=[nln]
ipynb={
'cells':{},
'nbformat':4,
'nbformat_minor':5,
'metadata':{
  'kernelspec':{ 
	'display_name': 'Python 3 (ipykernel)',
	'language': 'python',
	'name': 'python3',
	},
  'language_info': {
	'codemirror_mode': {'name': 'ipython', 'version': 3},
	'file_extension': '.py',
	'mimetype': 'text/x-python',
	'name': 'python',
	'nbconvert_exporter': 'python',
	'pygments_lexer': 'ipython3',
	'version': '3.9.7'
	}
  }
}
#code lines
codes=[{
	'cell_type': 'code',
	'execution_count': i+1,
	'id': '{:08d}'.format(i*2+1),
	'metadata': {},
	'outputs': [],
	'source': l[beg[i]:end[i]],
	} for i in range(ncells)]
#mark lines
marks=[{
   "cell_type": "markdown",
   "id": '{:08d}'.format(i*2),
   "metadata": {},
   "source": l[mbeg[i]:mend[i]],
	} for i in range(nmarks)]
mix=[]
for i in range(ncells):
  mix+=[marks[i],codes[i]]
if nmarks>ncells:
  mix+=[marks[-1]]
ipynb['cells']=mix
with open(fnameO,'w', newline='') as jsonfile:
  json.dump(ipynb, jsonfile)

