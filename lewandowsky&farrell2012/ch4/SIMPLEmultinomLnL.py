
from __future__ import division
import numpy as np

def SIMPLEmultinomLnL(c, alpha, presTime, recTime, J, k):
    '''
    ARGS
        c: a parameter of SIMPLE
        a: a parameter of SIMPLE
        presTime: time separating onset of words during encoding
        recTime: time of separation during retrieval
        J: length of the list (ie, how many words?)
        k: a matrix where each row i corresponds to an output position,
            and element j in the row gives number of times item j was
            recalled at position i
    RETURNS
        lnL: the predicted proportion of correct responses at each position
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