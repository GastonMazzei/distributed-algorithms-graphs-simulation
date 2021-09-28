from Graph import Graph

import numpy as np, pandas as pd

import sys, os

def test_connectivity(A):
    if 0 in np.sum(A, axis=0):
        return False
    if 0 in np.sum(A, axis=1):
        return False
    return True

def count_edges(Graph):
    aux = np.where(Graph.am.flatten()>0,1,0)
    if Graph.undirected:
        return np.sum(aux)//2    
    else:
        return np.sum(aux)    

def compute_diam(Graph):
    diam = 0
    for i in range(Graph.N):
        Graph.build_random_tree(starting_point=i)
        diam = max([diam, Graph.tree_depth])
    return diam

class IndividualState():
    def __init__(self, type_of_state = 'FloodMax', u = 0, **kwargs):
        self.u = u
        self.answer = []
        if type_of_state == 'FloodMax':
            #specifics go here!
            self.max_uid = u 
            self.leader = None
            self.rounds = 0
            self.diam = kwargs['diam']


    def transition(self, 
                other_states: dict = {},
                weights: dict = {},
                messages: dict = {}
                communication_complexity: int):
        # states  is a dict of states
        # weights is a dict  of integers
        # messages is a dict of objects
        # communication complexity must be increased!


class FloodMaxSimulation():
    def __init__(self, N, p):
        self.graph = Graph(N,p, weighted=False)
        while not(test_connectivity(self.graph.am)):
            self.graph = Graph(N,p)
        self.E = count_edges(self.graph)
        self.diam = compute_diam(self.graph)
        self.ix = np.asaray(range(N))
        self.coms = 0
        self.time = 0

    def InitializeProcessors(self, type_of_simulation: str = "FloodMax", **kwargs):
        """
        Assign UIDs to each of the graph's elements, 
        and give them a "state"
        """
        self.States = []
        self.MessageLog = []
        self.FutureMessageLog = []
        for _ in range(self.graph.N)
            self.States += [IndividualState({
                                    'type_of_simulation':"FloodMax",
                                    'u': uuid4().int//2**64,
                                    **kwargs})]
            self.MessageLog += [[]]
            self.FutureMessageLog += [[]]
    
    def CleanChannels(self):
        self.MessageLog = self.FutureMessageLog.copy()
        self.FutureMessageLog = [[] for _ in range(self.graph.N)]

    def Iterate(self):
        """
        Do this for every processor while keeping track the "synchronic
        parallel time" + "number of communications". Thanks:
        Provide the transition function with all the requrired information
        in order for it to make its magic. 
        """
        for i in range(self.graph.N):
            perform_FloodMax_iteration_(self, i)
        self.time += 1
        self.CleanChannels()
        if self.HALTING_STATE:
            raise Exception("HALT")
    
    def PerformSimulation(self, VERBOSE = False):
        if VERBOSE: 
            print('starting simulation')
            counter = 0
        while True:
            try:
                self.Iterate()
            except:
                break
            if VERBOSE and counter % 10 == 0: 
                print(f'iteration #{counter}')
                counter += 1
        return 0

def perform_FloodMax_iteration_(FloodMaxSimulation, i):
    graph = FloodMaxSimulation.graph
    states = FloodMaxSimulation.States
    message_log = FloodMaxSimulation.MessageLog
    # Avoid interacting with each neighbor individually as in general
    # the transition function could be nonlocal.
    indexes = ix[np.where(graph.am[:,i]>0, True, False)]
    states[i].transition(
        "other_states" = {j : states[j] for j in indexes},
        "weights" = {{j : graph[j,i] for j in indexes},
        "messages" = {j : message_log[j,i] for j in indexes},
        "communication_complexity" = FloodMaxSimulation.coms
        )
    for j,k in enumerate(indexes):    
        FloodMaxSimulation.FutureMessageLog[i,k] = states[i].answer[j].copy()     
        

def main(N, p, VERBOSE = False):
    S = FloodMaxSimulation(N, p)
    print(f'there are {S.E} edges, and the diameter is {S.diam}')
    S.graph.tree_status = False
    if VERBOSE: S.graph.view()


if __name__=='__main__':
    main(8,0.25, True)


