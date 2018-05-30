
from __future__ import division
import numpy as np
import scipy.misc



def binomPMF(k, N, p):
    # could also use scipy.stats.binom()
    pMass = scipy.misc.comb(N,k) * p**k * (1-p)**(N-k);
    return pMass

def SIMPLEserialBinoPMF(c, presTime, recTime, J, Nc, N):
    '''
    ARGS
        c: the single parameter of SIMPLE
        presTime: time separating onset of words during encoding
        recTime: time of separation during retrieval
        J: length of the list (ie, how many words?)
        Nc: number of words correctly recalled at each position
        N: number of trials at each position
    RETURNS
        pcor: the predicted proportion of correct responses at each position
    '''

    # presentation times (for each word)
    Ti = np.cumsum(np.repeat(presTime,J))
    # recall times
    Tr = Ti[-1] + np.cumsum(np.repeat(recTime,J))

    pmf = [] # to hold responses
    for i in range(J):
        # i indexes output + probe position

        # the temporal displacement of all 
        # words from the present word (i)
        M = np.log(Tr[i]-Ti)
        # similarity between present word and all others
        eta = np.exp(-c*abs(M[i]-M))
        # predicted proportion correct at present position
        pcor = (1./sum(eta))
        pmf.append(binomPMF(Nc[i], N, pcor))

    return pcor