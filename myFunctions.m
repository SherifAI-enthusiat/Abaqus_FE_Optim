classdef myFunctions
    properties
    %     parameters; % these are parameters used to determine a cylinder.
    %     sfM; % this approx surface data.
    %     X_conv; % 
    %     oriCoords; % These are teh original coordinates collected from Abaqus - these are undeformed coordinates.
    %     med_men_length; % This is dimension length of the medial mesh from Matlab
    %     defCoords; % This is used to store the resultant coords for all load cases.
    %     revCentres; % These are the new tibial centres for measurement purposes.
    %     results; % Results of measured displacements.
    %     axes; % these are variables from ScanIP for making measurements in MATLAB.
    %     pixelConv; % This is data from ScanIP i.e. convertion factor from pixel to length(mm).
        path; % Path to experimental data stored.
    %     mnmx; % this is pretty much just for knee 5 - where SI points downwards.All the other cases are fine
    %     weights; % This will be a means to control the what nodes the optimiser focuses on. {Follows 1st optimisation of all knees}. The default is none provided is ones
    end 

    methods
        %% Cost function for the optimissation - this function handles everything
        function [outputn] = myscript(obj,x)
        % This function evaluates in Abaqus and returns a variable "count" which is
        % used to locate the results file.
            vp = .01; vf_p = .01;
            Gp = x(1)/(2*(1+vp)); % Gp
            x = [x(1),x(1),x(2),vp,vf_p,vf_p,Gp,x(3),x(3)];
        %     scalarM = 100.*ones(size(expData));
            ff = fullfile(obj.path,{'expData.mat'});
            load(string(ff(1)));   [a,~]=size(expData);
            if py.ParamTools.material_stability(x)
                formatSpec = 'lstestv2_parallel.py %d %d %d %d %d %d %d %d %d';%% This is where I can change bits.
                cmd = sprintf(formatSpec,x(1),x(2),x(3),x(4),x(5),x(6),x(7),x(8),x(9)); % 
                
                % workspacePath = "C:\WorkThings\github\Abaqus_FE_Optim\runDir\workspace_17985565299"
                try
                    [~, data]= pyrunfile(cmd,["Mcount","data"]);
                    data = data;
                catch
                    data = zeros(a,12);
                end
            else
                data = zeros(a,12);
            end
            outputn = obj.errorfunc(double(data),expData);
        end

        function result = errorfunc(obj,data,expData,dir)
            temp = 100*(data(1:end,:)-expData)./expData; % .*scalarM TO DO need to check dimensions here.
            temp = temp.^2;
            if exist("dir",'var')
                result = sum(temp,dir);
            else
                result = sum(temp,'all'); 
            end
        end
    end
end