import damask
import numpy as np
import os
import sys

n_grains=int(sys.argv[1])

cells_x=int(sys.argv[2])
cells_y=int(sys.argv[3])
cells_z=int(sys.argv[4])

Phase_fraction_alpha=0.91
Phase_fraction_mart=0.0
Phase_fraction_beta=0.09



# Create Material.yaml
config_material = damask.ConfigMaterial()
N_constituents_taylor=25

config_material['homogenization']['Taylor'] = {'N_constituents':N_constituents_taylor,'mechanical':{'type':'isostrain','output': ['F','P'] }}
config_material['phase']['Alpha'] = damask.ConfigMaterial.load('material_phase_phenopower_alpha_mod.yaml')
config_material['phase']['Martensite'] = damask.ConfigMaterial.load('material_phase_phenopower_martensite_mod.yaml')
config_material['phase']['Beta'] = damask.ConfigMaterial.load('material_phase_phenopower_beta_mod.yaml')


oris_all=np.loadtxt('../input/oris_all.txt')

final_O=[]
for m in range(0,n_grains):
    oris_this_grain=damask.Rotation.from_Euler_angles(oris_all[m*25:(m*25+25),:],degrees=True)
    final_O.append(oris_this_grain)
    

#calculate volume fractions:
v_column=np.ones(N_constituents_taylor)

v_column[0]=Phase_fraction_beta
v_column[1:13]=Phase_fraction_mart/12
v_column[13:25]=Phase_fraction_alpha/12


#Create file
config_material = config_material.material_add(phase = np.array(['Beta','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Martensite','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha','Alpha']).reshape(1,N_constituents_taylor),
                   O=final_O,
                   v = v_column.reshape(1,N_constituents_taylor),
                   homogenization = 'Taylor')



config_material.save()