from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from exhaustive_simulation.Simulation import Simulation

def main(N, p, AB, VERBOSE = False, mini_VERBOSE = False):


    S = Simulation(N, p, is_it_weighted=True)
    S.graph.make_undirected()

    # DEBUG
    TEST = False
    if TEST:
        S.graph.am[0,:] = np.asarray([0,2,0,6,0])
        S.graph.am[1,:] = np.asarray([2,0,3,8,5])
        S.graph.am[2,:] = np.asarray([0,3,0,0,7])
        S.graph.am[3,:] = np.asarray([6,8,0,0,9])
        S.graph.am[4,:] = np.asarray([0,5,7,9,0])
        S.graph.make_undirected()
        AB = (10,20)


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
            return (0,0,0,0,0,False)
    if VERBOSE: 
        S.graph.view()
    params = {'diam' :  S.diam, 'type_of_state' : "SynchGHS", 'N' : N, 'AB': AB}
    S.InitializeProcessors(**params)   
    S.PerformSimulation(VERBOSE = VERBOSE)

    cont = []
    for k,v in S.cache.items():
        for v_ in v:
            if v_ > 0:
                cont.append(v_)
    if len(cont)>0:
        cont_min = min(cont)
    else:
        cont_min = 0
    if mini_VERBOSE: 
        tree = None
        for P in S.States:
            if  len(P.component['connections'].keys())==N:
                tree = P.component['connections']
                break
        S.graph.tree = np.zeros((N,N))
        if tree == None:
            print("Script failed!")
            return 0,0,0,0,0,False
        for k,v in tree.items():
            for v_j in v:
                S.graph.tree[k,v_j] = 1
                S.graph.tree[v_j,k] = 1
        S.graph.tree_status = True
        S.graph.i0 = None
        S.graph.is_tree_adjacency = True
        S.graph.view()
        #plt.hist(cont, bins=20);plt.show()

    return (S.time, S.coms[0], S.E, S.diam, cont_min,  True)

if __name__=='__main__':
    VERBOSE = [False, True][0]
    mini_VERBOSE = [False, True][1]
    results = {'N':[], 'P':[], 'T':[], 'C':[], 'E':[], 'D':[], 'CM':[], 'AB':[]}
    AB = (30,20)
    for p in [0.7]:
        for N in list(range(2,25))+[30,35,40,45,50]:
            T_loc, C_loc, E_loc, D_loc, CM_loc, b = main(N,p, AB, VERBOSE = VERBOSE, 
                                                      mini_VERBOSE = mini_VERBOSE)
            if b:
                results['N'].append(N)
                results['P'].append(p)
                results['T'] += [T_loc].copy()
                results['C'] += [C_loc].copy()
                results['E'] += [E_loc].copy()
                results['D'] += [D_loc].copy()
                results['CM'] += [CM_loc].copy()
                results['AB'] += [AB]
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
    

