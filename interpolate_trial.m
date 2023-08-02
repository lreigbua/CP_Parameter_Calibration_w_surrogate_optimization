pointstointerp = linspace(0.001,0.025,25);

Vq=interp1(data(:,1),data(:,2),pointstointerp,'spline')

figure()
plot(pointstointerp,Vq,'*')
hold on
plot(data(:,1),data(:,2),'*')