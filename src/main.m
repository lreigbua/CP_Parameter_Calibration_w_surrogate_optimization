clc
clear
fclose('all');


% Change to data directory
tmp = matlab.desktop.editor.getActive;
cd(fileparts(tmp.Filename));
cd ../data/

addpath('../input')
addpath('../src')

%create tess
%status = system('. ../src/conda_initialise-3.9.sh && python ../src/create_columnar_periodic_tess.py 85 32 32 32')

%Read config.json
config_struct = jsondecode(fileread("../input/config.json"));

%save initial CP parameters as JSON fiiles
for i=1:1:length(config_struct.phases)
    status = system(sprintf(". ../src/conda_initialise-3.9.sh && python ../src/save_initial_CPs_as_JSON.py %s",config_struct.phases{i}));
end
   
for i=1:1:length(config_struct.phases)
    initial_CP_data_struct(i)=jsondecode(fileread(sprintf("./initial_%s_json_data.json",config_struct.phases{i})));
end



%read experimental data
data_exp=readmatrix('../input/exp_data_mart_2p5.txt');
%%

%specify upper and lower bounds
ub=[10 1.1 1.1 1.1 1.1];
lb=[0.05 0.9 0.9 0.9 0.9];

%Run surrogate optimization
objFun = @(cp_params) stress_dif([run_CP_model(cp_params,initial_CP_data_struct,config_struct) data_exp(:,2)]);

options = optimoptions('surrogateopt','PlotFcn','surrogateoptplot','MaxFunctionEvaluations',600,'MinSurrogatePoints',40);

[sol,fval,exitflag,output,trials] = surrogateopt(objFun,lb,ub,options);
writematrix(sol,'optimized_CP')


%% plots fitted curve:
fit = run_CP_model(sol,initial_CP_data_struct,config_struct);
figure()
axes();
plot(data_exp(:,1),data_exp(:,2), 'b--O','LineWidth',2);
hold on
plot(data_exp(:,1), fit, 'r-','LineWidth',2);
% plot(data_exp(:,1), Vq/1e6, 'r-');
legend({'Data points', 'Fitted Curve'})
ylim([0 1400])
xlim([0 3])



writematrix(fit,'optimized_curve')