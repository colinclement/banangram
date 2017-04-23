"""
stats.py

author: Samuel Kachuck and Colin Clement
date: 2017-02-13

Methods for generating and analysing random lexicons.
"""

import random, itertools, string
import numpy as np
from bisect import bisect
from scipy.special import binom

from rack import gen_rack, genfreqlist
from graph import DirectedGraph, trie_to_dawg


def word_prob(word, charfreqdict, lenrack):
    """Analytically compute the probability that word appears in a rack from a
    language characterized by charfreqdict.

    Note: Haven't gotten this one worked out yet... DO NOT TRUST
    """
    letfreq = reduce(lambda x, y: x*y, map(lambda c: charfreqdict[c], word))
    overcounts = [sum([l==c for c in word]) for l in set(word)]
    fac = reduce(lambda x, y: x*y, overcounts)
    blah = letfreq * binom(lenrack, len(word)) * np.math.factorial(len(word))/fac
    return blah

def numerical_word_prob(word, numlist, lenrack, N=10000):
    """Numerically determine the probability that word occurs in a rack.
    """
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

def generate_uniform_rand_lexicon(nchars, nwords, avgwordlen=5):
    assert nchars <= 26, 'Currently only supports english characters'
    chars = 'abcdefghijklmnopqrstuvwxyz'[:nchars]

    lex = []
    for i in range(nwords):
        # Word lengths are distributed uniformly, with average avgwordlen
        wordlength = random.randint(1,avgwordlen*2-1)
        word = ''.join([random.choice(chars) for i in range(wordlength)])
        lex.append(word)

    lexstr = '\n'.join(lex)
    return lexstr

def generate_rand_lexicon(nchars, nwords, wordlenpdf=None):
    """
    Generate a random lexicon whose word lengths are distributed by function
    wordlenpdf.
    input:
        nchars: number of characters in lexicon
        nwords: number of words in lexicon
        wordlenpdf: a function
    """
    assert nchars <= 26, 'Currently only supports english characters'
    chars = 'abcdefghijklmnopqrstuvwxyz'[:nchars]

    if wordlenpdf is None:
        wordlenpdf = lambda x: np.repeat(5, x)

    lex = []
    for l in wordlenpdf(nwords):
        # Ensure the word length is an integer.
        wordlength = int(l)
        word = ''.join([random.choice(chars) for i in range(wordlength)])
        lex.append(word)

    lexstr = '\n'.join(lex)
    return lexstr

def generate_rand_dawg(nchars, nwords, wordlenpdf=None):
    """
    Generate a random DAWG whose word lengths are distributed by function
    wordlenpdf, using gnerate_rand_lexicon above.
    input:
        nchars: number of characters in lexicon
        nwords: number of words in lexicon
        wordlenpdf: a function

    """
    rand_lex = generate_rand_lexicon(nchars, nwords, wordlenpdf)
    G = DirectedGraph()
    G.parselex(rand_lex)
    trie_to_dawg(G)
    return G

def markov_branch_trans(N, alpha, beta=0.5):
    """Generate the transition matrix for a lexicon branch.
    input:
        N: number of characters in lexicon
        alpha: the probability that a word ends a branch
        beta: the probability that words end
    """
    P = np.zeros((2*N+1, 2*N+1)) 
    # N v_NW
    P[:N,:N] = (1.-beta)/N
    P[N:2*N,:N] = beta/N
    # N v_W
    P[:N, N:2*N] = (1.-alpha)*(1-beta)/N
    P[N:2*N, N:2*N] = (1.-alpha)*beta/N
    P[-1, N:2*N] = alpha
    # v_B
    P[-1,-1] = 1.

    return P
    

def markov_branch(P, N, wordlist=None):
    """Generate a single branch of a Markov lexicon, with transition matrix P.

    inputs:
        P: Transition matrix
        N: Number of characters in lexicon
        wordlist: The list of words already in lexicon (default empty list)
    """

    assert P.shape == ((2*N+1), (2*N+1))
    wordlist = wordlist or []

    # Initial state
    i = random.randint(0,N-1)
    branch = string.ascii_lowercase[i]
    v = np.zeros(2*N + 1)
    v[i] = 1.
    
    while True:
        # Compute transition probabilities for next state.
        v = P.dot(v)
        # Cumulative sums will aid in choosing next state.
        cumv = np.cumsum(v)
        
        # We choose a random number and look for which state corresponds.
        i = bisect(cumv, np.random.rand())

        # Update the state
        v *= 0
        v[i]=1.

        # Check if transition is nonword ending,
        if i<N:
            branch += string.ascii_lowercase[i]
        # word ending,
        elif N<=i<2*N:
            branch += string.ascii_lowercase[i-N]
            # (so add it to the wordlist)
            wordlist.append(branch)
        # or branch ending.
        else:
            return wordlist



def markov_word_trans(N, gamma=0.5):
    """Generate the transition matrix for a lexicon word.
    input:
        N: number of characters in lexicon
        gamma: the probability that words end
    """
    P = np.zeros((N+1, N+1))
    # N v_NW
    P[:N,:N] = (1.-gamma)/N
    P[-1,:-1] = gamma
    # v_W
    P[-1,-1] = 1.

    return P

def markov_word(P, N):
    """Generate a single word for a Markov lexicon, with transition matrix P.
    input:
        P: transition matrix (see markov_word_trans)
        N: number of characters
    """

    assert P.shape == (N+1,N+1)
    i = random.randint(0,N-1)
    word = string.ascii_lowercase[random.randint(0,N-1)]+string.ascii_lowercase[i]

    # Initial state
    v = np.zeros(N + 1)
    v[i] = 1.

    while True:
        # Compute transition probabilities for next state.
        v = P.dot(v)
        # Cumulative sums will aid in choosing next state.
        cumv = np.cumsum(v)
        #print cumv

        # We choose a random number and look for which state corresponds.
        i = bisect(cumv, np.random.rand())

        # Check if transition is nonword ending,
        if i<N:
            word += string.ascii_lowercase[i]
            v = np.zeros(N+1)
            v[i]=1.
        # or word ending.
        elif i == N:
            return word
