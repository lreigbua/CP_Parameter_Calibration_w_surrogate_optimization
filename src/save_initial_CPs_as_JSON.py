import damask
import numpy as np
import json
import sys


material_name = sys.argv[1]

config_material = damask.ConfigMaterial()

config_material = damask.ConfigMaterial.load(f'../input/material_phase_phenopower_{material_name}.yaml')

dict_for_json = {}

dict_for_json['h0'] = config_material['mechanical']['plastic']['h_0_sl-sl']
dict_for_json['xi_0_sl'] = config_material['mechanical']['plastic']['xi_0_sl']
dict_for_json['xi_inf_sl'] = config_material['mechanical']['plastic']['xi_0_sl']


with open(f'../data/initial_{material_name}_json_data.json', "w") as fp:
    json.dump(dict_for_json,fp) 
