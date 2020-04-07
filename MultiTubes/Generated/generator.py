import granules.structure.LAMMPSdata as ld
import numpy as np


# para leer cyclos y coordenadas
base = ld.LammpsData("../../nanotube.data")

generated_cnt_pairs = []

for i in range(2): #90
    '''
    Calcular el angulo y de ahi la matriz de rotación
    '''
    angle = np.pi*i/180
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
    cnt.writeConf(f'rot{i:02}.data')



"""




offset = cnt.atomproperty.atoms[['x','y','z']].mean()
cnt.atomproperty.atoms[['x','y','z']] = cnt.atomproperty.atoms[['x','y','z']] - offset
base.atomproperty.atoms.copy()['y']+5
for i,row in cnt.atomproperty.atoms[['x','y','z']].iterrows():
    cnt.atomproperty.atoms.loc[i,['x','y','z']] = row.values.T.dot(np.array([[0,0,1],[0,1,0],[-1,0,0]]))
    
cnt.atomproperty.atoms[['x','y','z']] = cnt.atomproperty.atoms[['x','y','z']] + offset
cnt.writeConf('rottube.data')
"""