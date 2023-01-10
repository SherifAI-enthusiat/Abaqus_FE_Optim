function [outputn] = myscript(x)
%     This is a counter to create individual folders for results and
%     extract by Par-pool
expData = [0.611925065517,0.631498813629,0.591993808746,0.488072931767,0.738442957401];
    count =1; key = true;
    while key==true
        cmd1 = sprintf('runDir\\workspace_%d',count);
        if exist(cmd1)==7
            count = count + 1;
        else
            cmd1 = sprintf('MatlabOutput\\output_%d.mat',count);
            key = false;
        end
     end
    A = 100; B = 100;
    scalar = [A,A,A,B,B];
    formatSpec = 'lstestv2_parallel.py %d %d %d'; %% This is where I can change bits.
    cmd = sprintf(formatSpec,x(1),x(2),count);
    pyrunfile(cmd); % pyrunfile(cmd,"data");
%     cmd1 = sprintf('MatlabOutput\\output_%d.mat',count);
    tmp = load(cmd1, 'dat');
%     outputn = sum(tmp.dat(2,:).*scalar,2);
    temp = (tmp.dat(1,:)-expData).^2.*scalar;
    outputn = sum(temp,2);
%     if exist(cmd1)==2
%         delete(cmd1);
%     end
end