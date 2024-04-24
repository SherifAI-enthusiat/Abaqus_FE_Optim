
function result = errorfunc(data,expData,scalarM,dir)
    % temp = (data(1:2,:)-expData).^2.*scalarM; % TO DO need to check dimensions here.
    temp = 100*(data(1:end,:)-expData)./expData;
    temp = temp.^2;
    if exist("dir",'var')
        result = sum(temp,dir);
    else
        result = sum(temp,'all'); 
    end
end