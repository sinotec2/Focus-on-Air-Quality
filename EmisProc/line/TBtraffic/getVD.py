from pandas import *
import xml.etree.cElementTree as ET
fname='GetVDDATA'
tree=ET.ElementTree(file=fname)
ttxt=[elem.text for elem in tree.iter()]
id=set([elem.text for elem in tree.iter(tag='DeviceID')])
cols=['DeviceID','TotalOfLane','LaneNO','Volume','AvgSpeed','AvgOccupancy','Svolume','Mvolume','Lvolume']
v=[]
for i in xrange(len(cols)):
    v.append([])
for i in id:
    ist=ttxt.index(i)
    ttl=int(ttxt[ist+2])
    for j in xrange(ttl):
        v[0].append(i)
        v[1].append(ttl)
        istt=ist+4+j*8
        for k in xrange(2,len(cols)):
            v[k].append(ttxt[istt+k-2])
d={}
for i in xrange(len(cols)):
    d.update({cols[i]:v[i]})
cols.append('ExchangeTime')
d.update({cols[-1]:[ttxt[1] for x in xrange(len(v[0]))]})
df=DataFrame(d)
df[cols].set_index('DeviceID').to_csv('latest')
