import granules.structure.LAMMPSdata as ld
import numpy as np


# para leer cyclos y coordenadas
cnt = ld.LammpsData("cgtube.data")
offset = cnt.atomproperty.atoms[['x','y','z']].mean()
cnt.atomproperty.atoms[['x','y','z']] = cnt.atomproperty.atoms[['x','y','z']] - offset

for i,row in cnt.atomproperty.atoms[['x','y','z']].iterrows():
    cnt.atomproperty.atoms.loc[i,['x','y','z']] = row.values.T.dot(np.array([[0,0,1],[0,1,0],[-1,0,0]]))
    
cnt.atomproperty.atoms[['x','y','z']] = cnt.atomproperty.atoms[['x','y','z']] + offset
#cnt.writeConf('rotcgtube.data')
