import damask
import numpy as np
from matplotlib import pyplot as plt
import sys

n_grains = sys.argv[2]
cells_per_side = sys.argv[3]

class calc_stress_strain:
    def __init__(self, load_direction):
        self.load_direction = load_direction
        self.res = damask.Result(f'cubes_n{n_grains}-{cells_per_side}-cells-per-side_load{self.load_direction}.hdf5')

    def run(self):

        self.res.add_stress_Cauchy()
        self.res.add_strain()
        self.res.add_equivalent_Mises('sigma')
        self.res.add_equivalent_Mises('epsilon_V^0.0(F)')

        # res.export_VTK()

        if self.load_direction in ['X','Y','Z']:
            out_dirs = ['X', 'Y', 'Z']
        else:
            out_dirs = ['XY', 'XZ', 'YZ']
                    
        for dir in out_dirs:
            self.write_stress_strain(out_dir = dir)

    
    def write_stress_strain(self, out_dir):

        sigma = self.calculate_average_value('sigma', out_dir)
        epsilon = self.calculate_average_value('epsilon_V^0.0(F)', out_dir)
        stress_strain = np.array([epsilon, sigma])
        np.savetxt(f'stress-strain-{out_dir}.txt', np.transpose(stress_strain))
        plt.plot(epsilon, sigma)
        plt.savefig(f'stress-strain-{out_dir}.png')

    def calculate_average_value(self, var, out_dir):
        
        value = [0,0] if out_dir == 'X' else \
                [1,1] if out_dir == 'Y' else \
                [2,2] if out_dir == 'Z' else \
                [0,1] if out_dir == 'XY' else \
                [0,2] if out_dir == 'XZ' else \
                [1,2] if out_dir == 'YZ' else None

        
        res_dict = self.res.get(var)

        if isinstance(res_dict['increment_0'], np.ndarray): #if there is only one phase:
            s = [np.average(val[:,value[0],value[1]]) for val in res_dict.values()]
        else:
            s = []
            for s_per_inc in res_dict.values():
                s_this_inc = np.array([])
                for s_per_phase in s_per_inc.values():
                    s_this_inc = np.append(s_this_inc, s_per_phase[:,value[0],value[1]])
                s.append(np.average(s_this_inc))
        return s



if __name__ ==  '__main__':

    load_direction = sys.argv[1]
    instance = calc_stress_strain(load_direction)
    instance.run()
