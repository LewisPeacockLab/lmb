function [dev, p] = SIMPLEfreeBino(theta, data, recTime, presTime, N)

c = theta(1);
t = theta(2);
s = theta(3);

p = zeros(1,length(data));
lnL = zeros(1,length(data));

dist = log(recTime-presTime);

for i=1:length(data)
    for j=1:length(data)
        d(j) = (exp(-c*abs(dist(i)-dist(j))))./sum((exp(-c*abs(dist-dist(j)))));
    end
    p(i) = sum(1./(1+exp(-s*(d-t))));
    if (p(i)>1-eps)
        p(i)=1-eps;

    end
    lnL(i) = data(i).*log(p(i)) + (N-data(i)).*log(1-p(i));%*\label{line:5:lnLbino}*\%
end

dev = sum(-lnL);
