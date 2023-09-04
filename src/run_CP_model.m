%close all

function f=run_CP_model(param,initial_CP_data_struct,config_struct)

for i=1:1:length(initial_CP_data_struct)

%modify material
struct_params.h0 = initial_CP_data_struct(i).h0*param(1);
struct_params.xi_0_sl = initial_CP_data_struct(i).xi_0_sl*param(2);
struct_params.xi_inf_sl = initial_CP_data_struct(i).xi_inf_sl*param(3);
struct_params.a_sl = initial_CP_data_struct(i).a_sl*param(4);
% struct_params.n_sl = initial_CP_data_struct(i).n_sl*param(5);

writematrix(param,"current_sol.txt")

txt = jsonencode(struct_params,PrettyPrint=true);
fprintf(fopen('./data_json.json','wt'),txt);

status = system(sprintf('. ../src/conda_initialise-3.9.sh && python ../src/modify_material.py %s',config_struct.phases{i}))
end

%create material.yaml
status = system('. ../src/conda_initialise-3.9.sh && python ../src/create_materialYaml.py 85 32 32 32')

%RUN MODEL
% status = system('wsl export OMP_NUM_THREADS=16 ; DAMASK_grid --load ../input/loadZ.yaml --geom ../input/Neper_columnar_85_grains.vti');

str1 = 'DAMASK_grid --load ../input/loadZ.yaml --geom ../input/Neper_columnar_85_grains.vti';
Run_Damask_Command_Archie(str1)



%EXTRACT STRES STRAIN DATA PYTHON
status = system('. ../src/conda_initialise-3.9.sh && python ../src/plot_stress_strain.py 85 32 32 32')

%PLOT STRESS STRAIN
data = readmatrix("./stress-strain_85_grains_32_cells.txt");

%Removes first row to remove 0 strain data, which gives error in division
data(1,:)=[];

%Interpolate to match experimental strains
pointstointerp = linspace(0.001,0.015,15);
Vq=interp1(data(:,1),data(:,2),pointstointerp,'spline');

f=Vq.'/1e6; %traspose and change to MPa
end