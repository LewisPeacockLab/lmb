function lnL = SIMPLEmultinomLnL(c, alpha, presTime, recTime, J, k)
% c and alpha are the two parameters of SIMPLE
% presTime and recTime are the effective temporal
%    separation of items at input and output
% J is the length of the list
% k is a matrix; each row i corresponds to an output position,
%    and element j in the row gives the number of times
%    item j was recalled at position i

pmf = zeros(1,J);
Ti = cumsum(repmat(presTime,1,J));
Tr = Ti(end) + cumsum(repmat(recTime,1,J));

for i=1:J % i indexes output + probe position
    M = log(Tr(i)-Ti); 
    eta = exp(-c*abs(M(i)-M).^alpha); 
    pall = eta./sum(eta); %*\label{line:4:probObs}*\%
    lnL(i) = sum(k(i,:).*log(pall));
end