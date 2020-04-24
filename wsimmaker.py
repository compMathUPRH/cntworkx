from lib.chemicalGraph.molecule.allotrope.Tube import Tube
from lib.chemicalGraph.Mixture import Mixture
from granules.structure.LAMMPSdata import LammpsData
from multiprocessing import Pool
import numpy as np
import shutil
import os

#abrir script de lammps para editar temperatura
lammps_script_file = "lammps.in"
script = open(lammps_script_file).readlines()

start_temp = 275
max_temp = 420
temp_step = 10

#no es necesario crear un mismo tubo muchas veces
tubo1 = Tube(5,5,100)
centro = np.array(tubo1.center())
tubo1.moveby(-centro)


def writeObj(direc,angle):
    mix = Mixture()
    tubo2 = Tube(5,5,100)
    tubo2.moveby(-centro)

    tubo2.moveBy([10,0,0])
    tubo2.rotateDeg(angle,0,0)
    
    mix.add(tubo1)
    mix.add(tubo2)
    
    lmps = LammpsData().loadWolffiaMixture(mix)
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
gennedfiles = pool.starmap(writeObj, zip([og_folder]*len(range(0,92,2)),range(0,92,2)))
pool.close()
pool.join()
print(gennedfiles)


    
for temp in range(start_temp, max_temp, temp_step):
    pre = script[22][:20]
    suf = script[22][37:]
    mod_temp = f'{pre}{temp:.1f} {temp:.1f} 100.0{suf}'
    tdirectory = f"{parent_folder}/tubes{temp}k"
    if not os.path.exists(tdirectory):
        os.makedirs(tdirectory)

    open(f"{tdirectory}/lammps.in","w").writelines(script[:22]+[mod_temp]+script[23:])
    shutil.copytree(og_folder, tdirectory,dirs_exist_ok=True)
