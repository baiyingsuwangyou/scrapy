d={}
a=['1','2','1','3']
for i in a:
    d[i]=d.get(i,0)+1
print(d)