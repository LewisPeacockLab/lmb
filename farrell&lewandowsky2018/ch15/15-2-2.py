'''
15.2.2 - Neuroscience of Reinforcement Learning
'''

from __future__ import division

import numpy as np
import pandas as pd

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()


N_TRIALS = 40
N_STEPS = 25     # number of time steps in each trial
STIM_STEP = 5    # time step at which stimulus (CS) is presented
REWARD_STEP = 25 # time step at which reward is presented

# a matrix to record the deltas
delta_results = np.zeros([N_TRIALS,N_STEPS]) # (alld)

# w tracks the expected reward FOR EACH STEP/TIMEPOINT
w = np.zeros(N_STEPS+1)

GAMMA = 1
ALPHA = 0.5

for trial in range(N_TRIALS):

    # to save all step results from a single trial, and update w with
    sumd = np.zeros(N_STEPS+1)

  
    for step in range(N_STEPS):

        '''
        To make the temporal difference, we need
        x(t) and x(t+1). These are vectors of 0s, where
        a 1 marks how long it's been, and so shifts over
        for each step.
        Note the "-1" is for python indexing.
        '''
        x = np.zeros(N_STEPS+1)
        if step > STIM_STEP-1:
            x[step-STIM_STEP] = 1

        x1 = np.zeros(N_STEPS+1)
        if ((step+1) > STIM_STEP-1):
            x1[step+1-STIM_STEP] = 1
        
        # if it is the last step, we get a reward
        r = 1 if step==REWARD_STEP-1 else 0
        
        '''
        Calculate reward PREDICTIONS for t and t+1.
        Here, np.sum(w*1) serves to add across all the reward values
        that recieved 1s in them in the lines above. Ie, the two
        timepoints x and x1.
        '''
        Vt = np.sum(w*x)
        Vt1 = np.sum(w*x1)
        
        # calculate prediction error
        delta_t = r + GAMMA*Vt1 - Vt
    
        # this is just record keeping, to track prediction errors
        # (we'll plot this later)
        delta_results[trial,step] = delta_t
    
        # this is the sum of prediction errors across t that is used 
        # to update w at the end of the trial
        sumd += x*delta_t


    # update the final weights of this trial, including application of learning rate
    w += ALPHA * sumd




'''
Plot results
(Figure 15.6)
'''

ax = plt.subplot()

for sp in [0,11,24,39]:
    plt.plot(delta_results[sp,:],label=sp+1)

plt.legend(title='Trial')
plt.ylabel('Prediction Error')
plt.xlabel('Time step')
plt.title('Prediction error in a temporal difference model\nat different stages of learning')

