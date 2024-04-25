function [outputn] = myscript(x)
% This function evaluates in Abaqus and returns a variable "count" which is
% used to locate the results file.
    vp = .01; vf_p = .01;
    Gp = x(1)/(2*(1+vp)); % Gp
    x = [x(1),x(1),x(2),vp,vf_p,vf_p,Gp,x(3),x(3)];
%     scalarM = 100.*ones(size(expData));
    ff = fullfile('MatlabOutput',{'expData.mat'});
    load(string(ff(1)));  [a,~]=size(expData);
    if py.ParamTools.material_stability(x)
        formatSpec = 'lstestv2_parallel.py %d %d %d %d %d %d %d %d %d';%% This is where I can change bits.
        cmd = sprintf(formatSpec,x(1),x(2),x(3),x(4),x(5),x(6),x(7),x(8),x(9)); % 
        try
            [~,data]= pyrunfile(cmd,["Mcount","data"]);
        catch Error
            warning('Problem using function.  Assigning a value of 0.');
            warning(Error)
            data = zeros(a,12);
        end
    else 
        data = zeros(a,12);
    end
    outputn = errorfunc(double(data),expData);
end