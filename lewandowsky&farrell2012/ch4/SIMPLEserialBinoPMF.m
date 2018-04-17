function pmf = SIMPLEserialBinoPMF(c, presTime, recTime, J, Nc, N)
% c is the parameter of SIMPLE
% presTime and recTime are the effective temporal
% separation of items at input and output
% J is the length of the list
% Nc (a vector) is the number of items correctly recalled at each position
% N is the number of trials at each position

pmf = zeros(1,J);
Ti = cumsum(repmat(presTime,1,J));
Tr = Ti(end) + cumsum(repmat(recTime,1,J));

for i=1:J % i indexes output + probe position
    M = log(Tr(i)-Ti); 
    eta = exp(-c*abs(M(i)-M)); 
    pcor = 1./sum(eta); 
    pmf(i) = binomPMF(Nc(i), N, pcor);
end
