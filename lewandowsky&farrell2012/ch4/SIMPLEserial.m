function pcor = SIMPLEserial(c, presTime, recTime, J)
% c is the single parameter of SIMPLE
% presTime and recTime are the effective temporal
% separation of items at input and output
% J is the length of the list

pcor = zeros(1,J); %*\label{line:4:initpcor}*\%
Ti = cumsum(repmat(presTime,1,J)); %*\label{line:4:Ti}*\%
Tr = Ti(end) + cumsum(repmat(recTime,1,J)); %*\label{line:4:Tr}*\%

for i=1:J % i indexes output + probe position
    M = log(Tr(i)-Ti); %*\label{line:4:M}*\%
    eta = exp(-c*abs(M(i)-M)); %*\label{line:4:eta}*\%
    pcor(i) = 1./sum(eta); %*\label{line:4:pcor}*\%
end
