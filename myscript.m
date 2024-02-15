function [outputn] = myscript(x)
% This function evaluates in Abaqus and returns a variable "count" which is
% used to locate the results file.
    vp = .01; vf_p = .01;
    Gp = x(1)/(2*(1+vp)); % Gp
    x = [x(1),x(1),x(2),vp,vf_p,vf_p,Gp,x(3),x(3)];
%     scalarM = 100.*ones(size(expData));
    ff = fullfile('MatlabOutput',{'expData.mat'});
    load(string(ff(1)));  
    if py.ParamTools.material_stability(x)
        formatSpec = 'lstestv2_parallel.py %d %d %d %d %d %d %d %d %d';%% This is where I can change bits.
        cmd = sprintf(formatSpec,x(1),x(2),x(3),x(4),x(5),x(6),x(7),x(8),x(9)); % 
        [~,data]= pyrunfile(cmd,["Mcount","data"]);
        
    else
        data = zeros(4,12);
    end
    outputn = errorfunc(double(data),expData);
end