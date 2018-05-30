'''
15.2.1 - THeories of Reinforcement Learning

"The basic assumption of reinforcement learning is that 
an agent (e.g., a rat or human) learns to attach values 
to states of the environment, actions, or combinations 
of states and actions."

"Let’s start off with the simplest case where an agent 
learns about the values attached to actions."

Here in this example:
We setup an agent/subject who must repeatedly decide 
between 2 different actions.
They make a decision each trial, and their reward 
predictions get updated according to the reward from
each (previous) trial.
'''

from __future__ import division

import numpy as np
import pandas as pd

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()


'''
Choose some model parameters.

Epsilon is the probability that the agent chooses
the action randomly, and so epsilon-1 is the 
probability that the agent is "greedy" and takes 
the action that offers the highest reward.

Alpha is the learning rate.
'''

N_TRIALS = 1000 # per run
N_RUNS = 1000

EPSILON = 0.1
ALPHA = 0.1



'''
Each of 2 possible actions (or "arms") has a reward value.
These reward values are picked from normal distributions
with their own mean and std.
We pick them here, and build a dataframe that holds them.
Again, this dataframe will hold the TRUE reward values 
for each trial, which are the same for each run.
'''

REWARD_PARAMS = dict(
    action1= {'mu':5,   'sd':1},
    action2= {'mu':5.5, 'sd':1},
    )

reward_action1 = np.random.normal(
    REWARD_PARAMS['action1']['mu'],
    REWARD_PARAMS['action1']['sd'], size=[N_TRIALS,1])   # (r1)
reward_action2 = np.random.normal(
    REWARD_PARAMS['action2']['mu'],
    REWARD_PARAMS['action2']['sd'], size=[N_TRIALS,1])   # (r2)
reward_vals = np.hstack([reward_action1,reward_action2]) # (r)



'''
Build a structure to save results.

Each run will save all the results from individual trials,
and then add them to this array. So it ends up being a linear
combination of results from all runs.
'''

q_results = np.zeros_like(reward_vals) # (Qrecord)



'''
What will happen is the subject will make a reward PREDICTION
each trial, and the error will be relative to these TRUE values.
'''

for run in range(N_RUNS):

    '''
    q refers to reward value.
    In this case, it represents the agent's estimate of how much
    it will be rewarded for all the possible actions it could take.
    There are only 2 arms/actions, so q has 2 columns.
    It gets initialized with random reward values for the run.
    They start as random reward values, then get updated within
    a run as the subject chooses actions and gets rewards.
    '''
    # the EXPECTED reward, which will accumulate over trials
    cum_q = np.random.normal(0,.001,size=2) # (Q)

    # to hold results (see above description)
    q_run_results = np.zeros_like(reward_vals) # (QthisRun)


    for trial in range(N_TRIALS):

        # person first chooses an action
        if np.random.rand() < EPSILON:
            # random action selection
            action_num = np.random.randint(2)
        else:
            # greedy selection (that with highest reward)
            action_num = np.where(cum_q==cum_q.max())[0][0]

        # learn from the reward, and apply the learning rate
        prediction_error = ALPHA*(reward_vals[trial,action_num]-cum_q[action_num])
        # update the reward values for this RUN by adding them
        cum_q[action_num] += prediction_error
        # save the current trial prediction error BEFORE it gets updated again
        q_run_results[trial,:] = cum_q


    # save results by adding them together from each run (so final Q is linear combo of all run Qs)
    q_results = q_results + q_run_results



plt.plot(q_results[:,0]/N_RUNS, label='5')
plt.plot(q_results[:,1]/N_RUNS, label='5.5')
plt.legend(title='mean of reward value')
plt.title('Learning of a reinforcement action model')
plt.ylabel('Mean Q')
plt.xlabel('Trial')

