'''
listing 13.6 in python

This is a little different than the notebook.
It is more true to the actual listing (closer to a direct translation).
But I still think I changed some var names, which should be switched back.

'''


from __future__ import division

import numpy as np
import pandas as pd
from scipy.special import expit

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()


## 13.2.0

## Backpropogation

'''
Here we simulate a backpropogation model to learn regular and irregular English pronunciatino mappings.
'''

##### Listing 13.6

# num of units representing pattern stems that are 
# shared between regular and irregular inputs (eg, 'ave')
n_stem = 10
# num of units representing for the 'a' component that 
# differentiates different regular and irregular patterns
# (eg, 's' vs 'h' in 'save' vs 'have')
n_other = 20

n = n_stem + n_other # num of input units
h = 15 # num of hidden units
m = 30 # num of output units

## patterns the network will be trained on

# num of regular patterns the nw will be trained on
n_reg = 4
# num of irregular patterns the nw will be trained on
n_irreg = 1
# total num of patterns the network will be trained on
n_sets = 5
n_patterns = n_sets * (n_reg + n_irreg)

# num of training trials
n_train = 6000

eta = 0.1 # learning rate
mp = 0.9  # momentum parameter



# construct input and output patterns (ie, make the stims?)

inputs = np.empty([n_patterns,n])
outputs = np.empty([n_patterns,n])

i = 0
for train_set in range(n_sets):
    # each training set consists of a set of reg and irreg words

    # initialize stim vectors with 0s and 1s
    stem = np.random.randint(2,size=n_stem)
    train_out = np.random.randint(2,size=n)

    # regular
    '''The regular items all share the same output,
    and the irregular item has its own unique output.
    '''
    for w in range(n_reg):
        non_stem = np.random.randint(2,size=n_other)
        inp_patt = np.append(stem,non_stem)
        out_patt = train_out

        inputs[i,:] = inp_patt
        outputs[i,:] = out_patt
        i += 1


    # irregular
    for w in range(n_irreg):
        non_stem = np.random.randint(2,size=n_other)
        inp_patt = np.append(stem,non_stem)
        # make a new out stim bc irregular is inconsistent??
        train_out = np.random.randint(2,size=n)

        inputs[i,:] = inp_patt
        outputs[i,:] = train_out
        i += 1



## initialize weights and biases

# this one projects the input units to the hidden units
Wih = np.random.normal(size=[h,n]) * eta
# this one projects the hiddens units to the output units
Who = np.random.normal(size=[m,h]) * eta

# bias *vector* of the hidden layer
Bh = np.repeat(.01, h)
# bias *vector* of the output layer
Bo = np.repeat(.01, m)


## delta matrices
'''
These are the backpropagation part!
These will hold the delta values (error) to be passed
    back to the hidden units (so they know how they "did").
    I believe the network will try to minimize these!!!
'''
delta_Who = np.zeros_like(Who)
delta_Wih = np.zeros_like(Wih)


to_train = range(n_patterns)

# some empty stuff to hold results
error = np.zeros(n_train)
patt_err = np.zeros([n_patterns,n_train*n_patterns])
patts = np.zeros(n_train)
classes = np.zeros(n_train)


for sweep in range(n_train):

    ## which item to train?
    i = np.random.choice(to_train)

    cue = inputs[i,:]
    target = outputs[i,:]

    ## cue the network

    ## enter the hidden layer
    # dot product weight matrix with input
    net = np.dot( Wih, cue)
    # add bias term from all neurons of hidden layer
    net += Bh
    # get activation values from logistic function
    activation_hidden = expit(net)

    ## enter the output layer
    net = np.dot( Who, activation_hidden)
    net += Bo
    activation_output = expit(net)



    ## save performance
    rmsd = np.sqrt(np.mean((target-activation_output)**2))
    patt_err[i,sweep] = rmsd
    error[sweep] = rmsd
    patts[sweep] = i



    ### BACKPROPAGATION PART

    ## find the error in hidden-to-output weights
    delta_output = (target-activation_output) \
        * activation_output * (1-activation_output)
    delta_Who = eta * np.outer(delta_output,activation_hidden) \
        + mp * delta_Who

    ## find the error in input-to-hidden weights
    delta_hidden = np.dot(np.transpose(Who),delta_output) \
        * activation_hidden*(1-activation_hidden)
    delta_Wih = eta * np.outer(delta_hidden,cue) \
        + mp * delta_Wih

    ## update the weights and biases
    Who += delta_Who
    Wih += delta_Wih
    Bo += eta*delta_output
    Bh += eta*delta_hidden




