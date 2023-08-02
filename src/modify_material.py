import damask
import numpy as np
import json


# Create Material.yaml
config_material = damask.ConfigMaterial()

config_material = damask.ConfigMaterial.load('../input/material_phase_phenopower_alpha.yaml')

f = open('data_json.json')
data = json.load(f)
print(data)

config_material['mechanical']['plastic']['h_0_sl-sl']=data['h0']
config_material['mechanical']['plastic']['xi_0_sl']= data['xi_0_sl']
config_material['mechanical']['plastic']['xi_inf_sl'] = data['xi_inf_sl']

config_material.save('material_phase_phenopower_alpha_mod.yaml')
