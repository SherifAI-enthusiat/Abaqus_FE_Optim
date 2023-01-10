E_Fval =zeros(size(solutions,2),3);
for i=1:size(solutions,2)
    E_Fval(i,1:2) = solutions(1,i).X;
    E_Fval(i,3) = solutions(1,i).Fval;
end
subplot(1,2,1)
scatter(E_Fval(:,1),E_Fval(:,3),"ko")
hold on
scatter(E_Fval(1,1),E_Fval(1,3),"r*")
subplot(1,2,2)
scatter(E_Fval(:,2),E_Fval(:,3),"ko")
hold on
scatter(E_Fval(1,2),E_Fval(1,3),"r*")

%%
i=5;
plotyy(E_Fval(1:i,1),E_Fval(1:i,2),E_Fval(1:i,1),E_Fval(1:i,3),'scatter');
