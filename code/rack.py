"""
rack.py

Author: Samuel Kachuck
Date: 2017-01-22

For generating Banagram tiles.
"""
from __future__ import division

import random


BANNUMDICT = {'a':13, 
              'b':3, 
              'c':3, 
              'd':6, 
              'e':18, 
              'f':3, 
              'g':4, 
              'h':3, 
              'i':12, 
              'j':2, 
              'k':2,
              'l':5, 
              'm':3, 
              'n':8, 
              'o':11,
              'p':3, 
              'q':2, 
              'r':9, 
              's':6, 
              't':9, 
              'u':6, 
              'v':3, 
              'w':3, 
              'x':2, 
              'y':3, 
              'z':2}

ALPH = 'abcdefghijklmnopqrstuvwxyz'

numlist = [BANNUMDICT[l] for l in ALPH]

def cumsum(iterable):
    total = 0
    for x in iterable:
        total += x
        yield total

def genfreqlist(numlist):
    Ntiles = sum(numlist)
    return [i/Ntiles for i in cumsum(numlist)]

def findlowest(x, iterable):
    for i, n in enumerate(iterable):
        if x < n:
            return i

def select_with_replacement(freqlist):
    return ALPH[findlowest(random.random(), freqlist)]

def select_without_replacement(freqlist, numlist):
    ind = findlowest(random.random(), freqlist)
    altnumlist = [n for n in numlist]
    foundword = False
    while not foundword:
        if altnumlist[ind]:
            altnumlist[ind] -= 1
            altfreqlist = genfreqlist(altnumlist)
            foundword = True
            return ALPH[ind], altfreqlist, altnumlist

def gen_rack(n, freqlist, numlist=None, replace=True):
    if replace:
        rack = [select_with_replacement(freqlist) for i in range(n)]
    else:
        assert numlist
        assert n < sum(numlist)
        rack = []
        altnumlist = [i for i in numlist]
        altfreqlist = [f for f in freqlist]
        for i in range(n):
            l, altfreqlist, altnumlist = select_without_replacement(freqlist, altnumlist)
            rack.append(l)
    return rack
        
        
