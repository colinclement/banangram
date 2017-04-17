"""
stats.py

author: Samuel Kachuck and Colin Clement
date: 2017-02-13

Methods for generating and analysing random lexicons.
"""

import random, itertools
import numpy as np
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

def generate_markov_lexicon(nchars, maxwordlength=10, prob=0.5):
    """
    Generate a random lexicon for which 
    """
    assert nchars <= 26, 'Currently only supports english characters'
    chars = 'abcdefghijklmnopqrstuvwxyz'[:nchars]

    lex = []
    for wordlength in range(1, maxwordlength):
        for word in itertools.combinations_with_replacement(chars, wordlength):
            if random.random() < prob:
                lex.append(''.join(word))

    lexstr = '\n'.join(lex)
    return lexstr
