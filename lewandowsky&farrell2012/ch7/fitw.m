% Program to estimate parameters for WITNESS 
% for Lewandowsky and Farrell's
% "Computational Modeling in Cognition: Principles and Practice"
global consts;

consts.seed = 2135; %for random generator   %*\label{line:7:c1}*\%
consts.lSize=6;     %lineup size
consts.nRep=1000;   %number of reps at each call
consts.n=100;       %number of features in vectors
consts.nCond=9;     %number of conditions modeled
consts.fChoice=[7 8 9];   %forced-choice conditions
consts.paLineup=[4 5 6];  %paLineup conditions
consts.ptToCrit=[3 4 5 3 4 5]; %slots in parameters  %*\label{line:7:c2}*\%

%Data Exp 1 & 2 of Clare & Lewandowsky (2004),
%columns are: Suspect, Foil, and Reject
data = [.80, .13, .07;    %PP control    %*\label{line:7:d1}*\%
        .57, .06, .36;    %PP holistic
        .69, .12, .19;    %PP featural
        .05, .72, .23;    %PA control
        .20, .28, .52;    %PA holistic
        .00, .48, .52;    %PA featural
        .86, .14, .00;    %Exp 2 control
        .81, .19, .00;    %Exp 2 holistic
        .84, .16, .00];   %Exp 2 featural    %*\label{line:7:d2}*\%

%initialize parameters in order: 
%  s  
%  sim   
%  crec -control
%  crec -holistic 
%  crec -featural 
disp ('Starting values of parameters')
startParms = [0.2942    0.3508    1.0455    2.0930    1.8050]     %*\label{line:7:initparm}*\%
consts.maxParms = [1. 1. inf inf inf];   %*\label{line:7:maxparm}*\%

[finalParms,fVal] = Wwrapper4fminBnd(startParms, data);  %*\label{line:7:w4f}*\%

%print final predictions
predictions = witness(finalParms)


