% Global count
clear,clc;
pyrunfile("initialiseJob.py");
x0 =[20,50,1.4583]; % Here I am only interested in Ep,Ef and Gpf [20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583]
lb =[.01,1,1]; % This is the lower bound 
ub =[20,250,30]; % This is the lower bound 
% % % Custom points ---> Latin Hypercube sampling
ptmatrix= myhypercsample(50,"trans"); % This can be only be "trans" in the "three_param" branch.
datn = ptmatrix(:,[1,3,end]); % This is just Ep,Ef,and Gpf. Other params will be fixed or calculated
tpoints = CustomStartPointSet(datn);
% Previous Uncomment to use lsqnonlin and fmincon
options = optimoptions(@lsqnonlin,'Algorithm','levenberg-marquardt'); % optimoptions(@fmincon,'Algorithm','interior-point');
options.PlotFcns = 'optimplotresnorm'; %  'optimplotfirstorderopt'
options.UseParallel = false;
%% Problem definition
problem = createOptimProblem('lsqnonlin','x0',x0,'objective',@myscript,...
    'lb',lb,'ub',ub,'options',options);
% [x,ref] = lsqnonlin(problem);
% [Xnew,ref] = lsqnonlin(@myscript,x0,lb,ub,options);
%% Multi-Start algorithm-uses Parallel 
% ms = MultiStart('PlotFcns',@gsplotbestf); % Multi-Start
ms = MultiStart;
ms.UseParallel = true;
te = gcp('nocreate');
if exist("te","var")==1
    delete(gcp)
end
pool = parpool(3);
[Xnew,fval,exitflag,output,solutions]= run(ms,problem,tpoints);
save("last_run.mat")