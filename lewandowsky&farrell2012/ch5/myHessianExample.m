function [x, fVal,hess, cov] = myHessianExample

rand('seed',151513);
randn('seed',151513);

N=100;
y = normrnd(500,65, [N 1]) + exprnd(100, [N 1]); %*\label{line:5:gendata}*\%

% find MLEs for ex-Gaussian parameters
% use inline specification of function to be minimized
%   so we can pass parameters and data

[x,fVal] = fminsearch(@(x) exGausslnL(x,y), [500 65 100]) %*\label{line:5:MLE}*\%

% find Hessian for MLEs
hess = hessian(@exGausslnL,x,10^-3, y); %*\label{line:5:hessian}*\%
cov = inv(hess); %*\label{line:5:invhess}*\%

end

function fval = exGausslnL(theta, y)

mu = theta(1);
sigma = theta(2);
tau = theta(3);

fval = log(1./tau)+...
    (((mu-y)./tau)+((sigma.^2)./(2.*tau.^2)))...
    +log(.5)...
    +log(1+erf((((y-mu)./sigma)-(sigma./tau))./sqrt(2)));
fval = -sum(fval); % turn into a summed negative log-likelihood for minimization
end

