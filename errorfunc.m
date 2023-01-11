function result = errorfunc(data,expData,scalarM,dir)
    temp = (data(1:end,:)-expData).^2.*scalarM; % TO DO need to check dimensions here.
    if exist("dir",'var')
        result = sum(temp,dir);
    else
        result = sum(temp,'all'); 
    end
end