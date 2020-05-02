#!/usr/bin/python3

import pandas as pd

def read_dump(filename):
    text = open(filename).read().split('ITEM: TIMESTEP')

    frames = []
    for chunk in text[1:]:
        data = pd.DataFrame([line.split() for line in chunk.splitlines()[9:]])
        data.columns = ['id', 'type', 'xs', 'ys', 'zs']
        data = data.astype({'id':int, 'type':int, 'xs':float, 'ys':float, 'zs':float})
        data = data.sort_values('id').reset_index(drop=True)
        #print(data)
        frames.append(data)

    #para ver si cambiaron
    for i in range(len(frames)-1):
        if frames[i].equals(frames[i+1]):
            #print('did not move')
            pass
        else:
            print('moved')




def read_log(filename):
    text = open(filename).read().splitlines()[68:-30]
    
    rowholder = []
    for i in range(0, len(text), 5):
        #print(text[i][25:31])
        t1 = text[i].split()[2]+' '
        t2 = text[i+1].split()[2] +' '+text[i+1].split()[5]+' '+text[i+1].split()[8]+' '
        t3 = text[i+2].split()[2] +' '+text[i+1].split()[5]+' '+text[i+1].split()[8]+' '
        t4 = text[i+3].split()[2] +' '+text[i+1].split()[5]+' '+text[i+1].split()[8]+' '
        t5 = text[i+4].split()[2] +' '+text[i+1].split()[5]+' '+text[i+1].split()[8]
        row = t1+t2+t3+t4+t5
        rowholder.append(row)
    data = pd.DataFrame([x.split() for x in rowholder])
    data.columns = ['Timestep','TotEng','KinEng','Temp','PotEng','E_bond','E_angle','E_dihed','E_impro','E_vdwl' ,'E_coul','E_long','Press']
    print(data)





read_dump('generated/tubes350k/tube00deg/tube.dump')
read_log('generated/tubes350k/tube00deg/log.lammps')


