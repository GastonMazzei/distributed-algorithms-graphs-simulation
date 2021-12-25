import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/SynchBFS/results-synchbfs.pkl', 'rb') as f:
        results = pickle.load(f)

    # Prepare the plots and variables
    p = str(round(results['P'][0]*100,0))
    fig, ax = plt.subplots(1,2,figsize=(15,10))
    E = np.asarray(results['E'])
    C = np.asarray(results['C'])
    N = np.asarray(results['N'])
    D = np.asarray(results['D'])

    # Plot raw  data on axis 0 
    ax[0].plot(N, E, label='Edges', c='r',lw=4,alpha=0.5, ls='-')
    ax[0].plot(N, C, label='Messages', c='k',lw=4,alpha=0.8, ls=':')
    
    # Plot the relevant dependency on axis 1, as its 
    # Communication ~ Edges (p.58 Distributed  Algorithms, Nancy Lynch)
    y = E
    ax[1].scatter(C,y, c='y', label='Edges', alpha=1)
    pol = np.polyfit(C,y,1)
    ax[1].plot(C, np.polyval(pol,C), label='linear fit', c='k', lw=3, alpha=0.6, ls=':')

    # Plot configuration
    ax[1].set_xscale('log')
    ax[0].grid(color='gray')
    ax[0].set_title(f'SynchBFS over Erdos Renyi with p: {p[:-2]}%')
    ax[1].set_title('Verification of the communication complexity')
    ax[0].set_ylim(0, max([max(results['C']),max(results['E'])])*1.1)
    ax[1].set_yscale('log')
    ax[0].set_xlabel("Number of Nodes")
    ax[0].set_ylabel("Value (logscale)")
    ax[1].set_xlabel("Communication (logscale)")
    ax[1].set_ylabel("Value (logscale)")
    ax[0].legend()
    ax[1].legend()
    plt.show()
    
