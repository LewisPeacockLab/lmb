function [theta, fVal, quants] =  bootstrapExample

rand('state',14141);
randn('state',151515);

data = [40, 28, 13, 11, 11, 10, 6, 11, 17, 8, 14,...
    14, 13, 14, 22, 43, 53, 70, 71, 74];
N = 80;

% some assumed experimental parameters
Ti = 1:20;
Tr = 30; % we assume retrieval time is fixed here

% information and initialization for the bootstrap procedure
bootSamples = 1000;
samplePhat = zeros(bootSamples, 3);

% MLE of parameters
[theta, fVal] = fminsearch(@(x) SIMPLEfreeBino(x, data, Ti, Tr, N), [2 .1 20]);

% run the model one last time to get the parameters
[temp, pred] = SIMPLEfreeBino(theta, data, Ti, Tr, N);

% now do the bootstrapping
for i=1:bootSamples
    
    if mod(i,100)==0
        disp(i);
    end
    % the binornd function is from the Statistics Toolbox
    sampData = binornd(80, pred);
    [samplePhat(i,:)] = fminsearch(@(x) SIMPLEfreeBino(x, sampData, Ti, Tr, N), theta);
end

% the quantile function comes from the MATLAB Statistics Toolbox
quants = quantile(samplePhat,[.025 .975]);