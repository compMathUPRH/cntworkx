# nanotube.data
#abrir
# finaltube.data
import os
import numpy as np
import granules.structure.LAMMPSdata as ld

lammps_script_file = "lammps.in"
base_nanotube_file = "nanotube.data"
nanotube_line_file = "finaltube.data"


script = open(lammps_script_file).readlines()
base_cnt = ld.LammpsData(base_nanotube_file)
base_lines = ld.LammpsData(nanotube_line_file)


start_temp = 275
max_temp = 420
temp_step = 10

#fix nvt
def writelobj(base,rot,direc):
    angle = np.pi*rot/180
    rotmat = np.array([[np.cos(angle),0,np.sin(angle)],[0,1,0],[-np.sin(angle),0,np.cos(angle)]])
    cnt = ld.LammpsData()
    cnt.atomproperty.atoms = base.atomproperty.atoms.copy()
    cnt.atomproperty.atoms['y'] += 10
    cnt.atomproperty.atoms['aID'] += cnt.atomproperty.atoms.shape[0]
    
    offset = cnt.atomproperty.atoms[['x','y','z']].mean()
    cnt.atomproperty.atoms[['x','y','z']] = (cnt.atomproperty.atoms[['x','y','z']] - offset).dot(rotmat).rename(columns={0:'x',1:'y',2:'z'}) + offset
    cnt.atomproperty.atoms = base.atomproperty.atoms.append(cnt.atomproperty.atoms.copy())
    
    cnt.topologia.bonds = base.topologia.bonds.copy()
    cnt.topologia.bonds[['Atom1','Atom2']] += cnt.atomproperty.atoms.shape[0]/2
    cnt.topologia.bonds = base.topologia.bonds.append(cnt.topologia.bonds.copy()).astype('int32')
    
    cnt.atomproperty.masses = base.atomproperty.masses.copy()
    cnt.writeConf(f'{direc}/rot{rot:02}.data')


parent_folder="generated"

for temp in range(start_temp,max_temp,temp_step):
    pre = script[22][:20]
    suf = script[22][37:]
    mod_script =f'{pre}{temp:.1f} {temp:.1f} 100.0{suf}'
    
    tdirectory = f"{parent_folder}/tubes{temp}k"
    if not os.path.exists(tdirectory):
        os.makedirs(tdirectory)    
    
    ldirectory = f"{parent_folder}/lines{temp}k"
    if not os.path.exists(ldirectory):
        os.makedirs(ldirectory)
    
    for rot in range(46):#0-45
        writelobj(base_cnt,rot,tdirectory)
        writelobj(base_lines,rot,ldirectory)
        
        
        
        
        
