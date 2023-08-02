clc
clear

% Change to data directory
tmp = matlab.desktop.editor.getActive;
cd(fileparts(tmp.Filename));
cd ../data/

addpath('../input')
addpath('../src')


%%
%read experimental data
data_exp=readmatrix('../input/exp_data_dual_2p5.txt');

%specify upper and lower bounds
ub=[2.0 1.5 1.5];
lb=[0.5 0.5 0.25];

%
objFun = @(cp_params) stress_dif([run_CP_model(cp_params) data_exp(:,2)]);

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