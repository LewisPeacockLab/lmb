'''Lewandowsky and Farrell, Chapter 4

SIMPLEserial model and variations

This script includes the Ch4 matlab functions:
    - SIMPLEserial.m
    - SIMPLEserialBinoPMF.m
    - SIMPLEmultinomialLnL.m
    - binomPMF.m

SIMPLEserial models the recall of a short list of words.

There are 3 SIMPLE models below, each with their own "thing".
'''


from __future__ import division
import numpy as np
import scipy.misc



def binomPMF(k, N, p):
    # could also use scipy.stats.binom()
    pMass = scipy.misc.comb(N,k) * p**k * (1-p)**(N-k)
    return pMass


def SIMPLEserial(c, presTime, recTime, J):
    '''
    ARGS
        c:          the single parameter of SIMPLE
        presTime:   time separating onset of words during encoding
        recTime:    time of separation during retrieval
        J:          the length of the list (ie, how many words?)
    RETURNS
        pcor:       the predicted proportion of correct responses at each position
    '''

    # presentation times (for each word)
    Ti = np.cumsum(np.repeat(presTime,J))
    # recall times
    Tr = Ti[-1] + np.cumsum(np.repeat(recTime,J))

    pcor = [] # to hold responses
    for i in range(J):
        # i indexes output + probe position

        # the temporal displacement of all 
        # words from the present word (i)
        M = np.log(Tr[i]-Ti)
        # similarity between present word and all others
        eta = np.exp(-c*abs(M[i]-M))
        # predicted proportion correct at present position
        pcor.append(1./sum(eta))

    return pcor





def SIMPLEserialBinoPMF(c, presTime, recTime, J, Nc, N):
    '''
    ARGS
        c:          the single parameter of SIMPLE
        presTime:   time separating onset of words during encoding
        recTime:    time of separation during retrieval
        J:          length of the list (ie, how many words?)
        Nc:         vector of n_words correctly recalled at each position
        N:          number of trials at each position
    RETURNS
        pmf:       the predicted proportion of correct responses at each position
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

    return pmf



def SIMPLEmultinomLnL(c, alpha, presTime, recTime, J, k):
    '''
    ARGS
        c:          a parameter of SIMPLE
        alpha:      a parameter of SIMPLE
        presTime:   time separating onset of words during encoding
        recTime:    time of separation during retrieval
        J:          length of the list (ie, how many words?)
        k:          a matrix where each row i corresponds to an output position,
                    and element j in the row gives number of times item j was
                    recalled at position i
    RETURNS
        lnL:        
    '''

    lnL = np.zeros([1,J])
    Ti = np.cumsum(np.repmat(presTime,1,J))
    Tr = Ti[-1] + np.cumsum(np.repmat(recTime,1,J))

    for i in range(J): # i indexes output + probe position
        M = np.log(Tr[i]-Ti)
        eta = np.exp(-c*abs(M(i)-M)**alpha)
        pall = eta/sum(eta)
        lnL[i] = sum(k[i,:] * np.log(pall))

    return lnL

