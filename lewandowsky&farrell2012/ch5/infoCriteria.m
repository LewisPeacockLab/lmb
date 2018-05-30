function [AIC, BIC, AICd, BICd, AICw, BICw] = infoCriteria(nlnLs, Npar, N)
% Calculate information criteria (AIC; BIC),
%   IC differences from best model (AICd; BICd),
%   and model weights (AICw, BICw)
%   from a vector of negative lnLs
% Each cell in the vectors corresponds to a model
% Npar is a vector indicating the 
%   number of parameters in each model
% N is the number of observations on which
%   the log-likelihoods were calculated

AIC = 2.*nlnLs + 2.*Npar;
BIC = 2.*nlnLs + Npar.*log(N);

AICd = AIC-min(AIC);
BICd = BIC-min(BIC);

AICw = exp(-.5.*AICd)./sum(exp(-.5.*AICd));
BICw = exp(-.5.*BICd)./sum(exp(-.5.*BICd));