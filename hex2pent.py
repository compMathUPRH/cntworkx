import networkx as nx
import granules.structure.NAMDdata as gr
from Polygon import Polygon
# Python Program to count 
# cycles of length n 
# in a given graph. 


#from https://www.geeksforgeeks.org/cycles-of-length-n-in-an-undirected-and-connected-graph/
# Number of vertices 
#V=6

def DFS(graph, marked, n, vert, start, count, cycle): 
    global cycles_sets
	
    marked[vert] = True  # mark the vertex vert as visited 
    cycle.append(vert)
    
    if n == 0:  # if the path of length (n-1) is found 
        if graph.has_edge(vert,start): # Check if vertex vert can end with vertex start 
            count = count + 1
            cycles_sets.add(frozenset(cycle))
            #print(cycle)

        # mark vert as un-visited to make it usable again. 
        marked[vert] = False
        cycle.pop()

        return count 
	# For searching every possible path of length (n-1) 
    for i in graph.nodes(): 
        if not marked[i] and graph.has_edge(vert,i): 
            # DFS for searching path by decreasing length by 1 
            count = DFS(graph, marked, n-1, i, start, count,cycle) 

	# marking vert as unvisited to make it 
	# usable again. 
    marked[vert] = False
    cycle.pop()
    return count 

# Counts cycles of length 
# N in an undirected 
# and connected graph. 
def countCycles( graph, n): 
    # all vertex are marked un-visited initially. 
    marked = [False] * (len(graph) + 1)

    # Searching for cycle by using v-n+1 vertices s
    count = 0
    for atom in graph.nodes():
        #print("start: " , atom, " con adyacencias ", graph.neighbors(n))
        count = DFS(graph, marked, n-1, atom, atom, count, []) 
        
        # ith vertex is marked as visited and 
        # will not be visited again. 
        #marked[atom] = True
	
    return int(count/2) 

def getCycles():
    return cycles_sets




cycles_sets = set()

if __name__ == "__main__":
    
    # para leer cyclos y coordenadas
    cnt = gr.NAMDdata("nanotubesv0.pdb","nanotubesv0.psf","nanotubesv0.prm")
    
    psf = cnt.psf
    V = psf.atoms.shape[0]
    enlaces = zip(psf.bonds['atom1'],psf.bonds['atom2'])
    g = nx.Graph(enlaces)
    
    cycle_length = 6
    cycles_sets = set()  #cycles_sets para aguantar los ciclos
    
    
    print("Total cycles of length ",cycle_length," are ",countCycles(g, cycle_length)) #397 hrexagonos
    print("Total unique cycles of length ",cycle_length," are ",len(cycles_sets)) #397 hrexagonos
    
    
    #escoger columnas que nos interesan para hexagonos
    cnt.pdb = cnt.pdb[['ID','x','y','z']]
    
    
    
    hexagons = []
    for verts in cycles_sets:
        hexagon_coordinates = cnt.pdb[cnt.pdb['ID'].isin(verts)]
        #v = hexagon_coordinates['ID'].values            #vertices
        c = hexagon_coordinates[['x','y','z']].values   #coordenadas
        h = Polygon(verts,c)
        hexagons.append(h)
    
    #---
    
    hex_connections = []
    for h1 in hexagons:
        for h2 in hexagons:
            if h1.isneighbor(h2):
                hex_connections.append((h1,h2))
    
    print(hex_connections)
    cgmol = nx.Graph(hex_connections)
    
    
    # create LAMMS structure
    import granules.structure.LAMMPSdata as LAMMPSdata
    import pandas as pd
    
    
    lammps = LAMMPSdata.LammpsData()
    newatoms = pd.DataFrame([[i,1,1,0]+list(h.center())+[0]*3 for i,h in enumerate(hexagons,start=1)])
    newatoms.columns = lammps.atomproperty.atoms.columns
    lammps.atomproperty.atoms = lammps.atomproperty.atoms.append(newatoms)
    
    #print(lammps.atomproperty.atoms)
    
    # añade aristas
    b = 1
    for i,h1 in enumerate(hexagons,start=1):
        for j,h2 in enumerate(hexagons,start=1):
            for v1 in h1.vertices:
                if v1 not in h2.vertices:
                    for v2 in h2.vertices:
                        #if g.has_edge(v1,v2):
                        if g.has_edge(v1,v2) and len(h1.vertices.intersection(h2.vertices)) == 0:
                            lammps.topologia.bonds.loc[b] = [b,1,i,j]
                            if b < 20: print(h1.vertices,h2.vertices,v1,v2)
                            b+=1
                            
    #print(lammps.topologia.bonds.columns)
    #lammps.topologia.bonds = lammps.topologia.bonds.drop_duplicates(subset=['Atom1','Atom2'], inplace=False).reset_index(drop=True)
    #lammps.topologia.bonds['bID'] = lammps.topologia.bonds.index.copy() + 1
    print(lammps.topologia.bonds)
    
    
    lammps.writeConf('pentaprism.data')
    
    # buscar pentagonos
