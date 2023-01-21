% Global count
clear,clc;
x0 =[20,10,50,0.3,0.2,0.2,4.7115,1.4583,1.4583]; % [20,20,100,0.3,0.2,0.2,4.7115,1.4583,1.4583]
lb =[1,1,1,.15,.15,.15,1,1,1];
ub =[20,20,100,.5,.5,.5,30,30,30];
% % % Custom points
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
[Xnew,fval,exitflag,output,solutions]= run(ms,problem,100);
