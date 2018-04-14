% Implementation of the phonological loop for 
% Lewandowsky and Farrell's
% "Computational Modeling in Cognition: Principles and Practice"
% Sage publishing.
clear all
nReps = 1000;        %number of replications   
listLength = 5;     %number of list items
initAct = 1;        %initial activation of items
decRate = .8;       %mean decay rate (per second) %*\label{line:decRate}*\%
decSD = .1;         %standard deviation of decay rate %*\label{line:decSD}*\%
delay = 5;          %retention interval (seconds)
minAct = .0;        %minimum activation for recall  
rRange = linspace(1.5,4.,15);   %*\label{line:rRange2}*\%
tRange = 1./rRange;
pCor = zeros(size(rRange));

i=1;                %index for word lengths
for tPerWord=tRange

    for rep=1:nReps
        actVals = ones(1,listLength)*initAct;  
        dRate = decRate+randn*decSD;   %*\label{line:newdRate}*\%

        cT = 0;
        itemReh = 0; 
        while cT < delay   
            intact = find(actVals>minAct);
            itemReh = find(intact>itemReh, 1);
            if isempty(itemReh)
                itemReh=1;
            end
            actVals(itemReh) = initAct; 
            
            % everything decays
            actVals = actVals - (dRate.*tPerWord); 
            cT=cT+tPerWord; 
        end
        pCor(i) = pCor(i) + (sum(actVals>minAct)./listLength); 
    end
    i=i+1;
end 

scatter(rRange,pCor./nReps,'s','filled','MarkerFaceColor','k')
xlim([0 4.5])
ylim([0 1])
xlabel('Speech Rate')
ylabel('Proportion Correct')

%the following code works on SL home machine running vista; the coordinates
%are screen-specific
%I = getframe(gcf,[-4,-4,569,504]);
%imwrite(I.cdata, 'WLEsim2.jpg');