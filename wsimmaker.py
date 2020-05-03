from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.Mixture import Mixture
from granules.structure.LAMMPSdata import LammpsData
from multiprocessing import Pool
import numpy as np
import shutil
import os

from WolffiaState import WolffiaState
from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.molecule.solvent.WATER import WATER
from interface.textWidgets.PrintBar import PrintBar
#from lib.chemicalGraph.Mixture import Mixture
import numpy as np
from granules.structure.LAMMPSdata import LammpsData

# build a box
from lib.Container import Box



#abrir script de lammps para editar temperatura
lammps_script_file = "lammps.in"
script = open(lammps_script_file).readlines()

start_temp = 275
max_temp = 420
temp_step = 10

 
#ahora si es necesario crear nas de un objeto WolffiaState
tubo1 = Tube(5,5,100)
centro = np.array(tubo1.center())
tubo1.moveby(-centro)


def writetubemix(direc,angle):
    #crear objetos
    wolffia = WolffiaState()
    mix = wolffia.getMixture()
    
    #tubo1
    tubo1 = Tube(5,5,100)
    centro = np.array(tubo1.center())
    tubo1.moveby(-centro)
    
    #tubo2
    tubo2 = Tube(5,5,100)
    tubo2.moveby(np.array([10,0,0])-centro)
    #tubo2.moveBy([10,0,0])
    tubo2.rotateDeg(angle,0,0)
    
    #anadir tubos a la mezcla
    mix.add(tubo1)
    mix.add(tubo2)
    
    #crear caja
    mins, maxs = mix.enclosingBox()
    wolffia.setContainer(Box(1, (mins[0]-10, maxs[0]+10,
                             mins[1]-10, maxs[1]+10,
                             mins[2]-10, maxs[2]+10)))
    
    print(mix.nodes())
    cant = wolffia.getContainer().amountSolventMolecules(WATER)
    print("cantidad solvente = ", cant)
    bar = PrintBar(max_value=cant)
    mix.fillBox(wolffia.getContainer(), WATER(), cant, checkCollisions=True, progress=bar)
    print(mix.nodes())
    
    
    
    lmps = LammpsData().loadWolffiaMixture(wolffia.getMixture())
    filename = f"{direc}/tube{angle:02}deg.data"
    lmps.writeConf(filename)
    return filename

parent_folder="generated"
if not os.path.exists(parent_folder):
    os.makedirs(parent_folder)


og_folder=f"{parent_folder}/og"
if not os.path.exists(og_folder):
    os.makedirs(og_folder)

pool = Pool()
#se crean fuera del for para no calcular lo mismo mucha veces,se puede escribir lo mismo
#gennedfiles = pool.starmap(writeObj, zip([og_folder]*len(range(0,92,2)),range(0,92,2)))
gennedfiles = pool.starmap(writetubemix, zip([og_folder],range(0,92,2)))
pool.close()
pool.join()
print(gennedfiles)


    
#for temp in range(start_temp, max_temp, temp_step):
for temp in [350]:
    pre = script[22][:20]
    suf = script[22][37:]
    mod_temp = f'{pre}{temp:.1f} {temp:.1f} 100.0{suf}'
    tdirectory = f"{parent_folder}/tubes{temp}k"
    

    if not os.path.exists(tdirectory):
        os.makedirs(tdirectory)

    for i in gennedfiles:
        subdir = f"{tdirectory}/{i.split('/')[-1].split('.')[0]}" 
        print(subdir)
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        
        open(f"{subdir}/lammps.in","w").writelines(script[:22]+[mod_temp]+script[23:])
        shutil.copy(i, f"{subdir}/tube.data")


