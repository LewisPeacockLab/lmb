nDataPts = 20;
rho = .8;
intercept = .0;

%generate simulated data
data=zeros(nDataPts,2);
data(:,2) = randn (nDataPts,1) ; %*\label{line:3:gendata}*\%
data(:,1) = randn (nDataPts,1) .* sqrt(1.0-rho^2) + (data (:,2).*rho) + intercept;  %*\label{line:3:gencordat}*\%

%do conventional regression analysis and compute parameters
bigX = [ones(nDataPts,1) data(:,2)];       %*\label{line:3:setupX}*\%
y = data (:,1);
b = bigX\y              %*\label{line:3:compreg}*\%

%assign and display starting values and call parameter-estimation function
startParms = [-1., .2]  %*\label{line:3:svs}*\%
[finalParms,finDiscrepancy] = wrapper4fmin(startParms,data) %*\label{line:3:callwrapper}*\%