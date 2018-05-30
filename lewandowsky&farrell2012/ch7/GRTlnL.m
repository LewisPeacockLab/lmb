function [lnL, predP] = GRTlnL(theta, x, data, N)
% gives the negative log-likelihood
% for response frequencies from a single participant (data)
% given the GRT parameters (in vector theta),
% the stimulus values in x,
% the number of times `A' was selected as a response (data)
% and the total number of test trials for each stimulus (N)

bound1 = theta(1);%*\label{line:7:bound1}*\%
bound2 = theta(2);%*\label{line:7:bound2}*\%

if bound1 >= bound2 %*\label{line:7:boundIf}*\%
    lnL = realmax;
    predP = repmat(NaN, size(N));
end%*\label{line:7:endBoundIf}*\%

sd = theta(3);%*\label{line:7:sd}*\% 

a1 = normalCDF((bound1-x)./sd);%*\label{line:7:a1}*\% 
a2 = 1 - normalCDF((bound2-x)./sd);%*\label{line:7:a2}*\% 
predP = a1 + a2;%*\label{line:7:a1plusa2}*\%

lnL = -sum(data.*log(predP) + (N-data).*log(1-predP));%*\label{line:7:GRTbino}*\%

%% normalCDF
function p = normalCDF(x)

p = 0.5.*erf(x./sqrt(2));