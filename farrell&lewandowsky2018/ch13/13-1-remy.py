'''
Walking through section 13.1

(doesn't include last part about lesions)
'''


from __future__ import division

import numpy as np
import pandas as pd
from scipy.spatial import distance

import seaborn as sea
import matplotlib.pyplot as plt; plt.ion()


## 13.1

#### 13.1.1 The Hebbian Associator

'''
##### Let's get formal...

The **_input_** layer is a vector, **c** (c stands for cue).

The activation of a particular unit $j$ of the input layer is referred to as $c_j$.

The **_output_** layer is vector **o**, where each unit $i$ is $o_i$.

All the units of the input layer are connected to all the units of the output layer. Therefore, the weight matrix **W** contains all the connections between input unit $j$ and output unit $i$ located at $W_{ij}$.

That is, each row $i$ of the matrix contains those weights projecting from input unit $c_j$ to output unit $o_i$.
'''

'''
We "learn" the weight matrix by providing the model with the input and output layers.

In a simple model, when the network is cued (a stimulus is presented as a cue for the associated response), each output unit determines its activation by taking a weighted sum o the inputs.

$$ o_i = \sum_{j} W_{ij}c_{j} $$

All we are doing here is taking each input activation $c_j$ and multiplying it by the weight from input unit $j$ to output unit $i$, and adding up the resulting weighted activations.

**This equation gets applied to each input unit $j$** (note the sum). This is assumed to happen in parallel.

This is one of the most simple activation functions. It is linear.
'''


'''
Learning involves modifying the weights so as to produce the correct response.

We can choose learning rules.

Of course, the Hebbian learning rule is very common, and this is a very simple rule.

Cells that fire together, wire together.

Formally, this means that the change in the weight between input unit $j$ and output unit $i$ is the product of the two activations.

$$ \delta W_{ij} = c_{j} o_{i} $$

where $\delta$ denotes a change in the weight matrix between time $t$ and time $t+1$, so that $ W_{ij}(t+1) = W_{ij}(t) + \delta W_{ij} $.

Usually the updating of the weights will be controlled by a learning rate $\alpha$ that determines how much a stored association modifies the existing weights.

$$ \delta W_{ij} = \alpha c_{j} o_{i} $$

'''

##### listing 13.1


# stimulus
c = np.array([
    [ 1, -1,  1, -1 ], # word 1
    [ 1,  1,  1,  1 ], # word 2
    ])

# response
o = np.array([
    [ 1,  1, -1, -1 ], # response 1
    [ 1, -1, -1,  1 ], # response 2
    ])


# characteristics of the network

n = 4 # num of input units
m = 4 # num of output units

W = np.zeros([m,n])

alpha = 0.25



# learning

# iterate over stimuli/response combinations
for stim in range(2):

    # iterate over output units
    for i in range(n):
        # iterate over input units
        for j in range(m):

            W[i,j] += alpha * c[stim,j] * o[stim,i]


# test phase
# FIRST STIMULUS ONLY

# this output layer should match the first row of o

o_resp1 = np.zeros(m)

for i in range(m):
    for j in range(n):
        o_resp1[i] = o_resp1[i] + W[i,j]*c[0,j]



# absolute values might differ, so measure similarity using cosine similarity
orig_resp = o[0,:]

cos_similarity = 1 - distance.cosine(orig_resp,o_resp1)

'''
There are other options, like Euclidian distance, or normalizing the vectors or alpha parameter.
'''




#### 13.1.2 Hebbian Models as Matrix Algebra




'''
dot product == inner product

$$ x \odot y = x^{T} y = \sum_{i} x_{i} y_{i} $$

NOTE this is like the original weight matrix equation.

We just take the dot product between each input and output layer.

We also use multiplication to describe learning in the Hebbian model.

The change in weights, 􏰗**$ \delta W $**, is given by the outer product of the two vectors being associated:

$$ o \otimes c = oc^{T} $$

Outer product provides a matrix rather than scalar from inner product.


**We can now efficiently express learning as the formation of outer products, and retrieval as formation of inner products.**

'''


'''
Cool now we will build a neural network model of cued recall.

Importantly, watch how the model will now be abl to generalize to new stims that were not used in training. When encountering unseen stims, the model should produce something approximating the originally learned response to the similar stim.
'''

##### first, get weight matrix as above but with linear algebra


# learning
W2 = np.zeros([m,n])
for stim in range(2):
    W2 += np.outer(o[stim,:], c[stim,:])


# test phase
# FIRST STIMULUS ONLY

# this output layer should match the first row of o
stim1 = c[0,:]
oresp1_2 = np.dot(W2,stim1)




##### listing 13.2


n = 100 # num of input units
m = 50  # num of output units

# Each learning set is specified to comprise 20 pairs
list_length = 20 # num of pairs in each list

# how many trials to simulate
n_reps = 100

alpha = 0.25

# we will iterate across stim set combinations of varying similarity
# (0 is completely dissimilar, 1 is completely similar)
stim_sim_list = np.array([ 0, .25, .5, .75, 1])

# to store results
accuracy = np.zeros(len(stim_sim_list))


# iterate over independent trials
for i in range(n_reps):

    # initialize empty weight matrix
    W = np.zeros([m,n])

    ## CREATE STUDY SET
    ## think of stim1 and resp1 as the TRAINING SET
    ## and then stim2 as TEST SET to estimate hypothetical resp2

    # build lists of stims and responses
    # (these are the c and o vectors)
    ## I HAVE CHANGED THE USE OF VARIABLE STIM -- BADDDDDD
    stim1_list = [ np.random.choice([1,-1],size=n) for stim in range(list_length) ]
    resp1_list = [ np.random.choice([1,-1],size=m) for resp in range(list_length) ]

    ## STUDY THE LIST
    for item in range(list_length):
        c = stim1_list[item]
        o = resp1_list[item]
        W += alpha * np.outer(o,c)


    ## LOOP OVER PROBE STIMS OF DIFFERING SIMILARITIES WITH THE TRAINED STIMS
    ## AND USE THESE TO PROBE FOR RESPONSES
    for ss_count, stim_sim in enumerate(stim_sim_list):

        ## CREATE TEST STIMULI WITH CURRENT SIMILARITY
        stim2_list = []
        for item in range(list_length):

            svec = np.random.choice([1,-1],size=n)
            mask = np.random.uniform(size=n) < stim_sim

            stim2 = mask*stim1_list[item] + (1-mask)*svec
            stim2_list.append(stim2)

        ## TEST THE NEW STIM LIST
        total_acc = 0
        for item in range(list_length):
            c = stim2_list[item]
            o = np.dot(W,c)

            # compare with original response
            similarity = 1 - distance.cosine(o,resp1_list[item])
            total_acc += similarity

        accuracy[ss_count] += total_acc / list_length




plt.plot(stim_sim_list,accuracy/n_reps,marker='o',ms=5)

plt.xlabel('Stimulus-Cue Similarity')
plt.ylabel('Cosine')
plt.title('figure 13.4, generalization in the Hebbian model')



##### 

