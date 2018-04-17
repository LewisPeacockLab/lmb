mMu = 5; mTau= 5; muN=50; tauN=50; %range and resolution of points along each dimension
mu = linspace(0,mMu,muN);
tau = linspace(0,mTau,tauN);

rt = [3 4 4 4 4 5 5 6 6 7 8 9];

i=1;
lsurf = zeros(tauN,muN);
% nested loops across mu and tau
% calculate a joint likelihood for each parameter combination
for muloop=mu
    j=1;
    for tauloop = tau
        lsurf(j,i)=prod(exGaussPDF(rt,muloop, .1, tauloop));
        lnLsurf(j,i) = sum(log(exGaussPDF(rt,muloop, .1, tauloop)));
        j=j+1;
    end
    i=i+1;
end

%likelihood surface
colormap(gray(1)+.1)
mesh(tau, mu, lsurf);
xlabel('\tau (s)');
ylabel('\mu (s)');
zlabel('L(y|\theta)');
xlim([0 mTau]);
ylim([0 mMu]);

figure
%log-likelihood surface
colormap(gray(1)+.1)
mesh(tau, mu, lnLsurf);
xlabel('\tau (s)');
ylabel('\mu (s)');
zlabel('ln L(y|\theta)');
xlim([0 mTau]);
ylim([0 mMu]);