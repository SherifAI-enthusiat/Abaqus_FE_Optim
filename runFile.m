% Global count
clear,clc;
pyrunfile("initialiseJob.py");
x0 =[20,10,50,0.3,0.2,0.2,4.7115,1.4583,1.4583]; % [20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583]
lb =[.01,.01,1,.01,.01,.01,1,1,1];
ub =[20,20,250,.5,.5,.5,20,30,30];
% % % Custom points ---> Latin Hypercube sampling
ptmatrix= myhypercsample(50,"trans"); % Number of samples is more releveant here.
tpoints = CustomStartPointSet(ptmatrix);
% x0 =[210,.3];  % the ans is 250,.3 I believe.
% lb =[100,.15]; ub = [300,.5];
% v1 = 100:10:300;
% v2 = .15:.05:.5;
% [X,Y] = meshgrid(v1,v2);
% ptmatrix = [X(:),Y(:)];
% tpoints = CustomStartPointSet(ptmatrix);
% Previous Uncomment to use lsqnonlin and fmincon
options = optimoptions(@lsqnonlin,'Algorithm','trust-region-reflective'); % optimoptions(@fmincon,'Algorithm','interior-point');
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
% pool = parpool(3); % Trying to address error "IdleTimeout has been reached."
[Xnew,fval,exitflag,output,solutions]= run(ms,problem,tpoints);
