"""
randomlexicon.py

author: Colin Clement
date: 2017-01-23

Functions for generating random lexica, racks

"""

import random

def generate_random_lexicon(L, N, chars = ['0','1']):
    """ Generate N random 'words' of length L from chars """
    pop = reduce(lambda x, y: x+y, [[c for i in range(L)] for c in chars])
    words = [reduce(lambda x, y: x+y, random.sample(pop, L)) for i in range(N)]
    return ' '.join(words)
