import numpy as np
from scipy.special import binom

from rack import gen_rack, genfreqlist

def word_prob(word, charfreqdict, lenrack):
    letfreq = reduce(lambda x, y: x*y, map(lambda c: charfreqdict[c], word))
    overcounts = [sum([l==c for c in word]) for l in set(word)]
    fac = reduce(lambda x, y: x*y, overcounts)
    blah = letfreq * binom(lenrack, len(word)) * np.math.factorial(len(word))/fac
    return blah

def numerical_word_prob(word, numlist, lenrack, N=10000):
    num_racks_with_word = 0
    for i in xrange(N):
        testrack = gen_rack(lenrack, genfreqlist(numlist))
        def check_and_pop(word, testrack):
            for c in word:
                if c in testrack: 
                    testrack.remove(c)
                else:
                    return False
            return True

            
        #if reduce(lambda x, y: x and y, map(lambda c: c in testrack, word)):
        if check_and_pop(word, testrack):
            num_racks_with_word += 1
    return num_racks_with_word/float(N)
