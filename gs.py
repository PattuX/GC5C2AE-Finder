import xml.etree.ElementTree as et
queries = ['geocaching.loc']
gcs = []

for q in queries:
    t = et.parse(q)
    root = t.getroot()
    for child in root.iter("name"):
        gcs.append(child.attrib["id"][2:])

print("Caches in all PQs:",len(gcs))
gcs = list(set(gcs))
print("Non-duplicate caches:",len(gcs))
to_be_removed = []

for gc in gcs:
    if any(gc.count(c)-1 for c in gc):
        to_be_removed.append(gc)
for gc in to_be_removed:
    gcs.remove(gc)

l=len(gcs)
print("Caches without double characters:",l)

for i1 in range(l):
    s=gcs[i1]
    for i2 in range(i1,l):
        if all(c not in s for c in gcs[i2]):
            s+=gcs[i2]
            for i3 in range(i2,l):
                if all(c not in s for c in gcs[i3]):
                    s+=gcs[i3]
                    for i4 in range(i3,l):
                        if 16<=len(s+gcs[i6])<=19 and all(c not in s for c in gcs[i4]):
                            s+=gcs[i4]
                            for i5 in range(i4,l):
                                if 21<=len(s+gcs[i6])<=23 and all(c not in s for c in gcs[i5]):
                                    s+=gcs[i5]
                                    for i6 in range(i5,l):
                                        if 26<=len(s+gcs[i6])<=27 and all(c not in s for c in gcs[i6]):
                                            s+=gcs[i6]
                                            for i7 in range(i6,l):
                                                if all(c not in s for c in gcs[i7]):
                                                    s+=gcs[i7]
                                                    if len(s)==31:
                                                        print(gcs[i1], gcs[i2], gcs[i3], gcs[i4], gcs[i5], gcs[i6], gcs[i7], i1,i2,i3,i4,i5,i6,i7)
                                                    s.replace(gcs[i7],"")
                                            s=s.replace(gcs[i6],"")
                                    s=s.replace(gcs[i5],"")
                            s=s.replace(gcs[i4],"")
                    s=s.replace(gcs[i3],"")
            s=s.replace(gcs[i2],"")
    print(i1)
