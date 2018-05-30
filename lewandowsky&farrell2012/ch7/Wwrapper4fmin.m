function [x, fVal] = Wwrapper4fmin(parms, data)
global consts;

defOpts = optimset ('fminsearch');  %*\label{line:7:opt1}*\%
options = optimset (defOpts, 'Display', 'iter', 'MaxFunEvals', 400)  %*\label{line:7:opt2}*\%
[x,fVal,dummy,output] = fminsearch(@bof,parms,options,data)

    function rmsd=bof(parms, data)
        if (min(parms) < 0) || (min(consts.maxParms - parms) < 0)  %*\label{line:7:bound}*\%
            rmsd = realmax;
        else
            sd=(witness (parms)-data).^2;
            rmsd=sqrt (sum(sum(sd))/numel(data));
        end
    end
end