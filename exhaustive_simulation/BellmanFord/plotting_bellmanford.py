import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/BellmanFord/results-bellmanford.pkl', 'rb') as f:
        results = pickle.load(f)

    # Prepare variables and figures
    p = str(round(results['P'][0]*100,0))
    fig, ax = plt.subplots(1,2, figsize=(15,10))
    C = np.asarray(results['C'])
    E = np.asarray(results['E'])
    N = np.asarray(results['N'])
    
    # Plot raw data
    ax[0].plot(N, C, label='Messages', c='k',lw=4,alpha=0.7, ls=':')
    ax[0].plot(N, E, label='Edges', c='r',lw=4,alpha=0.7, ls='-')
    ax[0].plot(N, N, label='Nodes', c='g',lw=2,alpha=0.5, ls='dotted')


    # Plot the relevant dependence, as the message complexity is
    # Communication ~ Nodes * Edges (p.62 Distributed Algorithms, Nancy Lynch)
    y = (N * E)
    ax[1].scatter(C, y, label=r'$Edges \times Nodes$',c='y',alpha=1)
    pol = np.polyfit(C,y,1)
    ax[1].plot(C, np.polyval(pol,C), label='linear fit',c='k',lw=3,alpha=0.6, ls=':')

    # Plot configuration
    ax[0].grid(color='gray')
    ax[0].set_title(f'SynchBFS over Erdos Renyi with p: {p[:-2]}%')
    ax[1].set_title(f'Verification of the communication complexity')
    ax[0].set_ylim(1, max([max(results['C']),max(results['E'])])*1.1)
    ax[0].tick_params(axis='y', colors='r')
    ax[0].set_xlabel('Number of Nodes')
    ax[0].set_ylabel('Value (logscale)')
    ax[0].set_yscale('log')
    ax[1].set_xscale('log')
    ax[1].set_yscale('log')
    ax[1].legend()
    ax[1].set_xlabel('Communication (logscale)')
    ax[1].set_ylabel('Value (logscale)')
    ax[0].legend()

    plt.show()
    
