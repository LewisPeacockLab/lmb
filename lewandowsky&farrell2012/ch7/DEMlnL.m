function [lnL, predP] = DEMlnL(theta, x, feedback, data, N)
% gives the negative log-likelihood
% for response frequencies from a single participant (data)
% given the DEM parameters (in vector theta), the stimulus values in x,
% the number of times each stimulus was an `A' in feedback
% the number of times `A' was selected as a response (data)
% and the total number of test trials for each stimulus (N)

c = theta(1);%*\label{line:7:getC}*\%
gamma = theta(2);%*\label{line:7:getGamma}*\%

for i=1:length(x)%*\label{line:7:DEMstartloop}*\%
    s = exp(-c.*abs(x(i)-x));%*\label{line:7:DEMs}*\%
    sumA = sum(s.*feedback(1,:));%*\label{line:7:sumA}*\%
    sumB = sum(s.*feedback(2,:));%*\label{line:7:sumB}*\%
    predP(i) = (sumA^gamma)/(sumA^gamma + sumB^gamma);%*\label{line:7:DEMLuce}*\%
end%*\label{line:7:DEMendloop}*\%

lnL = -sum(data.*log(predP) + (N-data).*log(1-predP));%*\label{line:7:DEMBino}*\%