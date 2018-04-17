% Implementation of the phonological loop for 
% Lewandowsky and Farrell's
% "Computational Modeling in Cognition: Principles and Practice"
% Sage publishing.
clear all

nReps = 1000;        %number of replications   %*\label{line:nreps}*\%

listLength = 5;     %number of list items
initAct = 1;        %initial activation of items
dRate = .8;         %decay rate (per second)
delay = 5;          %retention interval (seconds)
minAct = .0;        %minimum activation for recall  %*\label{line:minact}*\%

rRange = linspace(1.5,4.,15);   %*\label{line:rRange}*\%
tRange = 1./rRange;
pCor = zeros(size(rRange));

i=1;                %index for word lengths %*\label{line:ieq1}*\%
for tPerWord=tRange

    for rep=1:nReps
        actVals = ones(1,listLength)*initAct;  %*\label{line:actVals}*\%

        cT = 0;
        itemReh = 0; % start rehearsal
                     % with beginning of list
        while cT < delay   %*\label{line:whilect}*\%
          
            intact = find(actVals>minAct);
            % find the next item still accessible
            itemReh = find(intact>itemReh, 1);
            % rehearse or return to beginning of list
            if isempty(itemReh)
                itemReh=1;
            end
            actVals(itemReh) = initAct  %*\label{line:restore}*\%
            
            % everything decays
            actVals = actVals - (dRate.*tPerWord) %*\label{line:decay}*\%
            cT=cT+tPerWord; %*\label{line:clock}*\%
        end
        pCor(i) = pCor(i) + (sum(actVals>minAct)./listLength); %*\label{line:pcor}*\%
        
    end
    i=i+1;
end %*\label{line:endFrame}*\%

scatter(rRange,pCor./nReps,'s','filled','MarkerFaceColor','k')
xlim([0 4.5])
ylim([0 1])
xlabel('Speech Rate')
ylabel('Proportion Correct') %*\label{line:endFrame}*\%

%the following code works on SL home machine running vista; the coordinates
%are screen-specific
%I = getframe(gcf,[-4,-4,569,504]);
%imwrite(I.cdata, 'WLEsim1.jpg');