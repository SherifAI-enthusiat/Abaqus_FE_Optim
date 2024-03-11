% E_Fval = zeros(size(solutions,2),3);
% for i=1:size(solutions,2)
%     E_Fval(i,1:2) = solutions(1,i).X;
%     E_Fval(i,3) = solutions(1,i).Fval;
% end
% subplot(1,2,1)
% scatter(E_Fval(:,1),E_Fval(:,3),"ko")
% hold on
% scatter(E_Fval(1,1),E_Fval(1,3),"r*")
% subplot(1,2,2)
% scatter(E_Fval(:,2),E_Fval(:,3),"ko")
% hold on
% scatter(E_Fval(1,2),E_Fval(1,3),"r*")
% 
% %%
% i=5;
% plotyy(E_Fval(1:i,1),E_Fval(1:i,2),E_Fval(1:i,1),E_Fval(1:i,3),'scatter');

% %% Write solutions to file
% new = zeros(size(solutions,2),10);
% for i=1:size(solutions,2)
% %     solutions(1,i).X
%     new(i,:) = [solutions(1,i).Fval,solutions(1, i).X];
% end
% act = [0,20,10,50,0.3,0.2,0.2,4.7115,1.4583,1.4583];
% new=[act;new];
% writematrix(new,"optimised.txt")

%% Testing python run functions
% if py.ParamTools.material_stability(x)
%     sprintf("Yes")
% end

% Measured coordinates on rigid component after a given state
% state1 = [52.74, 70.32, 42.78; 40.73, 73.25, 44.83];
% state2 = [52.74, 72.664, 43.95; 40.73, 75.594, 46.29];
% state3 = [49.517, 72.957, 45.708; 37.211, 74.422, 47.759];
% state4 = [53.326, 74.129, 46.001; 41.313, 77.938, 48.052];
% state5 = [52.739999999999995,70.32,42.778;40.727,73.25,44.829];


% % What coordinate transformation maps coords1 to coords2? 
% coords1 = [35.452999999999996,44.829,47.759 ;45.415,46.879999999999995,46.586999999999996] ;
% coords2 = [54.75,84.3,43.05; 43.5,87.0,44.4];
% 
% % Define the new set of coordinates
% coords3 = [47.172999999999995,79.11,39.262];
% % Perform Procrustes analysis
% [d, Z, transform] = procrustes(coords1', coords2');
% 
% % d is the Procrustes distance (a measure of the dissimilarity between the two sets)
% % Z is the transformed coordinates of coords1 that best align with coords2
% % transform is the transformation information (scaling, rotation, translation)
% 
% % Extract rotation matrix, translation vector, and scaling factor
% R = transform.T;
% t = transform.c(1, :);
% s = transform.b;
% 
% % Display the results
% disp('Rotation Matrix:');
% disp(R);
% disp('Translation Vector:');
% disp(t);
% disp('Scaling Factor:');
% disp(s);
% 
% % Apply the Procrustes transformation to coords3
% transformed_coords3 = bsxfun(@plus, s * (R * coords3')', t);
% 
% disp('Transformed Coordinates (coords3):');
% disp(transformed_coords3);


%% Tibial features 
experimentData.knee4 = [52.739999999999995,70.32,42.778;
	40.727,73.25,44.829];
experimentData.knee5 = [35.452999999999996,44.829,47.759;
	45.415,46.879999999999995,46.586999999999996];
experimentData.knee2 = [54.75,84.3,43.05;
	43.5,87.0,44.4];

latDisp = [4.350000000000000000e+01,8.700000000000000000e+01,4.420000076293945312e+01;
-2.637968771159648895e-02,1.829739953384543291e-34,1.256193280220031738e+00;
8.018562570214271545e-03,1.862337812781333923e-02,1.152442455291748047e+00;
1.102145668119192123e-02,2.548521198332309723e-02,1.494221210479736328e+00;
1.304368861019611359e-02,3.008034639060497284e-02,1.762936234474182129e+00];

medDisp = [5.475000000000000000e+01,8.430000305175781250e+01,4.284999847412109375e+01;
-2.932956069707870483e-02,1.829739953384543291e-34,1.231854081153869629e+00;
-1.013840455561876297e-02,-5.650383606553077698e-02,1.152426958084106445e+00;
-1.399107091128826141e-02,-7.745420932769775391e-02,1.494205713272094727e+00;
-1.660234853625297546e-02,-9.149129688739776611e-02,1.762920737266540527e+00];

Obj = myFunctions();
dataKnee2 = Obj.calcTibiaFeatures(medDisp,latDisp);

% abaqus.knee4 = [];
% abaqus.knee5 = [];
% abaqus.knee2 = [];
scatter3(experimentData.knee2(:,1),experimentData.knee2(:,2),experimentData.knee2(:,3),"green","filled")
hold on
scatter3(dataKnee2.lat(1,1),dataKnee2.lat(1,2),dataKnee2.lat(1,3));
scatter3(dataKnee2.med(1,1),dataKnee2.med(1,2),dataKnee2.med(1,3));
legend("Experimental- tibial feature locations","Abaqus tibial feature locations -lateral","Abaqus tibial feature locations -medial")


