function [x,fVal] = wrapper4fmin(pArray,data) %*\label{line:3:wraphead}*\%

[x,fVal] = fminsearch(@bof,pArray); %*\label{line:3:fmins}*\%

%nested function 'bof' inherits 'data' and argument 'parms'
%is provided by fminsearch
    function rmsd=bof(parms)     %*\label{line:3:bofhead}*\%

        predictions=getregpred(parms, data); %*\label{line:3:bofcallpred}*\%
        sd=(predictions-data(:,1)).^2;
        rmsd=sqrt(sum(sd)/numel(sd));
    end                         %*\label{line:3:bofend}*\%
end

