import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/BellmanFord/results-bellmanford.pkl', 'rb') as f:
        results = pickle.load(f)

    # Prepare two axis
    p = str(round(results['P'][0]*100,0))
    fig, ax1 = plt.subplots()
    print(max(results['E']))
    ax1.plot(results['N'], results['C'],label='Messages', c='k',lw=4,alpha=0.7, ls=':')
    #ax1.plot(results['N'], results['T'],label='Time', c='g',lw=2,alpha=0.7, ls='-')
    ax1.plot(results['N'], results['E'],label='Edges', c='r',lw=4,alpha=0.7, ls='-')
    ax1.plot(results['N'], results['N'],label='Nodes', c='g',lw=2,alpha=0.5, ls='dotted')
    y3 = np.asarray(results['N']) * np.asarray(results['E'])
    ax1.plot(results['N'], y3,
                            label='Edges * Nodes', c='y',lw=2,alpha=0.85, ls='-.')
    ax1.grid(color='gray')
    ax1.set_title(f'SynchBFS over Erdos Renyi with p: {p[:-2]}%')
    ax1.set_ylim(1, max([max(results['C']),max(results['E']), max(y3)])*1.1)
    ax1.tick_params(axis='y', colors='r')
    ax1.set_xlabel('Number')
    ax1.set_ylabel('Value (logscale)')
    ax1.set_yscale('log')
    TWIN = [False, True][0]
    if TWIN:
        ax2 = ax1.twinx()
        ax2.scatter(results['N'],
            [results['T'][i]/results['D'][i] for i in range(len(results['E']))],label=r'$\frac{Time}{Diameter}$',
            c='g', lw=3)
        ax2.set_ylabel('Quotient')
        ax2.set_ylim(0,4)
        ax2.legend()
        ax2.tick_params(axis='y', colors='g')
    if False:
        ax1.set_yscale('log')
        ax1.set_ylabel('Number (logscale)')
    if False:
        ax1.set_xscale('log')
        ax1.set_xlabel('Number (logscale)')
        if TWIN:
            ax2.set_xscale('log')
    plt.xlabel('Nodes')
    ax1.legend()
    #plt.yscale('log')
    plt.show()
    
