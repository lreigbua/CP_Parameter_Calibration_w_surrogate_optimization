import os
import sys
import damask
import numpy as np
import random

# This file just generates the vtis needed. We need one columnar tessellation and one cubic tessellation. the orientations and phases of the
# different grains are decided in material.yaml, but in order to generate material.yaml correctly it will use this files. However, generating 
# the vtis is a time consuming process, so we do it here and then we can use the vtis to generate the material.yaml file as a function of our 
# microstructural parameters (phase fractions and lath thicknesses).

n_PBGs=85 # number of parent beta grains in our microstructure
cells_per_side=16 # number of cells/grains per side in our microstructure

# Generate Columnar Voronoi in Neper:
os.system(f'module load neper/gcc-8.5.0/4.5.0 && export OMP_NUM_THREADS=1 && neper -T -n {n_PBGs} -morpho "columnar(z)"  -periodicity "x,y" -tesrsize {cells_per_side} -format tess,vtk -o columnar_n{n_PBGs}-{cells_per_side}-cells-per-side')
grid_columnar = damask.Grid.load_Neper(f'columnar_n{n_PBGs}-{cells_per_side}-cells-per-side.vtk').renumber() #damask passes vtk to vti
grid_columnar.save(f'columnar_n{n_PBGs}-{cells_per_side}-cells-per-side') #save it to disk

# Generate Cubic Voronoi in Neper:
os.system(f'module load neper/gcc-8.5.0 && export OMP_NUM_THREADS=1 && neper -T -n from_morpho -morpho "cube({cells_per_side})" -tesrsize {cells_per_side} -periodicity all -format vtk')
grid_cube = damask.Grid.load_Neper(f'nfrom_morpho-id1.vtk').renumber()
grid_cube.save(f'cubes_n{n_PBGs}-{cells_per_side}-cells-per-side')