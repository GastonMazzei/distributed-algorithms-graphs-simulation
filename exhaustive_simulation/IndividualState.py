from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from aux import compute_diam, count_edges, test_connectivity


class IndividualState():
    def __init__(self, type_of_state = 'FloodMax', u = 0, **kwargs):
        self.u = u
        self.answer = {}
        self.type = type_of_state
        if type_of_state == 'FloodMax':
            #specifics go here!
            self.max_uid = u 
            self.leader = None
            self.rounds = 0
            self.diam = kwargs['diam']
        if type_of_state == 'OptFloodMax':
            #specifics go here!
            self.max_uid = u 
            self.leader = None
            self.rounds = 0
            self.diam = kwargs['diam']
            self.previous_round_seen = []
        if type_of_state == "SynchBFS" :
            self.marked = False
            self.previous_mark = False
            self.parent = None
            self.diam = kwargs['diam']
            self.rounds = 0
            self.msg = -1
            self.i0 = kwargs['i0']
        if type_of_state == "BellmanFord":
            self.i0 = kwargs['i0']
            self.parent = None
            self.dist = np.inf
            self.rounds = 0
            self.msg = -1

    def transition(self, 
                keys = [],
                out_keys = [],
                other_states: dict = {},
                weights: dict = {},
                messages: dict = {},
                communication_complexity: list = [],
                **kwargs,
                ):
        """
        It's a long code, modelling transitions according to each algorithm.
        Just keep calm and remember that messages == [-1] represent empty
        """
        if self.type == "FloodMax":
            if kwargs.get('VERBOSE',False): 
                print(f'\ntransitioning for u: {self.u}')
            LIMIT = self.diam 
            # Initialization
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
                self.answer = {k:[self.max_uid] for k in out_keys}
                if kwargs.get('VERBOSE',False):
                    print(f'answer is {self.answer}')
                communication_complexity[0] += len(keys)
                return False
            elif self.rounds == LIMIT:
                communication_complexity[0] += len(keys)
                if self.max_uid == self.u:
                    self.leader = True
                else:
                    self.leader = False
                return True

        if self.type == "OptFloodMax":
            if kwargs.get('VERBOSE',False): 
                print(f'\ntransitioning for u: {self.u}')
            previous_max = [self.max_uid].copy()[0]
            LIMIT = self.diam 
            if self.rounds == 0:
                for k in keys:
                    messages[k] = [ other_states[k].u]
                self.previous_round_seen =  keys
            # Weights will be ignored
            self.rounds += 1
            max_arriving_uid = max([messages[k][0] for k in keys])
            self.max_uid = max([self.max_uid, max_arriving_uid])
            if kwargs.get('VERBOSE',False):
                print(f'round {self.rounds}, u {self.u}, mesgs {messages}')
                print(f'limit is {LIMIT}')
            if self.rounds < LIMIT:
                # One improvement
                if previous_max!=self.max_uid:
                    self.answer = {k:[self.max_uid] for k in out_keys}
                else:
                    self.answer = {k:[-1] for k in out_keys}
                # Further improvement
                for k in self.answer.keys():
                    if k in self.previous_round_seen:
                        self.answer[k] = [-1]
                if kwargs.get('VERBOSE',False):
                    print(f'answer is {self.answer}')
            elif self.rounds == LIMIT:
                communication_complexity[0] += len([v for v in self.answer.values() if v[0]!=-1])
                if self.max_uid == self.u:
                    self.leader = True
                else:
                    self.leader = False
                return True
            self.previous_round_seen =  keys
            communication_complexity[0] += len([v for v in self.answer.values() if v[0]!=-1])
            return False

        if self.type == "SynchBFS":
            if self.rounds == 0:
                # Am I "i0"?
                my_ix = np.argmax([0 if P.u!=self.u else 1 for P in kwargs['Simulation'].States])
            else: 
                my_ix = -1
            incoming_messages = [v[0] for v in messages.values()]
            if (not self.previous_mark) and (('search' in incoming_messages) or 
                                            (my_ix == self.i0)):
                msg = 'search'
                self.marked = True
                if my_ix == self.i0:
                    self.parent = -1 # "-1" means root!
                elif 'search' in incoming_messages:
                    self.parent = np.random.choice(list(keys))
            else:
                msg = -1
            self.answer = {k:[msg] for k in out_keys}
            self.rounds += 1
            self.previous_mark = [self.marked].copy()[0]
            communication_complexity[0] += len([v for v in self.answer.values() if v[0]!=-1])
            marked_status = [P.marked for P in kwargs['Simulation'].States]
            if kwargs.get('VERBOSE',False):
                print(f'out of, {len(marked_status)} only {len([m for m in marked_status if m==True])} are marked!')
                print(f'round {self.rounds}, u {self.u}, mesgs {messages}')
                print(f'answer is {self.answer}')
            return all(marked_status)

        if self.type == "BellmanFord":
            if self.rounds == 0:
                # Am I "i0"?
                my_ix = np.argmax([0 if P.u!=self.u else 1 for P in kwargs['Simulation'].States])
                if my_ix == self.i0:
                    self.dist = 0
                    self.parent = -1
                messages = {k : np.inf for k in keys}
            options = {k : weights[k] + messages[k] for k in keys}
            v = list(options.values())
            if min(v)<self.dist:
                self.dist = min(v)
                self.parent = [k for k in keys if options[k] == min(v)][0]
            msg = [self.dist].copy()[0]
            self.answer = {k:[msg] for k in out_keys}
            self.rounds += 1
            communication_complexity[0] += len(out_keys)
            parental_status = [P.parent for P in kwargs['Simulation'].States]
            if kwargs.get('VERBOSE',False):
                print(f'round {self.rounds}, u {self.u}, mesgs {messages}')
                print(f'answer is {self.answer}')
            if self.rounds >= len(parental_status):
                return True
            else:
                return False
#            return len(parental_status) == len([p for p in parental_status if p != None])


