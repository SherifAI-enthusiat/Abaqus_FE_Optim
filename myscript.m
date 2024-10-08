function [outputn] = myscript(x)
% This function evaluates a Abaqus and returns a variable "count" which is
% used to locate the results file.
    formatSpec = 'lstestv2_parallel.py %d %d %d %d %d %d %d %d %d';%% This is where I can change bits.
    cmd = sprintf(formatSpec,x(1),x(2),x(3),x(4),x(5),x(6),x(7),x(8),x(9)); % 
    count= pyrunfile(cmd,"Mcount");
    ff = fullfile('MatlabOutput',{'expData.mat';sprintf('output_%d',count)});
    load(string(ff(1)));
    scalarM = 100.*ones(size(expData));
    tmp = load(string(ff(2)), 'dat');
    outputn = errorfunc(tmp.dat,expData,scalarM,1);
end