'''Lewandowsky and Farrell, Chapter 4

Visualizing the (log) likelihood surface plot of parameter estimation.
One plot is likelihood and other is log-likelihood.

This script includes the Ch4 matlab functions:
    - LSurfaceL.m
    - exGaussPDF.m

There might be some runtime errors about illegal divisions.
This same division happens in MATLAB but just
doesnt give warnings, so plots look the same.

### WARNING
### currently for some reason this only 
### runs from within ipython
### %run LSurfaceL.py
###
'''

from __future__ import division
import numpy as np
from scipy import stats
from scipy import special
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.ion()


# pick range and resolution of points along each dimension (ie, each parameter)
pmin = 0
pmax = 5
n_samples = 50 # per parameter
mu_list = np.linspace(pmin,pmax,n_samples)
tau_list = np.linspace(pmin,pmax,n_samples)

# make fake response time data (vector y in textbook)
rt = np.array([3,4,4,4,4,5,5,6,6,7,8,9])

# make an exponential normal (aka ex-Gaussian) distribution
def exGaussPDF(y, mu, sigma, tau):
    '''
    ARGS
        mu:     parameter for an ex-Gaussian pdf (mean)
        sigma:  parameter for an ex-Gaussian pdf (variance)
        tau:    parameter for an ex-Gaussian pdf (rate of exponential)
        y:      vector of RTs (ie, data)
    RETURNS
        dens:   a vector (same length as y) that holds the pdf _density_
                for each provided RT in y
    '''
    dens = (1/tau) * np.exp(((mu-y)/tau)+((sigma**2)/(2*tau**2)))*.5* \
        (1+special.erf((((y-mu)/sigma)-(sigma/tau))/np.sqrt(2)))
    return dens


## create likelihood and log-likelihood surfaces

# empties to fill
likeli_surf = np.empty([n_samples,n_samples])
loglikeli_surf = np.empty([n_samples,n_samples])

# nested loops to try each combination of parameters mu and tau
for i, mu in enumerate(mu_list):
    for j, tau in enumerate(tau_list):
        # get a density for each RT
        densities = exGaussPDF(rt, mu, .1, tau)
        ## here calculate _joint_ likelihoods
        # likelihood is the product of each independent density
        likeli_surf[i,j] = np.prod(densities)
        # after taking the log of _anything_, *products* become *sums*
        loglikeli_surf[i,j] = np.sum(np.log(densities))



## plotting

def plot(surface, title, zoom=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(mu_list, tau_list)
    surf = ax.plot_surface(X, Y, surface, alpha=0, linewidth=0.5, edgecolors='k')
    ax.set_xlim(pmin,pmax)
    ax.set_ylim(pmin,pmax)
    ax.set_xlabel(r'$\mu$ (s)')
    ax.set_ylabel(r'$\tau$ (s)')
    if title == 'likelihood surface':
        ax.set_zlabel(r'$L(y|\theta)$', fontsize=14)
    elif title == 'log-likelihood surface':
        ax.set_zlabel(r'$ln L(y|\theta)$', fontsize=14)
        if zoom:
            ax.set_zlim(-30,-20)
        # notice that when zooming in here it shows that 
        # the _pattern_ of ll and logll surfaces are the same
    else:
        ax.set_zlabel(r'$-ln L(y|\theta)$', fontsize=14)
        if zoom:
            ax.set_zlim(20,30)
    ax.set_title(title)
    ax.invert_xaxis() # just to make it look more similar to textbook fig4.9
    return ax

axl = plot(surface=likeli_surf, title='likelihood surface')
axll = plot(surface=loglikeli_surf, title='log-likelihood surface')
axnll = plot(surface= -loglikeli_surf, title='negative log-likelihood surface')
zoom_axll = plot(surface=loglikeli_surf, 
    title='log-likelihood surface', zoom=True)
zoom_axnll = plot(surface= -loglikeli_surf, 
    title='negative log-likelihood surface', zoom=True)


