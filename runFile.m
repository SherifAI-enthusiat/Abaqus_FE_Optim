% Global count
clear,clc;
pyrunfile("initialiseJob.py");
% % % Custom points ---> Latin Hypercube sampling
% ptmatrix= myhypercsample(50,"ortho"); % Number of samples is more relevant here.
% tpoints = CustomStartPointSet(ptmatrix);
x0 =[150,.1];  % the ans is 200,.3.
lb =[100,.15]; ub = [300,.5];
v1 = 100:10:300;
v2 = .15:.05:.5;
[X,Y] = meshgrid(v1,v2);
ptmatrix = [X(:),Y(:)];
tpoints = CustomStartPointSet(ptmatrix);
% Previous Uncomment to use lsqnonlin and fmincon
algo ='levenberg-marquardt'; % 'trust-region-reflective';
options = optimoptions(@lsqnonlin,'Algorithm',algo); 
% optimoptions(@fmincon,'Algorithm','interior-point');
options.PlotFcns = 'optimplotresnorm'; %  'optimplotfirstorderopt'
options.UseParallel = false;
%% Problem definition
problem = createOptimProblem('fmincon','x0',x0,'objective',@myscript,...
    'lb',lb,'ub',ub,'options',options); % 'lsqnonlin'
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
pool = parpool(4); % Trying to address error "IdleTimeout has been reached."
[Xnew,fval,exitflag,output,solutions]= run(ms,problem,tpoints);
