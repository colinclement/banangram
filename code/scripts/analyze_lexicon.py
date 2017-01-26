from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def charfreq(lexicon):
    if isinstance(lexicon, list):
        lexicon = ' '.join(lexicon)
    hist = defaultdict(int)
    total = 0
    for c in lexicon:
        if not c.isspace():
            hist[c] += 1
            total += 1
    return {c: float(hist[c])/float(total) for c in hist}
    

