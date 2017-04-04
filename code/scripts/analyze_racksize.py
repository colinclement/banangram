import cPickle as pkl
import numpy as np
import matplotlib.pyplot as plt

def successrate(lst):
    report = 0
    for g in lst:
        if g['solution']:
            report += 1
    return float(report)/float(len(lst))

sizedict = pkl.load(open('../../data/2016-01-26-racksize-data.pkl', 'r'))

p = np.array([successrate(sizedict[k]) for k in sizedict])
branches = np.array([[f['branches'] for f in sizedict[k]] for k in sizedict])

fig0, ax0 = plt.subplots()
ax0.plot(sizedict.keys(), p, '-o')
ax0.set_xlabel('Rack size')
ax0.set_ylabel('P(solution)') 

fig1, ax1 = plt.subplots()
for b, k in zip(branches, sizedict):
    if k % 2 == 0:
        ax1.hist(b, bins=50, histtype='step', normed=True,
                 label=str(k))
ax1.legend()
ax1.set_title('Branch count for branch limit = 100000')
ax1.set_xlabel('Branch count')
ax1.set_ylabel('Density of branch counts')

plt.show()

