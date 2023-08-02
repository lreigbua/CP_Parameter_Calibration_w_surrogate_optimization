%close all

function f=run_CP_model(param)
%create tess
% status = system('python create_columnar_periodic_tess.py 85 4 4 4')

%modify material
struct_params.h0 = 200.e+6*param(1);
struct_params.xi_0_sl = [340.e+6, 445.e+6, 0.0, 544.e+6]*param(2);
struct_params.xi_inf_sl = [568.e+6, 150.e+7, 0.0, 3420.e+6]*param(3);

txt = jsonencode(struct_params,PrettyPrint=true);
fprintf(fopen('data_json.json','wt'),txt);

status = system('python modify_material.py')
status = system('python create_materialYaml.py 85 4 4 4')

%RUN MODEL
status = system('wsl export OMP_NUM_THREADS=16 ; DAMASK_grid --load loadZ.yaml --geom Neper_columnar_85_grains.vti');


%EXTRACT STRES STRAIN DATA PYTHON
status = system('python plot_stress_strain.py 85 4 4 4')

%PLOT STRESS STRAIN
data = readmatrix("stress-strain_85_grains_4_cells.txt");

%Removes first row to remove 0 strain data, which gives error in division
data(1,:)=[];

%Interpolate to match experimental strains
pointstointerp = linspace(0.001,0.025,25);
Vq=interp1(data(:,1),data(:,2),pointstointerp,'spline');

f=Vq.'/1e6; %traspose and change to MPa
end