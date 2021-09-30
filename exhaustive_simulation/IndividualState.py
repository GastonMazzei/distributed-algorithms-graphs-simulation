from Graph import Graph
from uuid import uuid4 

import numpy as np, pandas as pd, matplotlib.pyplot as plt

import sys, os, pickle

from aux import compute_diam, count_edges, test_connectivity


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
        if type_of_state == 'OptFloodMax':
            #specifics go here!
            self.max_uid = u 
            self.leader = None
            self.rounds = 0
            self.diam = kwargs['diam']
            self.already_seen = []
        if type_of_state == "SynchBFS" :
            self.marked = False
            self.parent = None
            self.diam = kwargs['diam']
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
                communication_complexity[0] += len(keys)
                if self.max_uid == self.u:
                    self.leader = True
                else:
                    self.leader = False
                return True
            communication_complexity[0] += len(keys)
            return False

        if self.type == "OptFloodMax":
            if kwargs.get('VERBOSE',False): 
                print(f'\ntransitioning for u: {self.u}')
            previous_max = [self.max_uid].copy()[0]
            LIMIT = self.diam 
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
                if previous_max!=self.max_uid:
                    self.answer = [[self.max_uid] if out_keys[i] not in self.already_seen else [-1] for i in range(len(out_keys))]
                else:
                    self.answer = [[-1] for _ in range(len(out_keys))]
                if kwargs.get('VERBOSE',False):
                    print(f'answer is {self.answer}')
            elif self.rounds == LIMIT:
                communication_complexity[0] += len([x for x in self.answer if x[0]!=-1])
                if self.max_uid == self.u:
                    self.leader = True
                else:
                    self.leader = False
                return True
            #self.already_seen += 
            communication_complexity[0] += len([x for x in self.answer if x[0]!=-1])
            return False

        if self.type == "SynchBFS":
            if self.marked:
                self.answer = [[-1] for _ in range(len(out_keys))]
                # request halting if all the nodes are marked
                marked_status = [P.marked for P in kwargs['Simulation'].States]
                return all(marked_status)
            incoming_messages = []
            for k in keys:
                incoming_messages += [other_states[k].msg]
            if 'search' in incoming_messages:
                self.marked = True
                self.msg = 'search'
            self.rounds += 1
            self.answer = [[self.max_uid] for _ in range(len(out_keys))]
            if kwargs.get('VERBOSE',False):
                print(f'round {self.rounds}, u {self.u}, mesgs {messages}')
                print(f'answer is {self.answer}')

            communication_complexity[0] += len(keys)
            return False
