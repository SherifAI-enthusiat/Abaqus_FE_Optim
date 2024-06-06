% Global count
clear,clc;
pyrunfile("initialiseJob.py");
Obj = myFunctions();
Obj.path = "D:\Sherif_CT_Download\github\Abaqus_FE_Optim\MatlabOutput";
x0 =[20,50,1.4583]; % Here I am only interested in Ep,Ef and Gpf [20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583]
lb =[.01,1,1]; % This is the lower bound 
ub =[20,250,30]; % This is the lower bound 
% %% Optimisation using particle swarm from scratch
options = optimoptions('particleswarm','SwarmSize',7,'HybridFcn', @fmincon,'InertiaRange',[1.5,0.5]);
options.UseParallel = true;
myObj = @(x)Obj.myscript(x);
[Xnew, fval, exitflag, output] = particleswarm(myObj,3,lb, ub, options);
save("last_run.mat")