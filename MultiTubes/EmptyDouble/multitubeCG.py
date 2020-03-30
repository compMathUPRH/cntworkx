from Polygon import Polygon
from hex2point import DFS,countCycles,getCycles
import pandas as pd

import granules.structure.LAMMPSdata as ld
import networkx as nx

lammps = ld.LammpsData('Nanotubesed.data')
e = lammps.topologia.bonds
enlaces = zip(e['Atom1'],e['Atom2'])
g = nx.Graph(enlaces)

tubo1,tubo2 = list(nx.connected_components(g))


