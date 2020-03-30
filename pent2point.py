

# ESTE ARCHIVO NO FUNCIONA BIEN

import networkx as nx
import granules.structure.NAMDdata as nd
import granules.structure.LAMMPSdata as ld
from Polygon import Polygon
from hex2point import DFS,countCycles,getCycles
import pandas as pd

# para leer cyclos y coordenadas
cnt = ld.LammpsData("cgtube.data")


enlaces = cnt.topologia.bonds
enlaces = zip(enlaces['Atom1'],enlaces['Atom2'])
g = nx.Graph(enlaces)

cycle_length = 5
print("Total cycles of length ",cycle_length," are ",countCycles(g, cycle_length)) 
c = getCycles()
print('----------')



crudepentagons = []
for verts in c:
    #convertir a pentagonos
    pentagon_coordinates = cnt.atomproperty.atoms[cnt.atomproperty.atoms['aID'].isin(verts)]
    #v = hexagon_coordinates['ID'].values            #vertices
    coords = pentagon_coordinates[['x','y','z']].values   #coordenadas
    h = Polygon(verts,coords)
    crudepentagons.append(h)


pentagons = []
for p in crudepentagons:
    temp = g.subgraph(p.vertices)
    if len(temp.edges()) == 5:
        pentagons.append(p)
    


lammps = ld.LammpsData()
newatoms = pd.DataFrame([[i,1,1,0]+list(h.center())+[0]*3 for i,h in enumerate(pentagons,start=1)])
newatoms.columns = lammps.atomproperty.atoms.columns
lammps.atomproperty.atoms = lammps.atomproperty.atoms.append(newatoms)




lammps.writeConf('tubito.data')





#vv HEcho
#granules tabla nueva con distancia entre los atomos
#sort a la tabla
#descartar distancia 0
#enlazar distancias minimas
#pdist en 2 instrucciones