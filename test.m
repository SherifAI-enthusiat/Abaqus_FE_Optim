% E_Fval = zeros(size(solutions,2),3);
% for i=1:size(solutions,2)
%     E_Fval(i,1:2) = solutions(1,i).X;
%     E_Fval(i,3) = solutions(1,i).Fval;
% end
% subplot(1,2,1)
% scatter(E_Fval(:,1),E_Fval(:,3),"ko")
% hold on
% scatter(E_Fval(1,1),E_Fval(1,3),"r*")
% subplot(1,2,2)
% scatter(E_Fval(:,2),E_Fval(:,3),"ko")
% hold on
% scatter(E_Fval(1,2),E_Fval(1,3),"r*")
% 
% %%
% i=5;
% plotyy(E_Fval(1:i,1),E_Fval(1:i,2),E_Fval(1:i,1),E_Fval(1:i,3),'scatter');

%% Write solutions to file
new = zeros(size(solutions,2),10);
for i=1:size(solutions,2)
%     solutions(1,i).X
    new(i,:) = [solutions(1,i).Fval,solutions(1, i).X];
end
act = [0,20,10,50,0.3,0.2,0.2,4.7115,1.4583,1.4583];
new=[act;new];
writematrix(new,"optimised.txt")

%% Gaussian test
clear,clc
pyrunfile("initialiseJob.py");
vars_Ep = optimizableVariable('Ep',[.01,20]);
vars_Ef = optimizableVariable('Ef',[1,250]);
vars_Gpf = optimizableVariable('Gpf',[1,30]);
vars = [vars_Ep,vars_Ef,vars_Gpf];
x0 = [20,50,1.4583];
fun = myscript(x0);
results = bayesopt(fun,[vars_Ep,vars_Ef,vars_Gpf],'Verbose',0,...
    'AcquisitionFunctionName','expected-improvement-plus',UseParallel=true); % MinWorkerUtilization=3

