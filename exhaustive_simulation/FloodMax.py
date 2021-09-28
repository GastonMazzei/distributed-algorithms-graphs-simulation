from Graph import Graph
from uuid import uuid4 

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
    diam = np.inf
    for i in range(Graph.N):
        Graph.build_random_tree(starting_point=i)
        diam = min([diam, Graph.tree_depth])
    return diam

class IndividualState():
    def __init__(self, type_of_state = 'FloodMax', u = 0, **kwargs):
        self.u = u
        self.answer = []
        self.type = type_of_state
        if type_of_state == 'FloodMax':
            #specifics go here!
            self.max_uid = u 
            self.leader = None
            self.rounds = 0
            self.diam = kwargs['diam']
    def transition(self, 
                keys = [],
                out_keys = [],
                other_states: dict = {},
                weights: dict = {},
                messages: dict = {},
                communication_complexity: int = 0,
                **kwargs,
                ):
        if self.type == "FloodMax":
            if kwargs.get('VERBOSE',False): 
                print(f'\ntransitioning for u: {self.u}')
            LIMIT = self.diam + 4
            if self.rounds == 0:
                for k in keys:
                    messages[k] = [ other_states[k].u]
            # Weights will be ignored
            self.rounds += 1
            max_arriving_uid = max([messages[k][0] for k in keys])
            self.max_uid = max([self.max_uid, max_arriving_uid])
            if kwargs.get('VERBOSE',False):
                print(f'round {self.rounds}, u {self.u}, mesgs {messages}')
                print(f'limit is {LIMIT}')
            if self.rounds < LIMIT:
                self.answer = [[self.max_uid] for _ in range(len(out_keys))]
                if kwargs.get('VERBOSE',False):
                    print(f'answer is {self.answer}')
            elif self.rounds == LIMIT:
                communication_complexity += len(keys)
                if self.max_uid == self.u:
                    self.leader = True
                else:
                    self.leader = False
                return True
            communication_complexity += len(keys)
            return False

class FloodMaxSimulation():
    def __init__(self, N, p):
        self.graph = Graph(N,p, weighted=False)
        while not(test_connectivity(self.graph.am)):
            self.graph = Graph(N,p)
        self.E = count_edges(self.graph)
        self.diam = compute_diam(self.graph)
        self.ix = np.asarray(range(N))
        self.coms = 0
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
            perform_FloodMax_iteration_(self, i, VERBOSE = VERBOSE)
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

def perform_FloodMax_iteration_(FloodMaxSimulation, i, VERBOSE = False):
    # Avoid interacting with each neighbor individually as in general
    # the transition function could be nonlocal.
    indexes = FloodMaxSimulation.ix[np.where(FloodMaxSimulation.graph.am[:,i]>0, True, False)].copy()
    out_indexes = FloodMaxSimulation.ix[np.where(FloodMaxSimulation.graph.am[i,:]>0, True, False)].copy()
    FloodMaxSimulation.GLOBAL_HALTING_STATE = (
        FloodMaxSimulation.States[i].transition(
            keys = indexes,
            out_keys = out_indexes,
            other_states = {j : FloodMaxSimulation.States[j] for j in indexes},
            weights = {j : FloodMaxSimulation.graph.am[j,i] for j in indexes},
            messages = {j : FloodMaxSimulation.MessageLog[j][i] for j in indexes},
            communication_complexity = FloodMaxSimulation.coms,
            ) or  FloodMaxSimulation.GLOBAL_HALTING_STATE
    )
    for j,k in enumerate(out_indexes):    
        FloodMaxSimulation.FutureMessageLog[i][k] = FloodMaxSimulation.States[i].answer[j].copy()     
    if VERBOSE: 
        print(f'The future message log has  been updates: {FloodMaxSimulation.FutureMessageLog}')

def main(N, p, VERBOSE = False):
    S = FloodMaxSimulation(N, p)
    if VERBOSE: 
        print(f'there are {S.E} edges, and the diameter is {S.diam}')
    S.graph.tree_status = False
    if VERBOSE: S.graph.view()
    S.InitializeProcessors(type_of_simulation = "FloodMax", diam = S.diam)   
    S.PerformSimulation(VERBOSE = VERBOSE)
    if VERBOSE: 
        print([P.leader for P in S.States])
        print(f'There are {sum([P.leader for P in S.States])} leaders')
        print(f'uids are {[P.u for P in S.States]}')
        print(f'The max UID is: {max([P.u for P in S.States])}, and the leader\'s is {[P.max_uid for P in S.States][0] if len(set([P.max_uid for P in S.States]))==1 else [P.max_uid for P in S.States]}')

if __name__=='__main__':
    main(3,0.2, VERBOSE=False)


