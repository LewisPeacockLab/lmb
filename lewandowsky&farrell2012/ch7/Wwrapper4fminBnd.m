function [x, fVal] = Wwrapper4fminBnd(parms, data)
global consts;

[x,fVal,dummy,output] = fminsearchbnd(@bof,parms,zeros(size(parms)),consts.maxParms) %*\label{line:7:callbnd}*\%

    function rmsd=bof(parms)
        sd=(witness (parms)-data).^2;
        rmsd=sqrt (sum(sum(sd))/numel(data));
    end
end