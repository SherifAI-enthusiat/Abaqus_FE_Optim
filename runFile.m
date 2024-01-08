%% Global count
clear,clc;
pyrunfile("initialiseJob.py");
% % % Custom points ---> Latin Hypercube sampling
% ptmatrix= myhypercsample(50,"ortho"); % Number of samples is more relevant here.
% tpoints = CustomStartPointSet(ptmatrix);
x0 =[150,.2];  % the ans is 200,.3.
lb =[100,.15]; ub = [300,.5];
v1 = 100:15:300;
v2 = .15:.05:.5;
[X,Y] = meshgrid(v1,v2);
ptmatrix = [X(:),Y(:)];
tpoints = CustomStartPointSet(ptmatrix);
% Previous Uncomment to use lsqnonlin and fmincon
algo ='trust-region-reflective'; %'interior-point';
options = optimoptions(@lsqnonlin,'Algorithm',algo);
% options.FiniteDifferenceStepSize = [.5,0.01];
% options.UseParallel = true;
%% Problem definition
problem = createOptimProblem('lsqnonlin','x0',x0,'objective',@myscript,...
    'lb',lb,'ub',ub,'options',options); % 'lsqnonlin'
% [x,ref] = lsqnonlin(problem);
% [Xnew,ref] = lsqnonlin(@myscript,x0,lb,ub,options);
%% Multi-Start algorithm-uses Parallel 
ms = MultiStart; % ms = GlobalSearch;
ms.UseParallel = true; 
ms.Display = "iter"; 
te = gcp('nocreate');
if exist("te","var")==1
    delete(gcp)
end
pool = parpool(4); % Trying to address error "IdleTimeout has been reached."
[Xnew,fval,exitflag,output,solutions]= run(ms,problem,tpoints);

%% 2nd optimisation 
% new = zeros(size(solutions,2),10);
[a,b] = size(solutions);
int = round(b/5); new = zeros(5,4);
lst = [1,5,int,2*int,3*int];
pool = gcp;
options = optimoptions('particleswarm','SwarmSize', 5,'HybridFcn', @fmincon);
options.UseParallel = true;
% Modification to optimiser
% algo ='interior-point';
% options.UseParallel = true;
% options.FiniteDifferenceStepSize =[1,.05];
% options = optimoptions(@fmincon,'Algorithm',algo);
% addAttachedFiles(pool, {'myscript.m','errorfunc.m','lstestv2_parallel_v1.py','TestJob-2.inp','write2InpFile.py','HelperFunc.py','dataRetrieval.py'})
for i=1:5
    ind = lst(i); 
    newX = solutions(1,ind).X;
    [ub,lb]=genNewBounds(newX,[10,.02]); % i generate new bounds based on the soln location.
    [Xnew, fval, exitflag, output] = particleswarm(@myscript,2,lb, ub, options);
    new(i,:) = [Xnew,residual];
end

save("last_run.mat")

%% Optimisation using particle swarm from scratch
clear,clc;
pyrunfile("initialiseJob.py");
x0 =[150,.2];  % the ans is 200,.3.
lb =[100,.15]; ub = [300,.5];
options = optimoptions('particleswarm','SwarmSize',15,'HybridFcn', @fmincon,'InertiaRange',[.5,1.5]);
options.UseParallel = true;
[Xnew, fval, exitflag, output] = particleswarm(@myscript,2,lb, ub, options);

%% Function to generate bounds for particle swarm
function [ub,lb] = genNewBounds(x,stp)
    ub = [x(1)+stp(1),x(2)+stp(2)];
    if x(1)>stp(1) && x(2)>stp(2)
        lb = [x(1)-stp(1),x(2)-stp(2)];
    elseif x(1)<stp(1) && x(2)>stp(2)
        lb = [stp(1)-x(1),x(2)-stp(2)];
    elseif x(1)>stp(1) && x(2)<stp(2)
        lb = [x(1)-stp(1),stp(2)-x(2)];
    elseif x(1)<stp(1) && x(2)<stp(2)
        lb = [stp(1)-x(1),stp(2)-x(2)];
    end
end