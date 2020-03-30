import pandas as pd
import networkx as nx
from Polygon import Polygon
import hex2point #import DFS,countCycles,getCycles
from granules.structure.LAMMPSdata import LammpsData
from scipy.spatial.distance import pdist
import numpy as np

lammps = LammpsData('MultiTubes/EmptyDouble/Nanotubesed.data')
e = lammps.topologia.bonds
en = zip(e['Atom1'],e['Atom2'])
g = nx.Graph(en)
gs = tuple(nx.connected_components(g))
t1,t2 = gs

tubos = [LammpsData('MultiTubes/EmptyDouble/Nanotubesed.data') for i in range(len(gs))]

def removeAtoms(ldata,atomlist):
    #fully** remove atoms from a dataframe, given an iterable
    #atoms y bonds
    at = ldata.atomproperty.atoms.copy()
    at = at[~at['aID'].isin(atomlist)]
    ldata.atomproperty.atoms = at
    bd = ldata.topologia.bonds
    bd = bd[~(bd['Atom1'].isin(atomlist)|bd['Atom2'].isin(atomlist))]
    ldata.topologia.bonds = bd
    print(bd)




removeAtoms(tubos[0],t2)
removeAtoms(tubos[1],t1)
del lammps,e,en,g,t1,t2



offset = 0
ldataobs = []
for tubo in tubos:    
    hex2point.cycles_sets = set() #borra los anteriores
    enlaces = tubo.topologia.bonds # hace que sea mas legible
    tubo.atomproperty.atoms[['aID']]-= offset #arregla problemas con el DFS
    tubo.topologia.bonds[['Atom1','Atom2']] -= offset #arregla problemas con el DFS
    
    enlaces = tubo.topologia.bonds
    #enlaces[['Atom1','Atom2']] 
    print(enlaces)
    en = zip(enlaces['Atom1'],enlaces['Atom2'])
    graph = nx.Graph(en)
    
    cycle_length = 6
    print("Total cycles of length ",cycle_length," are ",hex2point.countCycles(graph, cycle_length)) 
    c = hex2point.getCycles()
    print('----------')
    print('length of c: ',len(c))
    
    
    crudehexagons = []
    for verts in c:
        #convertir a hexagonos
        hexagon_coordinates = tubo.atomproperty.atoms[tubo.atomproperty.atoms['aID'].isin(verts)]
        #v = hexagon_coordinates['ID'].values            #vertices
        coords = hexagon_coordinates[['x','y','z']].values   #coordenadas
        h = Polygon(verts,coords)
        crudehexagons.append(h)
    
    hex_connections = []
    for h1 in crudehexagons:
        for h2 in crudehexagons:
            if h1.isneighbor(h2):
                hex_connections.append((h1,h2))
    
    cgmol = nx.Graph(hex_connections)
    
    pentatube = LammpsData()
    newatoms = pd.DataFrame([[i,1,1,0]+list(h.center())+[0]*3 for i,h in enumerate(crudehexagons,start=1)])
    newatoms.columns = pentatube.atomproperty.atoms.columns
    pentatube.atomproperty.atoms = pentatube.atomproperty.atoms.append(newatoms)
    
    
    # añade aristas
    b = 0
    for i,h1 in enumerate(crudehexagons,start=1):
        for j,h2 in enumerate(crudehexagons,start=1):
            for v1 in h1.vertices:
                if v1 not in h2.vertices:
                    for v2 in h2.vertices:
                        if graph.has_edge(v1,v2) and len(h1.vertices.intersection(h2.vertices)) == 0:
                            pentatube.topologia.bonds.loc[b] = [b,1,i,j]
                            b +=1
    
    pentatube.topologia.bonds = pentatube.topologia.bonds.drop_duplicates(subset=['Atom1','Atom2'], inplace=False).reset_index(drop=True)
    pentatube.topologia.bonds['bID'] = pentatube.topologia.bonds.index.copy() + 1
    
    
    offset += tubo.atomproperty.atoms.shape[0]+1
    
    #para convertirlo en linea
    hex2point.cycles_sets = set() #borra los sets anteriores
    enlaces = pentatube.topologia.bonds
    enlaces = zip(enlaces['Atom1'],enlaces['Atom2'])
    g = nx.Graph(enlaces)
    
    cycle_length = 5
    print("Total cycles of length ",cycle_length," are ",hex2point.countCycles(g, cycle_length)) 
    c = hex2point.getCycles()
    
    crudepentagons = []
    for verts in c:
        #convertir a pentagonos
        pentagon_coordinates = pentatube.atomproperty.atoms[pentatube.atomproperty.atoms['aID'].isin(verts)]
        coords = pentagon_coordinates[['x','y','z']].values   #coordenadas
        h = Polygon(verts,coords)
        crudepentagons.append(h)
    
    pentagons = []
    for p in crudepentagons:
        temp = g.subgraph(p.vertices)
        if len(temp.edges()) == 5:
            pentagons.append(p)
        
    
    ld = LammpsData()
    newatoms = pd.DataFrame([[i,1,1,0]+list(h.center())+[0]*3 for i,h in enumerate(pentagons,start=1)])
    newatoms.columns = ld.atomproperty.atoms.columns
    ld.atomproperty.atoms = ld.atomproperty.atoms.append(newatoms)
    #Esta parte hace los bonds de la linea de atomos
    
    atoms = ld.atomproperty.atoms.copy()
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
    
    cols = ['atom1','atom2','distance']
    arr = pd.DataFrame(np.array(pairs))
    arr.columns = cols
    arr.sort_values('distance', inplace=True)
    arr = arr[:atoms.shape[0]-1]
    
    ld.topologia.bonds[['Atom1','Atom2']] = arr[['atom1','atom2']]
    ld.topologia.bonds['bID'] = range(1,ld.topologia.bonds.shape[0]+1)
    ld.topologia.bonds['bType'] = 1
    
    ld.topologia.bonds = ld.topologia.bonds.astype('int32')
    ld.writeConf('finaltube.data')
    
    ldataobs.append(ld)
    