classdef myFunctions
    properties
        parameters;
        sfM;
        X_conv;
        oriCoords;
        med_men_length;
        defCoords; % This is used to store the resultant coords.
        revCentres; % These are the new tibial centres for measurement purposes
        results; % Results of measured displace
        axes;
    end 

%% Plotting my points
    methods
        function obj = variables(obj,parameters,sfM,varargin)
            if ~isempty(varargin)
                obj.X_conv = varargin{1};
            end
            obj.parameters = parameters;
            obj.sfM = sfM;
        end
        %% Generating point to build cylinder
        function symmetric_ang = generatePoints(obj,startAng, noPoints)
            interval_size = startAng * 2 / (noPoints - 1);
            symmetric_ang = zeros(1, noPoints);
            
            for it = 1:noPoints
                ang = startAng - interval_size * (it - 1);
                symmetric_ang(it) = ang;
            end
        end
        
        %% Rptation matrix to build cylinder
        function [rotMa] = rotationMat(obj,rot_deg,axis)
            rad = deg2rad(rot_deg);
            if axis== 1
                rotMa = [1, 0, 0;
                         0, cos(rad), -sin(rad);
                         0, sin(rad), cos(rad)];
            elseif axis== 2
                rotMa = [cos(rad), 0, sin(rad);
                         0, 1, 0;
                         -sin(rad), 0, cos(rad)];
            elseif axis== 3
                rotMa = [cos(rad), -sin(rad), 0;
                         sin(rad), cos(rad), 0;
                         0, 0, 1];
            end
        end

        %% Convert cylinder to Point cloud
         function [X, Y, Z] = transformCylinder(obj,this, X, Y, Z)
            a = cast([0, 0, 1], 'like', this.Parameters);
            h = this.Height;
            % Rescale the height.
            Z(2, :) = Z(2, :) * h;
            
            if h == 0
                b = [0, 0, 1];
            else
                b = (this.Parameters(4:6) - this.Parameters(1:3)) / h;
            end
            
            % Rotate the points to the desired axis direction and translate
            % the cylinder.
            translation = this.Parameters(1:3);
            if iscolumn(translation)
                translation = translation';
            end
            v = cross(a, b);
            s = dot(v, v);
            if abs(s) > eps(class(s))
                Vx = [ 0, -v(3), v(2); ...
                     v(3),  0,  -v(1); ...
                    -v(2), v(1),   0];
                R = transpose(eye(3) + Vx + Vx*Vx*(1-dot(a, b))/s);
                
                XYZ = bsxfun(@plus, [X(:), Y(:), Z(:)] * R, translation);
            else % No rotation is needed, only translation.
                XYZ = bsxfun(@plus, [X(:), Y(:), Z(:)], translation);
            end
            X = reshape(XYZ(:, 1), 2, []);
            Y = reshape(XYZ(:, 2), 2, []);
            Z = reshape(XYZ(:, 3), 2, []);
         end

        %% This works for interpolating and finding the point around the cylinder.
        % Generates a cylinder given bottom and top points of the cylinder and the
        % radius.Dimension [1*7]
    function [interData,cyl_model,obj] = cylinderIntersect(obj,parameters,testData) 
            % close all % This is important because I use the figure to obtain the point hence only figure here is kept.
            cyl_model = cylinderModel(parameters);
            [X, Y, Z] = cylinder(cyl_model.Radius, 100);
            [X, Y, Z] = obj.transformCylinder(cyl_model,X, Y, Z);
            % Separating into bottom and top circle making the cylinder.
            X1 = X(1,:); X2 = X(2,:); 
            Y1 = Y(1,:); Y2 = Y(2,:); 
            Z1 = Z(1,:); Z2 = Z(2,:); 
            D1 = [X1',Y1',Z1']; D2 = [X2',Y2',Z2']; % D1 is bottom cylinder and D2 is top cylinder 
            dirVec = D2 - D1; % This is the corresponding direction vectors between points.
            t = linspace(0,1,100); 
            % fig2 = openfig('InitialMenisci.fig');
            % set(0, 'CurrentFigure', fig2);
            fig2 = figure(2); ax1 = axes;
            hold(ax1,"on") % If require we can assign axes and plot in specifc figure
            for i=1:size(D1,1)
                NewC = D1(i,:) + t'.*dirVec(i,:);
                plot3(NewC(:,1),NewC(:,2),NewC(:,3),"ks")  % This plot is in essense used to store and retrieve data
            end 
            
            AxisD = parameters(1:3) + t'.*dirVec(1,:); % dirVec(i,:) any direction here is // to cyl axis
            plot3(ax1,AxisD(:,1),AxisD(:,2),AxisD(:,3),"rs")
            hold(ax1,"off")
            set(0, 'CurrentFigure', fig2); h = gcf;  %current figure handle
            axesObjs = get(h, 'Children');  %axes handles
            dataObjs = get(axesObjs, 'Children'); 
            xdata = get(dataObjs, 'XData'); 
            ydata = get(dataObjs, 'YData');
            zdata = get(dataObjs, 'ZData');
            cyl_data =[]; [a,~] = size(xdata);
            for i=1:a
                nX = xdata{i,1}';nY = ydata{i,1}';nZ = zdata{i,1}';
                tmp = [nX,nY,nZ];
                cyl_data = [cyl_data;tmp];
            end
            shp = alphaShape(cyl_data,parameters(7));
            indices = inShape(shp,testData);
            interData = testData(indices,:);
            close(fig2)
    end

    function [sfM,sfM_G,obj] = fitmySurface(obj,data) 
        % The function finds the intersection between the surface and the cylinder
        % axis. "parameter" contains information [points1,points2,cyl_rad]
        % "data" contains information for the surface.
    %     nDir = Dir./norm(Dir);
        x_s = data(:,1);y_s = data(:,2);z_s = data(:,3);
        [sfM, sfM_G] = fit([x_s,y_s],z_s,"poly23");
        obj.sfM = sfM;
    end

    function res_Z = errorFunc(obj,t)
        % Function to minimise
        sfM = obj.sfM; p = obj.parameters;
        Dir = p(4:6) - p(1:3);
        ln_3D = p(1:3) + t*Dir; % This converts to x,y and z from t.
        x = ln_3D(1,1); y = ln_3D(1,2); z_ln = ln_3D(1,3);
        z = sfM.p00 + sfM.p10*x + sfM.p01*y + sfM.p20*x^2 + sfM.p11*x*y + sfM.p02*y^2 + sfM.p21*x^2*y + ...
            + sfM.p12*x*y^2 + sfM.p03*y^3;
        res_Z = (z_ln - z)^2;
    end


    function [ln_3D,pltM] = measuredPoint(obj,t,data)
        p = obj.parameters;
        Dir = p(4:6) - p(1:3);
        ln_3D = p(1:3) + t*Dir;
        apprxAns = mean(data);
        delTa = abs(ln_3D - apprxAns);
        cri = [.5,.5,.5]; ltn = ["cs","ks"];
        Bool = delTa>cri;
        if sum(Bool) >= 1
            pltM = ltn(1); ln_3D = apprxAns;
        else
            pltM = ltn(2);
        end
    end
    
    function [axis,tt] = determineSI_Dir(obj)
        % This is used to determine the axial orientation i.e. This is used to determine the Superior - Inferior axis 
        pcData = pointCloud(obj.oriCoords);
        tt = pcfitplane(pcData,5);
        [~,axis] = max(abs(tt.Normal));
    end

    function [AP_Dir] = determineAP_Dir(obj)
        % To-DO. This is used to determine the AP direction for my knee - might not be true though. Need to check for all knees 
        valA = sum(pca(obj.oriCoords));
        [~,AP_Dir] = max(valA);
    end
    
    function [tibiaEpiCoords] = calcTibiaFeatures(obj,medCoords,latCoords) %% - Done
        for i = 1:size(medCoords,1)-1
            tibiaEpiCoords.med(i,:) = medCoords(1,:) + medCoords(i+1,:);
            tibiaEpiCoords.lat(i,:) = latCoords(1,:) + latCoords(i+1,:);
        end
    end

    function [Points2Measure,newCentre] = PointsAroundMenisci(obj,tibiaEpiCoords,planeHeight,axes) % To - Do
        %% Important -- This code is a replica of what is in ScanIP("CalculateMenLocations.py") to allow congruency in results and for optimisation purposes.
        pixelConv = 0.15;
        ScalarA = 1.0; ScalarB = 1.5; ScalarC = 2.5; % These are definitions I visualised and liked in ScanIP - hence why Scalar is different for medial and lateral plateau points centres.
        D_vec = tibiaEpiCoords.lat(:,:) - tibiaEpiCoords.med(:,:); % This determines the points on the tibial plateaux that I measure bits from.
        [a,~] = size(D_vec);
        tes = obj.generatePoints(70,6); % these are defined constants in ScanIP
        lt = ["-","+"]; Points2Measure = struct();
        SI_Dir = axes(1); AP_Dir = axes(2);
        for it = 1:a
            % I will use newCentre to calc locations around the periphery of the menisci. The newcentre is calc based on two operations
            % 1. Using the direction vector based on tibial features 2. Modifying location using original tibia centres and translating by some amount.
            newCentre(it).med = tibiaEpiCoords.med(it,:) - ScalarA*D_vec(it,:);
            newCentre(it).lat = tibiaEpiCoords.lat(it,:) + ScalarB*D_vec(it,:); 
            newCentre(it).med(1,AP_Dir) = tibiaEpiCoords.lat(1,AP_Dir);
            newCentre(it).lat(1,AP_Dir) = tibiaEpiCoords.med(1,AP_Dir) - 6; % This value here "6" is based on definitions I made in ScanIP  
            newCentreA = [newCentre(it).med;newCentre(it).lat];
            DirV = D_vec(it,:).*ones(3,3); newcoord = [];
            for j = 1:2
                txt = "newCentreA(j,:) " + lt(j) +" dot(tmp,ScalarC*DirV')";
                for i = 1:6
                    tmp = obj.rotationMat(tes(i),SI_Dir);
                    new = eval(txt);
                    newcoord = [newcoord;new];
                end
            end
            % I make measurements on some given plane which corresponds to the planeHeight variable.
            newcoord(:,SI_Dir)= pixelConv*planeHeight(it); % this ".293" is the pixel resolution to convert to pixel height.
            newCentre(it).med(1,SI_Dir) = pixelConv*planeHeight(it); 
            newCentre(it).lat(1,SI_Dir) = pixelConv*planeHeight(it);
            Points2Measure(it).step = newcoord; 
        end
    end

    function defCoords = ResultantCoordinates(obj,displacements)
        % This function finds the deformed coordinate given coordinates from the assembly in Abaqus.  
        a = obj.med_men_length;
        med_men = obj.oriCoords(1:a,:); lat_men = obj.oriCoords(a+1:end,:); % These are the coordinates of the medial and lateral menisci
        med_men_displ = displacements(1:a*4,:); lat_men_displ = displacements((a*4)+1:end,:); % This data is composed of 4 steps {Move,Load1, Load2 and load3} 
        [a,~] = size(med_men_displ); [b,~] = size(lat_men_displ);
        a = a/4; b = b/4;  ltA = [1,a+1,2*a+1,3*a+1]; ltB = [1,b+1,2*b+1,3*b+1];
        for it =1:4
            defCoords(it).med = med_men + med_men_displ(ltA(it):a*it,:);
            defCoords(it).lat = lat_men + lat_men_displ(ltB(it):b*it,:);
        end
        % This is a structure with each row corresponding to the load step{Move, Load1, Load2,Load3}
    end

    function [results, obj] = EstimateMenisciDisplacements(obj,Points2Measure,displacements)
        cyl_rad =1; % this will be modified until suitable value is found{Verify by plotting}
        obj.defCoords = obj.ResultantCoordinates(displacements); % These are the coordinates after displacements 
        ltn = ["med_men","lat_men"]; % Separates the data into lateral and medial
        nlt = ["trp(1:6,:)","trp(7:12,:)"];  % These are the points plotted around the periphery of the menisci
        for it=1:size(Points2Measure,2)
            trp = Points2Measure(it).step;
            revCoords = [obj.revCentres(it).med;obj.revCentres(it).lat];
            med_men = obj.defCoords(it).med;
            lat_men = obj.defCoords(it).lat;
            for j=1:2
                trpn = eval(nlt(j)); measuredCoords = [];
                data = eval(ltn(j)); boolCoords = [];
                for i=1:6  %% To-Do -> I believe that the plot is causing the problem.
                    % dirVec = trpn(i,:) - revCoords(j,:);
                    parameters = [revCoords(j,:),trpn(i,:),cyl_rad];
                    cyl_mod = cylinderModel(parameters);
                    % plot(cyl_mod); legend("AutoUpdate","off")
                    % Generating and checking values that intersect with the cylinder
                    IntData = obj.cylinderIntersect(parameters,data);
                    % plot3(oriAx,IntData(:,1),IntData(:,2),IntData(:,3),"yo","DisplayName","Measure surface")
                    % legend('AutoUpdate', 'off')
                    % Fit surface and find intersect with cylinder axis
                    if size(IntData,1)>=9
                        sfM = obj.fitmySurface(IntData);
                        obj = obj.variables(parameters,sfM);
                        Con_X = fsolve(@obj.errorFunc,1);
                        [point,pltM]= obj.measuredPoint(Con_X,IntData);
                    else
                        point = mean(IntData); %[Solve for t == Con_X] this is the case where there is not enough data for data fitting.
                        pltM = "rs"; % These are approximate solutions.
                    end
                    measuredCoords = [measuredCoords;point];
                    boolCoords = [boolCoords;pltM];
                    % plot3(oriAx,point(:,1),point(:,2),point(:,3),pltM,"MarkerSize",5,"LineWidth",2)
                end
                if j ==1
                    obj.results(it).med = measuredCoords;
                    obj.results(it).medPlot = boolCoords;
                    obj.results(it).medDispl = sqrt(sum((revCoords(j,:) - measuredCoords).^2,2));
                else
                    obj.results(it).lat = measuredCoords;
                    obj.results(it).latPlot = boolCoords;
                    obj.results(it).latDispl = sqrt(sum((revCoords(j,:) - measuredCoords).^2,2));
                end
            end
        end
        results = obj.calcDisplacements();
    end

    function [displacements] = calcDisplacements(obj)
        a = size(obj.revCentres,2);
        displacements = zeros(a,12);
        for it = 1:a
            displacements(it,:)=[obj.results(it).medDispl;obj.results(it).latDispl]';
        end
    end
end
end

