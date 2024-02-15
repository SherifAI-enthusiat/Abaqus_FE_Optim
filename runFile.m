% Global count
clear,clc;
pyrunfile("initialiseJob.py");
x0 =[20,50,1.4583]; % Here I am only interested in Ep,Ef and Gpf [20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583]
lb =[.01,1,1]; % This is the lower bound 
ub =[20,250,30]; % This is the lower bound 
% %% Optimisation using particle swarm from scratch
options = optimoptions('particleswarm','SwarmSize',7,'HybridFcn', @fmincon,'InertiaRange',[.5,1.5]);
options.UseParallel = true;
[Xnew, fval, exitflag, output] = particleswarm(@myscript,3,lb, ub, options);
save("last_run.mat")