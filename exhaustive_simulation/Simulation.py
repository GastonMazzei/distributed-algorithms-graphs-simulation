from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from aux import compute_diam, count_edges, test_connectivity

from IndividualState import IndividualState as IndividualState
from Simulation_aux import sub_iteration

class Simulation():
    def __init__(self, N, p):
        self.graph = Graph(N,p, weighted=False)
        while not(test_connectivity(self.graph.am)):
            self.graph = Graph(N,p)
        self.E = count_edges(self.graph)
        self.diam = compute_diam(self.graph)
        self.ix = np.asarray(range(N))
        self.coms = [0]
        self.time = 0
        self.GLOBAL_HALTING_STATE = False

    def InitializeProcessors(self, type_of_simulation: str = "FloodMax", **kwargs):
        """
        Assign UIDs to each of the graph's elements, 
        and give them a "state"
        """
        self.States = []
        self.MessageLog = []
        self.FutureMessageLog = []
        for _ in range(self.graph.N):
            self.States += [IndividualState(**{
                                    'type_of_simulation':"FloodMax",
                                    'u': uuid4().int//2**64,
                                    **kwargs})]
            self.MessageLog += [[[-1] for _ in range(self.graph.N)]]
            self.FutureMessageLog += [[[-1] for _ in range(self.graph.N)]]
    
    def CleanChannels(self):
        self.MessageLog = self.FutureMessageLog.copy()
        self.FutureMessageLog = [[[-1] for _ in range(self.graph.N)] for __ in range(self.graph.N)]

    def Iterate(self, VERBOSE = False):
        """
        Do this for every processor while keeping track the "synchronic
        parallel time" + "number of communications". Thanks:
        Provide the transition function with all the requrired information
        in order for it to make its magic. 
        """
        if VERBOSE:
            print(self.graph.am)
        for i in range(self.graph.N):
            sub_iteration(self, i, VERBOSE = VERBOSE)
            if VERBOSE: 
                print(f'it {i}, halting state is {self.GLOBAL_HALTING_STATE}')
        if VERBOSE: 
            print('\n\n')
        self.time += 1
        self.CleanChannels()
        if self.GLOBAL_HALTING_STATE:
            raise Exception("HALT")
    
    def PerformSimulation(self, VERBOSE = False):
        if VERBOSE: 
            print('starting simulation')
            counter = 0
        while True:
#            if True:
            try:
                self.Iterate(VERBOSE = VERBOSE)
            except:
                if VERBOSE:
                    print('break')
                break
            if VERBOSE and counter % 5 == 0: 
                print(f'iteration #{counter}')
                counter += 1
        if VERBOSE: 
            print('ended simulation')
        return 0
