%stress diference
function f=stress_dif(stress)

    sigma_cpfe=stress(:,1);
    sigma_exp=stress(:,2);
    
    summ=0;
    for i=1:1:length(sigma_cpfe)
        summ=summ+(1-sigma_cpfe(i)/sigma_exp(i))^2;    
    end
    
    f=sqrt(1/length(sigma_cpfe)*summ);

end
