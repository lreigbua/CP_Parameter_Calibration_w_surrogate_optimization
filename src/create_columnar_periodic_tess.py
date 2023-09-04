import os
import sys
import damask

n_grains=int(sys.argv[1])

cells_x=int(sys.argv[2])
cells_y=int(sys.argv[3])
cells_z=int(sys.argv[4])

# Generate Voronoi:

os.system(f'module load neper/gcc-8.5.0/4.5.0 && neper -T -n {n_grains} -morpho "columnar(z)"  -periodicity "x,y" -tesrsize {cells_x}:{cells_y}:{cells_z} -format tess,vtk')
os.system(f'module load neper/gcc-8.5.0/4.5.0 && neper -V n{n_grains}-id1.tess -print img1')

grid = damask.Grid.load_Neper(f'n{n_grains}-id1.vtk') #passes vtk to vti
grid.save(f'Neper_columnar_{n_grains}_grains')