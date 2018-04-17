function dens = exGaussPDF(y, mu, sigma, tau)

dens = (1./tau).*...
    exp(((mu-y)./tau)+((sigma.^2)./(2.*tau.^2))).*.5.*(1+erf((((y-mu)./sigma)-(sigma./tau))./sqrt(2)));