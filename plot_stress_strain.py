import damask
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

if __name__ ==  '__main__':
    n_grains=int(sys.argv[1])
    
    cells_x=int(sys.argv[2])
    cells_y=int(sys.argv[3])
    cells_z=int(sys.argv[4])


    res = damask.Result(f'Neper_columnar_{n_grains}_grains_loadZ.hdf5')
    res.add_stress_Cauchy()
    res.add_equivalent_Mises('sigma')
    res.add_strain()
    res.add_equivalent_Mises('epsilon_V^0.0(F)')


    # res.export_VTK()


    sigma = [np.average(s['homogenization']) for s in res.get('sigma_vM').values()]
    epsilon = [np.average(e['homogenization']) for e in res.get('epsilon_V^0.0(F)_vM').values()]
    stress_strain=np.array([epsilon,sigma])
    np.savetxt(f'stress-strain_{n_grains}_grains_{cells_x}_cells.txt',np.transpose(stress_strain))
    plt.plot(epsilon,sigma)
    plt.savefig(f'stress-strain_{n_grains}_grains_{cells_x}_cells.png')

