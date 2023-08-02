clc
clear

%experimental values
% n=55;
% adot=0.001;
% ho=675;
% ts=175;
% to=90;
ub=[2.0 1.5 1.5];
lb=[0.5 0.5 0.25];

data_exp=readmatrix('exp_data_dual_2p5.txt');

objFun = @(cp_params) stress_dif([run_CP_model(cp_params) data_exp(:,2)]);
%sol = ga(objFun, 3,A,b,Aeq,beq,lb,ub,nonlcon,options);

%options = optimoptions('surrogateopt','ObjectiveLimit',0.01,'PlotFcn','surrogateoptplot');
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