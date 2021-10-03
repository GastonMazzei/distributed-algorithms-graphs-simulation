import os,sys,pickle

import numpy as np, matplotlib.pyplot as plt


if __name__=='__main__':

    # Open
    with open('exhaustive_simulation/SynchGHS/results-synchghs.pkl', 'rb') as f:
        results = pickle.load(f)

    # Compute the erdos renyi parameter "p"
    p = results['P'][0]
    a,b = results['AB'][0]

    # Prepare two axis
    fig, ax1 = plt.subplots()

    if True:
        unwanted = []
        for i in range(len(results['N'])):
            if results['T'][i]<results['N'][i]:
                unwanted.append(i)
        for k,v in results.items():
            results[k] = [v_ for i,v_ in enumerate(v) if i not in unwanted]
        ax1.plot(results['N'], results['C'],label='Messages', c='k',lw=4,alpha=0.7, ls='-')
        ax1.plot(results['N'], results['E'],label='Edges', c='r',lw=4,alpha=0.7, ls='-')
        ax1.plot(results['N'], results['T'],label='Time', c='b',lw=4,alpha=0.7, ls='-')
        ax1.scatter(results['N'], results['C'], c='k',lw=4,alpha=0.7, ls='-')
        ax1.scatter(results['N'], results['E'], c='r',lw=4,alpha=0.7, ls='-')
        ax1.scatter(results['N'], results['T'], c='b',lw=4,alpha=0.7, ls='-')
        #ax1.plot(results['N'], results['CM'],label='Time excess', c='y',lw=4,alpha=0.7, ls='-')
        #ax1.scatter(results['N'], results['CM'], c='y',lw=4,alpha=0.7, ls='-')


        ax1.grid(color='gray')
        ax1.set_yscale('log')
        ax1.set_title(f'SynchGHS over Erdos Renyi with p: {int(100*p)}%')
        ax1.set_ylim(0, max(results['C']) * 1.1) #max([max(results['C']),max(results['E'])])*1.1)
    else:
        x2,y2 = [],[]
        for i,_ in enumerate(results['N']):
            if results['CM'][i]>1:
                x2.append(_)
                y2.append(results['CM'][i])
        #a,b = 10,15
        yrounds = [a*N+b for N in x2]

        print(min(y2))
        ax1.plot(x2,yrounds, c='r',lw=2, label=f'rounds per level\nax+b, a:{a}, b:{b}')
        ax1.plot(x2,y2, c='k',lw=2, label='excess of rounds')
        ax1.scatter(x2,yrounds, c='r', marker='s')
        ax1.scatter(x2,y2, c='k',marker='s')


    TWIN = [False, True][0]
    if TWIN:
        ax2 = ax1.twinx()
        pol = np.polyfit(x2, np.asarray(yrounds)-np.asarray(y2),1)
        ax2.scatter(x2, np.asarray(yrounds)-np.asarray(y2), c='k', label='rounds - excess')
        ax2.plot(x2, np.polyval(pol, x2), c='g', ls=':', label=r'$ax+b$'+f' fit,\na:{round(pol[0],2)}, b:{round(pol[1],2)}')

        ax2.set_ylabel('Value')
        ax2.set_ylim(0,2*max(np.asarray(yrounds)-np.asarray(y2)))
        ax2.legend(loc='lower right')
        ax2.tick_params(axis='y', colors='g')

    ax1.tick_params(axis='y', colors='r')
    ax1.set_ylabel('Value')

    plt.xlabel('Nodes')
    ax1.legend()
    #plt.yscale('log')
    plt.show()
    
