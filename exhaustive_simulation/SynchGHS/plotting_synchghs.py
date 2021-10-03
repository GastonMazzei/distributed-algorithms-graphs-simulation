import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/SynchGHS/results-synchghs.pkl', 'rb') as f:
        results = pickle.load(f)

    # Compute the erdos renyi parameter "p"
    p = results['P'][0]

    # Prepare two axis
    fig, ax1 = plt.subplots()

    ax1.plot(results['N'], results['C'],label='Messages', c='k',lw=4,alpha=0.7, ls='-')
    ax1.plot(results['N'], results['E'],label='Edges', c='r',lw=4,alpha=0.7, ls='-')
    ax1.plot(results['N'], results['T'],label='Time', c='b',lw=4,alpha=0.7, ls='-')
    ax1.scatter(results['N'], results['C'], c='k',lw=4,alpha=0.7, ls='-')
    ax1.scatter(results['N'], results['E'], c='r',lw=4,alpha=0.7, ls='-')
    ax1.scatter(results['N'], results['T'], c='b',lw=4,alpha=0.7, ls='-')

    ax1.grid(color='gray')
    ax1.set_yscale('log')
    ax1.set_title(f'SynchGHS over Erdos Renyi with p: {int(100*p)}%')
    ax1.set_ylim(0, max(results['C']) * 1.1) #max([max(results['C']),max(results['E'])])*1.1)

    TWIN = [False, True][0]
    if TWIN:
        ax2 = ax1.twinx()
        #ax2.scatter(results['N'],
        #    [results['T'][i]/results['D'][i] for i in range(len(results['E']))],label=r'$\frac{Time}{Diameter}$',
        #    c='g', lw=3)
        ax2.plot(results['N'], results['E'],label='Edges', c='r',lw=4,alpha=0.7, ls='-')
        ax2.set_ylabel('Value')
        ax2.set_ylim(0,max(results['E']))
        ax2.legend()
        ax2.tick_params(axis='y', colors='g')

    ax1.tick_params(axis='y', colors='r')
    ax1.set_ylabel('Value')
    if False:
        ax1.set_xscale('log')
        ax2.set_xscale('log')
    plt.xlabel('Nodes')
    ax1.legend()
    #plt.yscale('log')
    plt.show()
    
