import networkx as nx
import granules.structure.NAMDdata as gr

# Python Program to count 
# cycles of length n 
# in a given graph. 
class Hexagon:
    def __init__(self,vert,coords):
        self.vertices = tuple(vert.tolist())
        self.coordinates = coords
        #self.center = tuple(coords.mean(axis=0).tolist()) # redundancia peligrosa
        
    def __str__(self):
        #permits printing
        return f"hexagon object with center:\n{self.center}\nvertices:\n{self.vertices} \ncoordinates:\n{self.coordinates}\n"
    
    def isneighbor(self, other): #adyacencia
        #check if has exacly 2 atoms in common with other hexagon
        return len(frozenset(self.vertices).intersection(other.vertices)) == 2
    
    def __eq__(self,other):
        #permits use of ==
        return self.vertices == other.vertices
    
    def __ne__(self,other):
        #permits use of !=
        return self.vertices != other.vertices
    
    def __hash__(self):
        #para crear el grafo
        return hash((self.vertices,self.center()))
    
    def __repr__(self):
        #mejor representación al imprimir edges del grafo
        t = tuple(f"{i:.2f}" for i in self.center())
        return f"hexagon{t}"
    
    def center(self):
        return tuple(self.coordinates.mean(axis=0).tolist())

#from https://www.geeksforgeeks.org/cycles-of-length-n-in-an-undirected-and-connected-graph/
# Number of vertices 
#V=6

def DFS(graph, marked, n, vert, start, count, cycle): 
    global cycles_sets
	
    marked[vert] = True  # mark the vertex vert as visited 
    cycle.append(vert)
    
    if n == 0:  # if the path of length (n-1) is found 
        cycle_as_set = frozenset(cycle)
        if graph.has_edge(vert,start): # Check if vertex vert can end with vertex start 
            count = count + 1
            cycles_sets.add(cycle_as_set)
            #print(cycle)
            #cycles_sets.append(True) #marcar break-points
            #return count # fin con mismo return en if y else => va afuera
        #else: 
            #return count  # fin con mismo return en if y else => va afuera

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
    
    v = hexagon_coordinates['ID'].values            #vertices
    
    c = hexagon_coordinates[['x','y','z']].values   #coordenadas
    
    h = Hexagon(v,c)
    hexagons.append(h)



hex_connections = []
for h1 in hexagons:
    for h2 in hexagons:
        if h1.isneighbor(h2):
            hex_connections.append((h1,h2))

print(hex_connections)
cgmol = nx.Graph(hex_connections)
#print(cgmol.edges())

nx.draw(cgmol, with_labels=False, font_weight='bold')
print("total connections:")
print(len(cgmol.edges()))
