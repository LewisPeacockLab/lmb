'''Lewandowsky and Farrell, Chapter 3

Sequential plot showing steps of parameter estimation.

This script includes all the matlab functions from Chapter 3:
    - getregpred.m
    - wrapper4fmin.m
    - bof

Running...
$ python parameter_estimation.py

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


def getregpred(parms,data):
    '''get REGRESSION prediction
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
    print 'Parameters (x,y): ({:.04f},{:.04f})'.format(parms[0],parms[1])
    print 'RMSD: {:.05f}'.format(rmsd)
    return rmsd

def wrapper4fmin(pArray,data):
    x, fVal = scipy.optimize.fmin(func=bof, x0=pArray)
    return x, fVal

# plot current predictions and data
def plot(data, preds):
    '''Called from within getregped() to display progress.
    '''
    plt.cla()
    plt.plot(data[:,1], data[:,0], 'o', color=[0.4, 0.4, 0.4], markeredgecolor='black')
    plt.plot(data[:,1], preds, linestyle='--');
    plt.xlim([-2, 2])
    plt.ylim([-2, 2])
    plt.xlabel('X', fontsize=18)
    plt.ylabel('Y', fontsize=18)
    plt.xticks([-2,2])
    plt.yticks([-2,2])
    plt.pause(.5)



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


## use fmin (and RMSD) to estimate parameters
startParms = [-1., .2]
finalParms, finDiscrepancy = wrapper4fmin(startParms,data)


## print this at the end for comparison
print 'Original regression equation parameter estimation was: ' \
    + '({:.04f}, {:.04f})'.format(b[1], b[0])

