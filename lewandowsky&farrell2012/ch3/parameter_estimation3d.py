'''Lewandowsky and Farrell, Chapter 3

Sequential plot showing steps of parameter estimation.

This script includes all the matlab functions from Chapter 3:
    - getregpred.m
    - wrapper4fmin.m
    - bof

Running...
$ python parameter_estimation3D.py

...will plot the sequential process of estimating parameters with fmin.
wrapper4fmin takes some starting parameters and then evaluates
and passes to bof() for evaluation. bof() returns the RMSD as an evaluation
of those parameters. The script stops after RMSD stops "bouncing around".

It will print out the current parameters and RMSD evaluation
of those parameters as it is moving around the plots.
'''

from __future__ import division
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.ion()

def getregpred(parms,data):
    '''get REGression prediction
    Called by discrepancy function (here, bof).
    Takes in current parameters and data, 
    and returns predictions from the regression
    line. The predictions are used by the 
    disrepancy function (bof) to calculate RMSD.
    '''
    b1 = parms[0]
    b0 = parms[1]
    # predict the data with these new parameters
    preds = b0 + b1*data[:,1]
    plot(data, preds)
    return preds

def bof(parms):
    '''The discrepancy function called 
    from _within_ fmin to evaluate the parameters.
    Here it returns the RMSD of the parameters,
    but could use an alternate evaluation.
    '''
    predictions = getregpred(parms, data)
    sd = (predictions-data[:,0])**2
    rmsd = np.sqrt(np.sum(sd)/sd.size)
    plot_3dpoint(b0=parms[1],b1=parms[0],rmsd=rmsd)
    print 'Parameters (x,y): ({:.04f},{:.04f})'.format(parms[0],parms[1])
    print 'RMSD: {:.05f}'.format(rmsd)
    return rmsd

def wrapper4fmin(pArray,data):
    x, fVal = scipy.optimize.fmin(func=bof, x0=pArray)
    return x, fVal

# plot current predictions and data
ax2 = plt.subplot()
def plot(data, preds):
    '''Called from within getregpred() to display progress.
    '''
    ax2.cla()
    ax2.plot(data[:,1], data[:,0], 'o', color=[0.4, 0.4, 0.4], markeredgecolor='black')
    ax2.plot(data[:,1], preds, linestyle='--');
    ax2.set_xlim([-2, 2])
    ax2.set_ylim([-2, 2])
    ax2.set_xlabel('X', fontsize=18)
    ax2.set_ylabel('Y', fontsize=18)
    ax2.set_xticks([-2,2])
    ax2.set_yticks([-2,2])
    # plt.pause(.5)

def plot_3dpoint(b0, b1, rmsd):
    g, = ax.plot([b1],[b0],[rmsd], markersize=10, color='g', marker='o')
    plt.pause(0.5)
    g.remove()



## generate simulated data

n_data_pts = 20
rho = .8
intercept = .0

# random variable a is from a standard normal distrn
data_rv_a = np.random.normal(size=[n_data_pts])
# random variable b is correlated (rho) with random variable a
data_rv_b = np.random.normal(size=[n_data_pts])*np.sqrt(1-rho**2) + (data_rv_a*rho) + intercept
# stack them into a single array
data = np.hstack([data_rv_b.reshape(-1,1), data_rv_a.reshape(-1,1)])


## do conventional regression analysis

# make design matrix X for lin regr matrix formula
X = np.hstack([np.ones(n_data_pts).reshape(-1,1), data[:,1].reshape(-1,1)])
y = data[:,0]
b = np.linalg.lstsq(X,y)[0]


# plot the surface before starting parameter search
# both around 0
b0_list = np.linspace(-5,5,50)
b1_list = np.linspace(-5,5,50)
def make_surface():
    # one time
    surface = np.empty([50,50])
    for i, b0 in enumerate(b0_list):
        for j, b1 in enumerate(b1_list):
            predictions = b0 + b1*data[:,1]
            sd = (predictions-data[:,0])**2
            rmsd = np.sqrt(np.sum(sd)/sd.size)
            surface[i,j] = rmsd
    return surface

def draw_surface(surface):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(b0_list, b1_list)
    surf = ax.plot_surface(X, Y, surface, alpha=0, linewidth=0.5, edgecolors='k')
    ax.set_xlim(b0_list.min(),b0_list.max())
    ax.set_ylim(b1_list.min(),b1_list.max())
    ax.set_xlabel('b0')
    ax.set_ylabel('b1')
    ax.set_zlabel('RMSD')
    ax.set_title('regression parameter surface')
    ax.invert_xaxis() # just to make it look more similar to textbook fig4.9
    return ax


## initiate the surface plot
surface = make_surface()
ax = draw_surface(surface=surface)

## use fmin (and RMSD) to estimate parameters
startParms = [-3., 3.]
finalParms, finDiscrepancy = wrapper4fmin(startParms,data)

## print this at the end for comparison
print 'Original regression equation parameter estimation was: ' \
    + '({:.04f}, {:.04f})'.format(b[1], b[0])








