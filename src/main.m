clc
clear

% Change to data directory
tmp = matlab.desktop.editor.getActive;
cd(fileparts(tmp.Filename));
cd ../data/

addpath('../input')
addpath('../src')

%create tess
%status = system('python create_columnar_periodic_tess.py 85 4 4 4')


%Read config.json
config_struct = jsondecode(fileread("../input/config.json"));

%save initial CP parameters as JSON fiiles
for i=1:1:length(config_struct.phases)
    status = system(sprintf("python ../src/save_initial_CPs_as_JSON.py %s",config_struct.phases{i}));
end
   
for i=1:1:length(config_struct.phases)
    initial_CP_data_struct(i)=jsondecode(fileread(sprintf("./initial_%s_json_data.json",config_struct.phases{i})));
end


%%
%read experimental data
data_exp=readmatrix('../input/exp_data_dual_2p5.txt');


%specify upper and lower bounds
ub=[2.0 1.5 1.5];
lb=[0.5 0.5 0.25];

%Run surrogate optimization
objFun = @(cp_params) stress_dif([run_CP_model(cp_params,initial_CP_data_struct,config_struct) data_exp(:,2)]);

options = optimoptions('surrogateopt','PlotFcn','surrogateoptplot');

[sol,fval,exitflag,output,trials] = surrogateopt(objFun,lb,ub,options);

%%
figure()
axes();
plot(data_exp(:,1),data_exp(:,2), 'b+');
hold on
plot(data_exp(:,1), run_CP_model(sol), 'r-');
% plot(data_exp(:,1), Vq/1e6, 'r-');
legend({'Data points', 'Fitted Curve'})
sol