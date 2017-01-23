"""
rack.py

Author: Samuel Kachuck
Date: 2017-01-22

For generating Banagram tiles.
"""
from __future__ import division

import random


BANNUMDICT = {'A':13, 
              'B':3, 
              'C':3, 
              'D':6, 
              'E':18, 
              'F':3, 
              'G':4, 
              'H':3, 
              'I':12, 
              'J':2, 
              'K':2,
              'L':5, 
              'M':3, 
              'N':8, 
              'O':11,
              'P':3, 
              'Q':2, 
              'R':9, 
              'S':6, 
              'T':9, 
              'U':6, 
              'V':3, 
              'W':3, 
              'X':2, 
              'Y':3, 
              'Z':2}

ALPH = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
        
        
