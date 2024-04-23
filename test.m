% Need the tibial coordinates for all load cases
% Angles
% T 
myObj = myFunctions();
tst = [13.4,14.8,15.9,16.4,19,23.7;6.7,6.2,6.3,8,11.9,18.9];
angles  = myObj.generatePoints(70,6);

X = tst(:,1:3).*cos(angles(1:3));
Y = tst(:,1:3).*sin(angles(1:3));

scatter(X(1,:),Y(1,:))
hold on
scatter(X(2,:),Y(2,:))
hold off