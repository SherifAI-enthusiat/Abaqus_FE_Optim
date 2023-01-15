function [outputn] = myscript(x)
%     This is a counter to create individual folders for results and
%     extract by Par-pool
    count =1; key = true;
    while key==true
        ff = fullfile('MatlabOutput',{'expData.mat';sprintf('output_%d',count)});
        cmd1 = fullfile('runDir', sprintf('workspace_%d',count));
        if exist(cmd1)==7
            count = count + 1;
        else
%             cmd1 = fullfile('runDir',sprintf('workspace_%d',count));
            key = false;
        end
    end
%% Call to python and results
    formatSpec = 'lstestv2_parallel.py %d %d %d %d %d %d %d %d %d %d'; %% This is where I can change bits.
    cmd = sprintf(formatSpec,x(1),x(2),x(3),x(4),x(5),x(6),x(7),x(8),x(9),count);
    pyrunfile(cmd);
    load(string(ff(1)));
    scalarM = 100.*ones(size(expData));
    tmp = load(string(ff(2)), 'dat');
    outputn = errorfunc(tmp.dat,expData,scalarM,1);
        %     if exist(cmd1)==2
        %         delete(cmd1);
        %     end
end