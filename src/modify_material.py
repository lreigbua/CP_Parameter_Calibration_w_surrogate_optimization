import damask
import numpy as np
import json
import sys


phase_name=sys.argv[1]

# Create Material.yaml
config_material = damask.ConfigMaterial()

config_material = damask.ConfigMaterial.load(f'../input/material_phase_phenopower_{phase_name}.yaml')

f = open('data_json.json')
data = json.load(f)
print(data)

config_material['mechanical']['plastic']['h_0_sl-sl']=data['h0']
config_material['mechanical']['plastic']['xi_0_sl']= data['xi_0_sl']
config_material['mechanical']['plastic']['xi_inf_sl'] = data['xi_inf_sl']

config_material.save(f'material_phase_phenopower_{phase_name}_mod.yaml')
