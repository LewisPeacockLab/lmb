'''
Messing around with chapter 7
'''

from __future__ import division
import numpy as np
import pandas as pd
from scipy import stats

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()
sea.set_style('whitegrid')



'''
Important to separate out the Markov Chain Monte Carlo part on its own.

The first MC refers to the non-memory part.

The second MC part refers to doing it a lot.

Then there are methods or _versions_ of this, like Metropolis-Hastings.

Here, rather than deriving the posterior analytically, we brute-force
_make_ a distribution of samples, and use that as ourposterior.

Importantly, here, posterior doesn't refer to the result, but the disrtibution 
that is used to asquire the result....???

That is, this way we avoid writing down/deriving that equation for the posterior.


Here, we still have the right-hand side of Bayes equation, but we dont have to 
do all the derivation.


BUT, we dont actually need the denominator. Remember it was a scaling factor, 
and so we drop it, and change = to proportionality.

$$ bayes theorem $$

$$ proportionality version $$

So now all we need is the prior (which we will always be formulating in bayesian inference),
and the likelihood. Then we take shit ton of samples.

Now our results wont neceasdilry be between 0 and 1, but we will interpret
them in relation to each other by comparing models.


WHAT is a markov chain?


'''

'''MH-MCMC

1. take a guess at the parameter value
2. add random (normal) noise
3. accept (and move on) or reject ()
4. repeat


'''


'''MCMC-specific TERMINOLOGY'''
# TARGET distribution is the posterior distribution (the one we are attemting to model)

# lets say we are interested in a normal like the book

chain = np.zeros(5000)

obs_val = 144
known_sd = 15

tune_sd = 2

# starting guess
chain[0] = 150


## NOTE we are doing parameter simulation?? for the mean of normal
## bc we kjnkow the Standard deviation of it.
## we just dont know the mean, but we have one sample to help us


for i in range(1,5000):
    
    # grab current value (Markov Chains have memory of 1-back)
    curr_mu = chain[i-1] # guessing MU (book calls this current)

    # propose new value (PROPOSING MU) by adding noise
    prop_mu = curr_mu + stats.norm(0,tune_sd).rvs(1)

    ## decide what to do

    # compare density of proposal and observed value (data)

    ## WE are taking the DENSITY of the observed value
    ## AT bothe the proposal and the previous iteration
    ## **we are not using the observed as the mean**
    curr_dens = stats.norm(curr_mu,known_sd).pdf(obs_val)
    prop_dens = stats.norm(prop_mu,known_sd).pdf(obs_val)

    # we want to keep the proposed value if the new density is higher
    # ie, if the probability of the data coming from a distribution with that mu
    # is higher than the previous one
    if prop_dens > curr_dens:
        # accept
        chain[i] = prop_mu
    else:
        # accept it on probabilistc terms
        llratio = prop_dens/curr_dens
        if np.random.uniform() < llratio:
            # accept
            chain[i] = prop_mu
        else:
            # reject (just keep current)
            chain[i] = curr_mu



# figure 7.1

x = np.linspace(100,200,1000)

### make this a function so we can use it later below


fig, (ax1,ax2) = plt.subplots(1,2)

# plot "true" normal distribution centered at 144
y = stats.norm(obs_val,known_sd).pdf(x)
ax1.plot(x,y,c='black',label='Normal PDF')

# plot observed
sea.kdeplot(chain, c='blue', label='All MCMC', ax=ax1)
sea.kdeplot(chain[1000:], c='green', label='Excluding burnin', ax=ax1)

ax2.plot(chain)

def title_chain_plots(ax1,ax2):
    ax1.set_title('Posterior derived from MCMC sampling')
    ax1.set_xlabel('Sampled values of mu')
    ax1.set_ylabel('Density')
    ax2.set_title('Accepted values across all chains')
    ax2.set_xlabel('Iteration (chain)')
    ax2.set_ylabel('Value of accepted sample')

title_chain_plots(ax1,ax2)

## do panels and c, or just make it interactive!!! do that.


'''
USING better than uniform priors

The book has a nice exaqmple here.
Walk through it bc te description of th sitautio is useful.
Just adds a normal rather than uniform prior.

'''

for i in range(1,5000):
    
    curr_mu = chain[i-1]
    prop_mu = curr_mu + stats.norm(0,tune_sd).rvs(1)

    curr_dens = stats.norm(curr_mu,known_sd).pdf(obs_val)
    prop_dens = stats.norm(prop_mu,known_sd).pdf(obs_val)

    # add the prior aspect here
    # this adjust each dens by its relation to the prior
    curr_dens *= stats.norm(prior_mu,prior_sd).pdf(obs_val)
    prop_desn *= stats.norm(prior_mu,prior_sd).pdf(obs_val)


    if prop_dens > curr_dens:
        # accept
        chain[i] = prop_mu
    else:
        # accept it on probabilistc terms
        llratio = prop_dens/curr_dens
        if np.random.uniform() < llratio:
            # accept
            chain[i] = prop_mu
        else:
            # reject (just keep current)
            chain[i] = curr_mu









## 7.2 Estimating multiple parameters.


'''
1. show what a mixture distribution is
- interactive plot, but the math behind the combinatinow of uniform and mnormal

2. fake the data and plot it
3. do the mixture stuff










