function preds = getregpred (parms,data)
b1 = parms(1);
b0 = parms(2);
preds = b0 + (b1 .* data(:,2));   %*\label{line:3:grpcompute}*\%

%plot current predictions and data and wait for keypress
clf      
hold on  
plot (data(:,2),data(:,1), 'o', 'MarkerFaceColor',[0.4 0.4 0.4],'MarkerEdgeColor','black');
plot (data(:,2),preds, '-k');
axis([-2 2 -2 2]);
xlabel('X','FontSize',18,'FontWeight','b');
ylabel('Y','FontSize',18,'FontWeight','b');
set(gca,'Ytick',[-2:2],'Xtick',[-2:2])
box on
pause
