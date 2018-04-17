% script catModels
clear all
close all

dataP = [0.75,0.67,0.54,0.4,0.4,0.37,0.58,0.71;
    0.92,0.81,0.53,0.28,0.14,0.22,0.45,0.81;
    0.91,0.97,0.93,0.64,0.28,0.09,0.12,0.7;
    0.98,0.94,0.85,0.62,0.2,0.037,0.078,0.71;
    0.97,0.94,0.8,0.58,0.4,0.45,0.81,0.97;
    0.29,0.66,0.85,0.71,0.33,0.1,0.32,0.77];

% number sessions x 10 blocks x 96 trials /(n stimuli)
Ntrain = ((5*10*96)/8);%*\label{line:7:Ntrain}*\%
pfeedback = [.6 .6 1 1 0 0 .6 .6];%*\label{line:7:pfeedback}*\%
Afeedback = pfeedback .* Ntrain;
feedback = [Afeedback; Ntrain-Afeedback];%*\label{line:7:feedback}*\%

Ntest = ((3*10*96)/8);%*\label{line:7:Ntest}*\%
N = repmat(Ntest,1,8);%*\label{line:7:NtestToN}*\%

dataF = ceil(Ntest.*(dataP));%*\label{line:7:dataF}*\%

stimval = linspace(.0625, .9375, 8);%*\label{line:7:stimval}*\%

%% Maximum likelihood estimation
for modelToFit = {'GCM','GRT','DEM'}; %*\label{line:7:modelLoop}*\%

    for ppt=1:6 %*\label{line:7:pptLoop}*\%
        switch char(modelToFit) %*\label{line:7:modelSwitch}*\%
            case 'GCM'
                f=@(pars) DEMlnL([pars 1], stimval, feedback, dataF(ppt,:), N);%*\label{line:7:fGCM}*\%
                [theta(ppt,:),lnL(ppt),exitflag(ppt)]=fminbnd(f, 0, 100);%*\label{line:7:GCMfminbnd}*\%
            case 'GRT'
                f=@(pars) GRTlnL(pars, stimval, dataF(ppt,:), N);
                [theta(ppt,:),lnL(ppt),exitflag(ppt)]=fminsearchbnd(f,[.3 .7 .1], [-1 -1 eps], [2 2 10]);%*\label{line:7:GRTmin}*\%
            case 'DEM'
                f=@(pars) DEMlnL(pars, stimval, feedback, dataF(ppt,:), N);
                [theta(ppt,:),lnL(ppt),exitflag(ppt)]=fminsearchbnd(f,[5 1], [0 0], [Inf Inf]);%*\label{line:7:DEMmin}*\%        
            otherwise
                error('Unknown model');
        end
        
        [junk, predP(ppt,:)] = f(theta(ppt,:));%*\label{line:7:runFinal}*\%
        
        hess = hessian(f,theta(ppt,:),10^-3);%*\label{line:7:catHessian}*\%
        cov = inv(hess);
        thetaSE(ppt,:) = sqrt(diag(cov));%*\label{line:7:thetaSE}*\%
    end

    figure%*\label{line:7:figure}*\%
    pptLab = {'SB','SEH','VB','BG','NV','LT'};
    
    for ppt=1:6
        subplot(2,3,ppt);
        plot(stimval, dataP(ppt,:), '-+');
        hold all
        plot(stimval, predP(ppt,:), '-.*');
        ylim([0 1]);
        xlabel('Luminance');
        ylabel('P(A)');
        title(char(pptLab{ppt}));
    end
    set(gcf, 'Name', char(modelToFit));%*\label{line:7:figureEnd}*\%
    
    t.theta = theta;%*\label{line:7:startPack}*\%
    t.thetaSE = thetaSE;
    t.nlnL = lnL;
    eval([char(modelToFit) '=t;']);%*\label{line:7:evalModelToFit}*\%
    clear theta thetaSE %*\label{line:7:endPack}*\%
end %*\label{line:7:endModelLoop}*\%


for ppt=1:6
    [AIC(ppt,:), BIC(ppt,:), AICd(ppt,:), BICd(ppt,:), AICw(ppt,:), BICw(ppt,:)] = ...
        infoCriteria([GCM.nlnL(ppt) GRT.nlnL(ppt) DEM.nlnL(ppt)], [1 3 2], repmat(Ntest*8,1,3));
end
