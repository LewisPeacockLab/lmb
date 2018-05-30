# hierarchical exponential forgetting model
model{
    # Priors for parent Distributions
    mualpha ~ dunif(0 ,1)
    taualpha ~ dgamma(epsilon, epsilon)
    mua ~ dunif(0,1)
    taua ~ dgamma(epsilon , epsilon)
    mub ~ dunif(0,1)
    taub ~ dgamma(epsilon , epsilon)

    # individual sampled parameters
    for (i in 1:ns){
        alpha[i] ~ dnorm(mualpha,taualpha)
        a[i] ~ dnorm(mua,taua)
        b[i] ~ dnorm(mub,taub)
    }
    
    # predictions for each subject at each lag
    for (i in 1 :ns){
        for (j in 1:nt){
            theta[i,j]<- a[i]+(1-a[i])*b[i]*exp(-alpha[i]*t[j])
        }
    }

    # observed data
    for (i in 1 :ns){
        for (j in 1:nt){
            k[i , j] ~ dbin(theta[i , j], n)
        }
    }
}