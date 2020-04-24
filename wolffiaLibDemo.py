'''
    Este programa requiere 
        export PYTHONPATH="<directorio de Wolffia> <directorio de granules"
       ejemplo:
        export PYTHONPATH="/home/jse/inv/wolffia/wolffia:/home/jse/inv/granules/package/granules"
'''

#import ChemicalGraph
from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.Mixture import Mixture
import numpy as np
from granules.structure.LAMMPSdata import LammpsData

mix = Mixture()

tubo1 = Tube(5,5,100)
centro = np.array(tubo1.center())
tubo1.moveby(-centro)
tubo2 = Tube(5,5,100)
tubo2.moveby(-centro)

tubo2.moveBy([10,0,0])
tubo2.rotateDeg(90,0,0)

mix.add(tubo1)
mix.add(tubo2)
#mix.writeFiles("dosTubos")

lmps = LammpsData().loadWolffiaMixture(mix)
lmps.writeConf("dosTubos.data")
