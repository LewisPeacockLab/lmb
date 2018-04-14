model{
	#priors for discriminability and bias
	d ~ dnorm(1,1)
	b ~ dnorm(0,1)
	
	#express as areas under the curve
	phih = phi(d/2-b) #normal cdf
	phif = phi(-d/2-b)
	
	#observed hits and false alarms
	h ~ dbin(phih,sigtrials)
	f ~ dbin(phif,noistrials)
}