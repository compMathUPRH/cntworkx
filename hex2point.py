import networkx as nx
import granules.structure.NAMDdata as gr

# Python Program to count 
# cycles of length n 
# in a given graph. 
class hexagon:
    def __init__(self,vert,coords):
        self.vertices = tuple(vert.tolist())
        self.coordinates = coords
        self.center = tuple(coords.mean(axis=0).tolist())
        
    def __str__(self):
        #permits printing
        return f"hexagon object with center:\n{self.center}\nvertices:\n{self.vertices} \ncoordinates:\n{self.coordinates}\n"
    
    def isneighbor(self, other): #adyacencia
        #check if has exacly 2 atoms in common with other hexagon
        return len(set(self.vertices).intersection(other.vertices)) == 2
    
    def __eq__(self,other):
        #permits use of ==
        return self.vertices == other.vertices
    
    def __ne__(self,other):
        #permits use of !=
        return self.vertices != other.vertices
    
    def __hash__(self):
        #para crear el grafo
        return hash((self.vertices,self.center))
    
    def __repr__(self):
        #mejor representación al imprimir edges del grafo
        t = tuple(f"{i:.2f}" for i in self.center)
        return f"hexagon{t}"
    

#from https://www.geeksforgeeks.org/cycles-of-length-n-in-an-undirected-and-connected-graph/
# Number of vertices 
#V=6
#lista para aguantar los ciclos y las marcas
LISTA = []

def DFS(graph, marked, n, vert, start, count, cycle): 
    global LISTA
	# mark the vertex vert as visited 
    marked[vert] = True
    cycle.append(vert)
    
    if cycle : # si cycle tiene algo
        LISTA.append(list(cycle))
	# if the path of length (n-1) is found 
    if n == 0: 
		# mark vert as un-visited to make it usable again. 
        marked[vert] = False
        cycle.pop()

		# Check if vertex vert can end with vertex start 
        if graph.has_edge(vert,start): 
            count = count + 1
            #print(cycle)
            #print('ok')
            LISTA.append(True) #marcar break-points
            return count 
        else: 
            return count 

	# For searching every possible path of 
	# length (n-1) 
    for i in range(V): 
        if marked[i] == False and graph.has_edge(vert,i): 

			# DFS for searching path by decreasing 
			# length by 1 
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
	marked = [False] * len(graph)

	# Searching for cycle by using v-n+1 vertices 
	count = 0
	for i in range(V-(n-1)): 
		count = DFS(graph, marked, n-1, i, i, count, []) 

		# ith vertex is marked as visited and 
		# will not be visited again. 
		marked[i] = True
	
	return int(count/2) 









# para leer cyclos y coordenadas
cnt = gr.NAMDdata("nanotubesv0.pdb","nanotubesv0.psf","nanotubesv0.prm")
psf = cnt.psf
V = psf.atoms.shape[0]
enlaces = zip(psf.bonds['atom1'],psf.bonds['atom2'])
g = nx.Graph(enlaces)


cycle_length = 6
print("Total cycles of length ",cycle_length," are ",countCycles(g, cycle_length)) #397 hrexagonos




rawlist = []
# this code is contributed by Shivani Ghughtyal 
for x in range(len(LISTA)): 
    if LISTA[x] == True: rawlist.append(frozenset(LISTA[x-1]))

S = set(rawlist)
print("---------")
FS = set([frozenset(e) for e in g.edges()])
print("-----------------")



#escoger columnas que nos interesan para hexagonos
cnt.pdb = cnt.pdb[['ID','x','y','z']]



hexagons = []
for verts in S:
    table = cnt.pdb[cnt.pdb['ID'].isin(verts)]
    #vertices
    v = table['ID'].values
    #coordenadas
    c = table[['x','y','z']].values 
    
    h = hexagon(v,c)
    hexagons.append(h)
    #print(h)



hex_connections = []
for h1 in hexagons:
    for h2 in hexagons:
        if h1.isneighbor(h2):
            hex_connections.append((h1,h2))

cgmol = nx.Graph(hex_connections)
print(cgmol.edges())

nx.draw(cgmol, with_labels=False, font_weight='bold')
print("total connections:")
print(len(cgmol.edges()))
#1165 connections
