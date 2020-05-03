'''
    Este programa requiere 
        export PYTHONPATH="<directorio de Wolffia> <directorio de granules"
       ejemplo:
        export PYTHONPATH="/home/jse/inv/wolffia/wolffia:/home/jse/inv/granules/package/granules"
'''



#import ChemicalGraph
from WolffiaState import WolffiaState
from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.molecule.solvent.WATER import WATER
from interface.textWidgets.PrintBar import PrintBar
#from lib.chemicalGraph.Mixture import Mixture
import numpy as np
from granules.structure.LAMMPSdata import LammpsData

wolffia = WolffiaState()
mix = wolffia.getMixture()
#mix = Mixture()

tubo1 = Tube(5,5,100)
centro = np.array(tubo1.center())
tubo1.moveby(-centro)
tubo2 = Tube(5,5,100)
tubo2.moveby(-centro)

tubo2.moveBy([10,0,0])
tubo2.rotateDeg(40,0,0)

mix.add(tubo1)
mix.add(tubo2)

# build a box
from lib.Container import Box
'''
center, radius = mix.boundingSphere()
radius += 6.0
wolffia.setContainer(Box(1, (center[0]-radius, center[0]+radius, 
                             center[1]-radius, center[1]+radius,
                             center[2]-radius, center[2]+radius)))
'''
mins, maxs = mix.enclosingBox()
wolffia.setContainer(Box(1, (mins[0]-10, maxs[0]+10, 
                             mins[1]-10, maxs[1]+10,
                             mins[2]-10, maxs[2]+10)))


# solvate
print(mix.nodes())
cant = wolffia.getContainer().amountSolventMolecules(WATER)
print("cantidad solvente = ", cant)
bar = PrintBar(max_value=cant)
mix.fillBox(wolffia.getContainer(), WATER(), cant, checkCollisions=True, progress=bar)
print(mix.nodes())

lmps = LammpsData().loadWolffia(wolffia)
lmps.writeConf("dosTubos.data")
