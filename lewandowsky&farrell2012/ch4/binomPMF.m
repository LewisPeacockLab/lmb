function pMass = binomPMF(k, N, p)

% this code is vectorized, so we can
% pass a vector of p's and obtain
% a vector of probability masses back
% k cannot be a vector; instead, use
% binopdf in the Mathworks Statistics Toolbox
pMass = nchoosek(N,k).* p.^k .*(1-p).^(N-k);