from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from exhaustive_simulation.Simulation import Simulation

def main(N, p, VERBOSE = False):
    S = Simulation(N, p, is_it_weighted=True)
    S.graph.make_undirected()
    if VERBOSE: 
        print(f'there are {S.E} edges, and the diameter is {S.diam}')
        print(f'{S.i_}, {S.TOL}')
    S.graph.tree_status = False
    print(S.constructor_success)
    if not S.constructor_success:
        if VERBOSE:
            raise Exception("Script failed")
        else:
            print('Script Failed')
            return (0,0,0,0,False)
    if VERBOSE: S.graph.view()
    # DEBUG
    S.graph.view()
    # DEBUG
    params = {'diam' :  S.diam, 'type_of_state' : "SynchGHS"}
    S.InitializeProcessors(**params)   
    S.PerformSimulation(VERBOSE = VERBOSE)
    print(S.States[0].component['connections'])
    return (S.time, S.coms[0], S.E, S.diam, True)

if __name__=='__main__':
    VERBOSE = [False, True][0]
    results = {'N':[], 'P':[], 'T':[], 'C':[], 'E':[], 'D':[]}
    for p in [0.99]:
        for N in [8]:
            T_loc, C_loc, E_loc, D_loc, b = main(N,p, VERBOSE = VERBOSE)
            if b:
                results['N'].append(N)
                results['P'].append(p)
                results['T'] += [T_loc].copy()
                results['C'] += [C_loc].copy()
                results['E'] += [E_loc].copy()
                results['D'] += [D_loc].copy()

    try:
        with open('exhaustive_simulation/SynchGHS/results-synchghs.pkl', 'rb') as f:
            previous_data = pickle.load(f)
    except:
        previous_data = {}

    with open('exhaustive_simulation/SynchGHS/results-synchghs.pkl', 'wb') as f:
        pickle.dump({**results, **previous_data}, f)        

    LOW_QUALITY_PLOT = False
    if LOW_QUALITY_PLOT:
        plt.plot(results['N'], results['C'],label='Messages')
        plt.plot(results['N'], results['E'],label='Edges')
        plt.ylabel('Number')
        plt.xlabel('Nodes')
        plt.legend()
        #plt.yscale('log')
        plt.show()
    

