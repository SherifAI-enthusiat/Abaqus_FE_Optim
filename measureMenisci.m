function measuredDisplacements = measureMenisci(path)
    % This script collects the radial displacements of the menisci with respect two points at approx. centre of either tibial compartment.
    %% To - Do 
    % ------  Input required for optimisation
    % Need medial and lateral coordinate data - Done
    % Need medial and lateral displacement data - Done
    % Need tibial epicondyle location data - Done
    % Need axis data and location of derived - Done
    % Need path for finding results - Done
    % fig1 = figure(1); oriAx = axes;
    %% Undeformed and displacement data
    fp_coords = fullfile("MatlabOutput",["medCoordData.txt";"latCoordData.txt";"expData.mat"]);
    fp_disp = fullfile(path+"\Results",['medDisplData.txt';"latDisplData.txt";"medEpiCoordData.txt";"latEpiCoordData.txt"]);
    med_men = readmatrix(string(fp_coords(1)));lat_men = readmatrix(string(fp_coords(2)));
    med_men_displ = readmatrix(string(fp_disp(1)));lat_men_displ = readmatrix(string(fp_disp(2)));
    medEpiCoord = readmatrix(string(fp_disp(3)));latEpiCoord = readmatrix(string(fp_disp(4)));
    load(string(fp_coords(3)));
    % Undeformed data - Move step is applied to bring it to the undeformed technically. 
    % Since Abaqus has issues with surfaces in contact. So i have to rearrange the data into four load steps and added the Move step load case to coord data.
    %% This piece of code determines the axis on which the menisci lies - 
    Obj = myFunctions();
    Obj.oriCoords = vertcat(med_men,lat_men);
    Obj.med_men_length = size(med_men,1); 
    displ = vertcat(med_men_displ,lat_men_displ);
    axisSI= Obj.determineSI_Dir(); % Determines the horizontal plane within the coordinates
    axisAP = Obj.determineAP_Dir(); % This is experimental - i need to check that it works for all cases.
    axes = [axisSI,axisAP];
    %% This piece of code determines the location of the menisci points for measurements.
    tibiaEpiCoords = Obj.calcTibiaFeatures(medEpiCoord,latEpiCoord);% Calcs coordinate data for tibial features for the different load states. 
    [Points2Measure,Obj.revCentres] = Obj.PointsAroundMenisci(tibiaEpiCoords,planeHeight,Obj.axes);
    %% I am here - Need to verify that points around the menisci are at the right location.
    % relative to surface from Abaqus. i then need to check resultant coords and measure points.
    %% FindPointsInCylinder function
    [measuredDisplacements,Obj] = Obj.EstimateMenisciDisplacements(Points2Measure,displ);
    %% Examine the output from processing.
    % figure(3)
    % hold on
    % for it=1:4
    %     step =[Obj.defCoords(it).med;Obj.defCoords(it).lat];
    %     scatter3(step(:,1),step(:,2),step(:,3));
    % end
end
