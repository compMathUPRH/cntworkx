"""
TO-DO
"""
#atom, index, false coords

from scipy.spatial.distance import pdist
import granules.structure.LAMMPSdata as ld
import numpy as np
import pandas as pd

lammps = ld.LammpsData('tubito.data')
atoms = lammps.atomproperty.atoms.copy()
atomIds = atoms[['aID']].copy()
a1 = atoms.set_index('aID')[['x', 'y', 'z']].values
distances = pdist(a1, 'euclidean')

distindex = 0
pairs = []
for i in atomIds.values.flatten():
    for j in atomIds.values.flatten():
        if i < j:
            pairs.append([i,j,distances[distindex]])
            distindex+=1

l = pd.DataFrame()
cols = ['atom1','atom2','distance']
for i in cols:
    l[i] = None

arr = pd.DataFrame(np.array(pairs))
arr.columns = cols
l = l.append(arr)
#filtrar dist == 0 DONE

l.sort_values('distance', inplace=True)
#sort DONE

#probar que no se repitan
#descartar extremos y sacar los atomos

l = l[:79]

lammps.topologia.bonds = lammps.topologia.bonds[0:0]
lammps.topologia.bonds[['Atom1','Atom2']] = l[['atom1','atom2']]
lammps.topologia.bonds['bID'] = range(1,80)
lammps.topologia.bonds['bType'] = 1

lammps.topologia.bonds = lammps.topologia.bonds.astype('int32')

lammps.writeConf('finaltube.data')




#TODO:

#separar los tubos y trabajarlos independientes cuando se tenga mas de uno

#generar tubos programaticamente* a diferentes angulos (0-90) grados con operaciones matriciales
# usar temperaturas diferentes (20 diffs)    1800 sims total

#









# para despues
#tomar linea de atomos y generar el tubo