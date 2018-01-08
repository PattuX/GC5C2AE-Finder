import xml.etree.ElementTree as et
import copy
queries = ['geocaching.loc']
gcs5 = []
gcs4 = []

for q in queries:
    t = et.parse(q)
    root = t.getroot()
    for child in root.iter("name"):
        code=child.attrib["id"][2:]
        if len(code)==5:
            gcs5.append(code)
        elif len(code)==4:
            gcs4.append(code)
        else:
            print(dropped(code))

print("Caches in all PQs:",len(gcs5)+len(gcs4))

gcs5 = list(set(gcs5))
gcs4 = list(set(gcs4))
for gcs in [gcs5, gcs4]:
    to_be_removed = []
    for gc in gcs:
        if any(gc.count(c)-1 for c in gc):
            to_be_removed.append(gc)
    for gc in to_be_removed:
        gcs.remove(gc)

l5=len(gcs5)
l4=len(gcs4)
print("Caches without double characters:",l5+l4)

combinations = []

for i1 in range(l4):
    s=gcs4[i1]
    for i2 in range(i1,l4):
        if all(c not in s for c in gcs4[i2]):
            s+=gcs4[i2]
            for i3 in range(i2,l4):
                if all(c not in s for c in gcs4[i3]):
                    s+=gcs4[i3]
                    for i4 in range(i3,l4):
                        if all(c not in s for c in gcs4[i4]):
                            s+=gcs4[i4]
                            ### 5 digit codes from here on
                            for i5 in range(l5):
                                if all(c not in s for c in gcs5[i5]):
                                    s+=gcs5[i5]
                                    for i6 in range(i5,l5):
                                        if all(c not in s for c in gcs5[i6]):
                                            s+=gcs5[i6]
                                            for i7 in range(i6,l5):
                                                if all(c not in s for c in gcs5[i7]):
                                                    s+=gcs5[i7]
                                                    combinations.append([gcs4[i1], gcs4[i2], gcs4[i3], gcs4[i4], gcs5[i5], gcs5[i6], gcs5[i7]])
                                                    s=s.replace(gcs5[i7],"")
                                            s=s.replace(gcs5[i6],"")
                                    s=s.replace(gcs5[i5],"")
                            s=s.replace(gcs4[i4],"")
                    s=s.replace(gcs4[i3],"")
            s=s.replace(gcs4[i2],"")
    print("Progress: "+str(int((i1+1)/l4*100))+"%", end="\r")

print(len(combinations), "combinations found")

for i,c in enumerate(combinations):
    tree = copy.deepcopy(t)
    root = tree.getroot()
    for wp in root.findall("waypoint"):
        if wp.find("name").get("id") not in ["GC"+x for x in c]:
            root.remove(wp)
    tree.write("Schmiederoute"+str(i+1)+".loc")
