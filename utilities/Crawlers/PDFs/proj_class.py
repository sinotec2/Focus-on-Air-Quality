import os, json

with open('proj_calss.html','r') as f:
    lines=[i for i in f]
a=[i for i in lines if "value=" in i and 'B' in i]
b=[i for i in a if '<' in i and '>' in i]
cat_Bnum=[i.split('"')[1] for i in a]
cat_CNnam=[i.split('>')[1].split('<')[0] for i in b]
for i in range(len(b)):
    dd=cat_Bnum[i]+'_'+cat_CNnam[i]
    dd=dd.replace('(','▒~H').replacce(')','▒~I' )
    os.system('mkdir -p '+dd)

dd={i:j for i,j in zip(cat_Bnum,cat_CNnam)}
with open('proj_class.json','+w',encoding='utf8') as f:
    json.dump(dd, f)
with open('proj_class.json','r') as f:
    bb=json.load(f)

print(dd==bb)
