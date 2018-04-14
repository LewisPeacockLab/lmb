'''
Lewandowsky and Farrell, 2014, Chapter 2
Model of phonological loop.
Simulates decay for a list of words,
where words vary by speech-rate (how
long it takes to say each word).

* with error applied to decay rate
'''

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


# define parameters
N_REPS = 1000       # number of iterations
N_WORDS = 5         # per list
INIT_ACTIV = 1      # initial activation of items
MIN_ACTIV = 0       # minimum activation for recall
DECAY_RATE = .8     # per second
DECAY_SD = .2       #
DELAY_TIME = 5      # seconds

# choose various speech-rates
speech_rates = np.linspace(1.5, 4, 15)
# invert speech_rates to go from speech-rate to time-to-speak
speech_times = 1. / speech_rates
# create vector to hold results for each rate
accuracy = np.zeros_like(speech_rates)


'''Each loop runs through <N_REPS> iterations of
simulating the maintenance and rehearsal of a list 
of words, all of which take <t> seconds to say.
'''

i = 0 # counter used to save results

# for each hypothetical word length
for t in speech_times:

    # simulate repeatedly
    for r in range(N_REPS):

        # start each word in the list with the same activation value
        activations = np.repeat(INIT_ACTIV, N_WORDS)

        # apply sd to jitter the decay rate
        trial_decay_rate = DECAY_RATE + (np.random.normal()*DECAY_SD)

        '''Rehearsal is performed during the delay period (ie, now).
        To simulate rehearsal, the initial activation value is added
        back to the word. Only one word can be rehearsed at a time, and
        words are assumed to be rehearsed in the original list order.
        '''

        # simulate delay period
        rehearsal_word = -1 # allows rehearsal to start at beginning of list
        secs = 0
        while secs < DELAY_TIME:

            # get index of all words still above threshold
            # (ie, find words still in memory)
            intact = np.where(activations>MIN_ACTIV)[0]

            # find indx of the 'next' word that is still intact.
            # first get all words that follow current word
            next_words = np.where(intact>rehearsal_word)[0]
            if next_words.size == 0:
                # head back to beginning of word list
                rehearsal_word = 0
            else:
                # take the 'next' word
                rehearsal_word = next_words[0]

            # re-activate the item being rehearsed
            activations[rehearsal_word] = INIT_ACTIV
            
            # everything decays
            # according to the length of the current word
            activations = activations - (trial_decay_rate*t)
            secs += t
        
        # END of delay period

        # how many items are still in memory?
        n_correct = np.sum(activations>MIN_ACTIV)
        # save accuracy as percentage of whole word list
        accuracy[i] += (n_correct/N_WORDS)

    # END of iterations

    # increase counter to next word
    i += 1



# plot
plt.scatter(speech_rates, accuracy/N_REPS)
plt.xlim(0, 4.5)
plt.ylim(0, 1)
plt.xlabel('Speech Rate')
plt.ylabel('Proportion Correct')
plt.show()
