#!/usr/bin/python3

import granules.structure.LAMMPSdata as ld
#import pandas as pd
import cntchecker
from sys import argv


print(argv)

tube_file = "tube.data"
dump_file = "tube.dump"

cnt = ld.LammpsData(tube_file)
last = cntchecker.read_dump(dump_file)[-1]

#incluir estas dos cosas en la funcion original
last.index +=1
last = last.round(3)

print(last)
if cnt.atomproperty.atoms.shape[0] == last.shape[0]:
    print(cnt.atomproperty.atoms)
    cnt.atomproperty.atoms[['x','y','z']] = last[['xs','ys','zs']]
    print(cnt.atomproperty.atoms)
    print(last)
