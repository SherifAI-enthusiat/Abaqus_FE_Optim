function result = errorfunc(data,expData,dir)
    temp = 100*(data(1:end,:)-expData)./expData; % .*scalarM TO DO need to check dimensions here.
    temp = temp.^2;
    if exist("dir",'var')
        result = sum(temp,dir);
    else
        result = sum(temp,'all'); 
    end
end