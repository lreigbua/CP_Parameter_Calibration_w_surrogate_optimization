import damask
import numpy as np
import os
import sys
import random


n_PBGs=int(sys.argv[1])
cells_per_side=int(sys.argv[6])

Phase_fraction_alpha=float(sys.argv[2])
Phase_fraction_mart=float(sys.argv[3])
Phase_fraction_beta=float(sys.argv[4])

lath_thickness = float(sys.argv[5])

# calculate hall-petch effect:
#tau0 = tauinf + k / sqrt(l_t)
#tauinf = given by material file

#k to be specified (MPa*sqrt(um))
k_alpha = 90.0e6
k_beta = 120.0e6
#k_mart = 180
l_th_beta = lath_thickness * Phase_fraction_beta



#lath_thickness_alpha = lath_thickness
#lath_thickness_mart = 0.22 um from he-xrd paper, usually constant
#lath_thickness_beta = #lath_thickness_alpha * 0.15



# load vti files:
grid_columnar = damask.Grid.load(f'../input/columnar_n{n_PBGs}-{cells_per_side}-cells-per-side')
grid_cube = damask.Grid.load(f'../input/cubes_n{n_PBGs}-{cells_per_side}-cells-per-side')

# 2. Create a list of dicts of orientation info for each columnar grain
# the txt files used can be genearted using create_orientations.m, which uses mtex of beta grains and its 
# corresponding alpha grains using the BOR.
orientation_dict_list = np.array([{}]*n_PBGs)
oris_alpha = np.loadtxt('../input/oris_alpha.txt', skiprows=1)
oris_beta = np.loadtxt('../input/oris_beta.txt', skiprows=1)

for i in range(n_PBGs):
    orientation_dict_list[i] = {"beta_ori": oris_beta[i,:], "alpha_oris": oris_alpha[12*i:12*i+12,:]}

# create probability distribution for each phase and alpha orientation
Phases = ['Alpha', 'Martensite', 'Beta']
Prob_each_phase = [Phase_fraction_alpha, Phase_fraction_mart, Phase_fraction_beta]
Prob_each_alpha_ori = [1/12]*12

phases = [''] * (cells_per_side**3)
oris = np.zeros((cells_per_side**3, 3))
n = 0

# loop through the columnar grid and save materials in the order of the cubic grid grid_cube.material
final_material_dict_list = np.array([{}]*(cells_per_side**3))
for i in range(len(grid_columnar.material)):
    for j in range(len(grid_columnar.material[i])):
        for k in range(len(grid_columnar.material[i][j])):
            
            PBG_id = grid_columnar.material[i][j][k]
            cube_id = grid_cube.material[i][j][k]

            phase = random.choices(Phases, Prob_each_phase)[0]   
            if phase == 'Beta':
                ori = orientation_dict_list[PBG_id]["beta_ori"]
            else:
                ori = random.choices(orientation_dict_list[PBG_id]["alpha_oris"], Prob_each_alpha_ori)[0]
                   
            phases[cube_id] = phase
            oris[cube_id] = ori
            
            n += 1

oris = damask.Rotation.from_Euler_angles(oris, degrees=True)

# Create Material.yaml
config_material = damask.ConfigMaterial()

config_material['homogenization']['Dummy'] = {'N_constituents': 1,'mechanical':{'type': 'pass'}}
config_material['phase']['Alpha'] = damask.ConfigMaterial.load('./material_phase_phenopower_alpha_mod.yaml')
config_material['phase']['Alpha']['mechanical']['plastic']['xi_0_sl'] += k_alpha/np.sqrt(lath_thickness)
config_material['phase']['Beta'] = damask.ConfigMaterial.load('./material_phase_phenopower_beta_mod.yaml')
config_material['phase']['Beta']['mechanical']['plastic']['xi_0_sl'] += k_beta/np.sqrt(l_th_beta)
config_material['phase']['Martensite'] = damask.ConfigMaterial.load('./material_phase_phenopower_martensite_mod.yaml')
# config_material['phase']['Martensite'][xi_0_sl] += k_alpha/np.sqrt(lath_thickness)

config_material = config_material.material_add(phase = phases,
                    O=oris,
                    homogenization = 'Dummy')

config_material.save('material.yaml')


#You can use the following code to generate a vti file with the IPF colors and phase names in each cell 
# to be viewed in paraview, but it is not necessary to run the simulation:
##Add IPF colors:

# geom = f'../input/cubes_n{n_PBGs}-{cells_per_side}-cells-per-side.vti'      # path for geometry file
# material_config = 'material.yaml'    # path for material.yaml

# v = damask.VTK.load(geom)
# material_ID = v.get(label='material').flatten()

# ma = damask.ConfigMaterial.load(material_config)

# phases = list(ma['phase'].keys())
# info = []

# for m in ma['material']:
#     c = m['constituents'][0]
#     phase = c['phase']
#     info.append({'phase':   phase,
#                  'phaseID': phases.index(phase),
#                  'lattice': ma['phase'][phase]['lattice'],
#                  'O':       c['O'],
#                 })
    
# l = np.array([0,0,1])                            # lab frame direction for IPF

# IPF = np.ones((len(material_ID),3),np.uint8)
# for i,data in enumerate(info):
#     IPF[np.where(material_ID==i)] = \
#     np.uint8(damask.Orientation(data['O'],lattice=data['lattice']).IPF_color(l)*255)
    
# v = v.set(f'IPF_{l}',IPF)

# p   = np.array([d['phase'] for d in info])
# pid = np.array([d['phaseID'] for d in info])
# v = v.set(label='phase',data=p[material_ID],info='phase name')
# v = v.set(label='phaseID',data=pid[material_ID],info='phase ID')

# v.save(f'n{n_PBGs}_{cells_per_side}_cells_per_side_cubic_microstructure_initial_IPF+phase')