from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from aux import compute_diam, count_edges, test_connectivity


def sub_iteration(Simulation, i, VERBOSE = False, **kwargs):
    # Avoid interacting with each neighbor individually as in general
    # the transition function could be nonlocal.
    indexes = Simulation.ix[np.where(Simulation.graph.am[:,i]>0, True, False)].copy()
    out_indexes = Simulation.ix[np.where(Simulation.graph.am[i,:]>0, True, False)].copy()
    Simulation.GLOBAL_HALTING_STATE = (
        Simulation.States[i].transition(
            keys = indexes,
            out_keys = out_indexes,
            other_states = {j : Simulation.States[j] for j in indexes},
            weights = {j : Simulation.graph.am[j,i] for j in indexes},
            messages = {j : Simulation.MessageLog[j][i] for j in indexes},
            communication_complexity = Simulation.coms,
            Simulation = Simulation,
             **kwargs,
            ) or  Simulation.GLOBAL_HALTING_STATE
    )
    for k in out_indexes:    
        Simulation.FutureMessageLog[i][k] = Simulation.States[i].answer.get(k,[-1]).copy()     
    if VERBOSE: 
        print(f'The future message log has  been updates: {Simulation.FutureMessageLog}')
    txt = ('\n' +
            str(Simulation.States[i].answer) + '\n' +
            f'ix: {i}, r: {Simulation.States[i].rounds}, L: {Simulation.States[i].level}')
    