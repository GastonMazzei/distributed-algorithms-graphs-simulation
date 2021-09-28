import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/results-floodmax.pkl', 'rb') as f:
        results = pickle.load(f)

    # Prepare two axis
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.plot(results['N'], results['C'],label='Messages', c='k', ls=':')
    ax1.plot(results['N'], results['E'],label='Edges', c='k', ls='-')
    ax2.plot(results['N'],
         [results['C'][i]/results['E'][i] for i in range(len(results['E']))],label=r'$\frac{Messages}{Edges}$',
         c='r')
    ax2.scatter(results['N'],
         [results['C'][i]/results['E'][i] for i in range(len(results['E']))],
         c='r', s=40)
    ax1.set_ylabel('Number')
    ax2.set_ylabel('Quotient')
    ax2.set_ylim(1,15)
    plt.xlabel('Nodes')
    plt.legend()
    #plt.yscale('log')
    plt.show()
    







ax1.set_xlabel('X data')
ax1.set_ylabel('Y1 data', color='g')
ax2.set_ylabel('Y2 data', color='b')

plt.show()