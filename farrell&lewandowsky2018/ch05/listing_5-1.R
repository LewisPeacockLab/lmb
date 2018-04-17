# listing 5.1

nsubj <- 30
nobs <- 20
q_p <- c(.1, .3, .5, .7, .9)

shift <- rnorm(nsubj,250,50)
scale <- rnorm(nsubj,200,50)
shape <- rnorm(nsubj,2,0.25)

params <- rbind(shift,scale,shape)

print(rowMeans(params))

# rows are participants, columns are observations
dat <- apply(params, 2, function(x) rweibull(nobs,shape=x[3],scale=x[2])+x[1])

# calculate sample quantiles for each participant
kk <- apply(dat, 2, function(x) quantile(x,probs=q_p))

## FITTING VIA QUANTILE AVERAGING
# average the quantiles
vinq <- rowMeans(kk)

# fit the shifted Weibull to averaged quantiles
weib_qdev <- function(x,q_emp,q_p){
    if (any(x<=0)){
        return(10000000)
    }
    q_pred <- qweibull(q_p,shape=x[3],scale=x[2])+x[1]
    dev <- sqrt(mean((q_pred-q_emp)^2))
}

res <- optim(c(225,225,1),
            function(x) weib_qdev(x,vinq,q_p))

print(res)