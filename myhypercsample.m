function [dat] = myhypercsample(SampNo,keyword)
% The purpose of this script is to go through a list of parameters
% generated and stored on a file called param_values.csv. 
% This way we can give the optimiser specific start points each time we
% start the optimisation. This is ensure that the solution space is well
% explored by the optimiser.

% The default is set to None to mean "orthotropic material" otherwise
% transverse isotropic material.
    ff = fullfile('Other',{'trans','ortho'},'param_values.csv');
    if keyword =="trans"
        T = readmatrix(string(ff(1)));
    else
        T = readmatrix(string(ff(2)));
    end
    n = size(rmmissing(T(1,:)),2);
    m = size(T,1);
    dat = zeros(SampNo,n);
    div = round(m/SampNo);
    tdiv = div; ndiv = 1; k = 1;
    while m > ndiv
        tmp = T(ndiv:tdiv,:);
        pn = randperm(div);
        dat(k,:) = rmmissing(tmp(pn(1),:));
        ndiv=tdiv; k=k+1;
        tdiv=tdiv+div;
        if tdiv>m
            Dtdiv= tdiv-m;
            tdiv = tdiv - Dtdiv;
        end
    end
        
% %     index = randperm(m);
%     SampRatio = SampNo/m;
%     ind = index(1:round(SampRatio*m));
%     dat = table2array(T(ind,:));
end