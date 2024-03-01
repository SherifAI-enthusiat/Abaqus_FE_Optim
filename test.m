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


% What coordinate transformation maps coords1 to coords2? 
coords1 = [35.452999999999996,44.829,47.759 ;45.415,46.879999999999995,46.586999999999996] ;
coords2 = [54.75,84.3,43.05; 43.5,87.0,44.4];

% Define the new set of coordinates
coords3 = [47.172999999999995,79.11,39.262];
% Perform Procrustes analysis
[d, Z, transform] = procrustes(coords1', coords2');

% d is the Procrustes distance (a measure of the dissimilarity between the two sets)
% Z is the transformed coordinates of coords1 that best align with coords2
% transform is the transformation information (scaling, rotation, translation)

% Extract rotation matrix, translation vector, and scaling factor
R = transform.T;
t = transform.c(1, :);
s = transform.b;

% Display the results
disp('Rotation Matrix:');
disp(R);
disp('Translation Vector:');
disp(t);
disp('Scaling Factor:');
disp(s);

% Apply the Procrustes transformation to coords3
transformed_coords3 = bsxfun(@plus, s * (R * coords3')', t);

disp('Transformed Coordinates (coords3):');
disp(transformed_coords3);

