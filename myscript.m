function [outputn] = myscript(x)
% This function evaluates a Abaqus and returns a variable "count" which is
% used to locate the results file.
    formatSpec = 'lstestv2_parallel_v1.py %d %d';%% This is where I can change bits for the meterial or parameters to optimise.
    cmd = sprintf(formatSpec,x(1),x(2)); % This is where I can change bits.
    [count,data]= pyrunfile(cmd,["Mcount","data"]);
    ff = fullfile('MatlabOutput',{'expData.mat'});
    load(string(ff(1)));
    scalarM = 100.*ones(size(expData));
    % tmp = load(string(ff(2)), 'dat');
    % outputn = errorfunc(tmp.dat,expData,scalarM,1);
    outputn = errorfunc(double(data),expData,scalarM);
%     fid = fopen('writeOptimParameters.ascii', 'w');  % Open file in binary write mode
%     stp = sprintf('%d %d %d',x(1),x(2),outputn);
%     fwrite(fid,stp); fclose(fid);  % Close the file % Write matrix as double-precision floating-point values
end

