import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/FloodMax/results-floodmax.pkl', 'rb') as f:
        results = pickle.load(f)

    # Prepare data
    p = str(round(results['P'][0]*100,0))
    D = np.asarray(results['D'])
    N = np.asarray(results['N'])
    E = np.asarray(results['E'])
    C = np.asarray(results['C'])
    fig, ax = plt.subplots(1,2,figsize=(15,10))

    # Plot raw data
    ax[0].plot(N, C,label='Messages', lw=4, c='k', ls=':')
    ax[0].plot(N, E, label='Edges', lw=4, c='r', ls='-')
    ax[0].plot(N, D, label='Depth', lw=4, c='g', ls='dotted')
    
    # Plot the relevant dependence, as the message complexity is
    # Communication ~ Edges * Depth (p.54 Distributed Algorithms, Nancy Lynch)
    y = D * E
    ax[1].scatter(C, y, label=r'$Edges \times Depth$', c='y', alpha=1)
    pol = np.polyfit(C,y,1)
    ax[1].plot(C, np.polyval(pol,C), label='linear fit', c='k', lw=3, alpha=0.6, ls=':')


    
    # Plot configuration
    ax[0].grid(color='gray')
    ax[0].set_title(f'FloodMax over Erdos Renyi with p: {p[:-2]}%')
    ax[1].set_title(f'Verification of the communication complexity')
    ax[0].set_ylim(1, max([max(results['C']),max(results['E']), max(D)])*1.1)
    ax[0].tick_params(axis='y', colors='r')
    ax[0].set_xlabel('Number of Nodes')
    ax[0].set_ylabel('Value (logscale)')
    ax[0].set_yscale('log')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    ax[1].set_xlabel('Communication (logscale)')
    ax[1].set_ylabel('Value (logscale)')
    plt.savefig('exhaustive_simulation/FloodMax/results.png')
    plt.show()
    
    







