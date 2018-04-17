# listing 5.2

## FITTING INDIVIDUAL PARTICIPANTS
weib_deviance <- function(x,rts){
    if (any(x<=0) || any(rts<x[1])){
        return(10000000)
    }
    likel <- dweibull(rts-x[1],shape=x[3],scale=x[2])
    dev <- sum(-2*log(likel))
}

res <- apply(dat,2,function(a) optim(c(100,255,1),
            function(x) weib_deviance(x,a)))

# Extract parameter estimates and put in to a matrix
parest <- matrix(
    unlist(lapply(res, function(x) x$par)),
    ncol=3, byrow=T)

print(colMeans(parest)) # mean parameter estimates
print(apply(parest,2,sd)) # SD of estimates