class Polygon:
    def __init__(self,vert,coords):
        #self.vertices = tuple(vert.tolist())
        self.vertices = vert
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
        return f"{len(self.vertices)}-sided poligon with center{t}"
    
    def __contains__(self, vertex):
        return vertex in self.vertices
    
    def center(self):
        return tuple(self.coordinates.mean(axis=0).tolist())
