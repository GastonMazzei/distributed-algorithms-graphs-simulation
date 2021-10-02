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

        if self.type == 'SynchGHS':
            # IMPORTANT: for a weighted UNDIRECTED graph
            #
            # we start with k = 1 so our N-nodes graph is split into components
            # that have only k = 1 nodes. Therefore, we start with all the nodes 
            # disconnected.
            #
            # In general, the procedure will run in levels. For each level, 
            # a fixed number of rounds will occur. This is O(n).
            #
            # here list stuff we require:
            #   METHODS
            #       - self.level = 1
            #       - self.ix = None
            #       - self.component = None
            #       - self.rounds = 1
            #       - self.answer = {}
            #       - self.cache = []
            #       - self.exchange = False
            #       - self.forward_MWOE = True
            #       - self.leader = True
            #       - self.inactive_rounds = 0
            #   KWARGS
            #       -kwargs['Simulation']
            # Clean the answers as we will build it iteratively, i.e. 
            # as opposed to overwritting it at once.
            self.answer = {}
            #initialize stuff for level 1
            if self.level == 1 and self.rounds == 1:
                self.leader = True
                self.ix = np.argmax([0 if P.u!=self.u else 1 for P in kwargs['Simulation'].States])
                self.component = {
                                #'connections': kwargs['Simulation'].graph.am.copy() * 0,
                                'leader' : self.u,
                }
                self.component['members'] = [self.ix]
            # Initialize stuff for rounds 1 of level "k"
            if self.rounds == 1:
                self.inactive_rounds = 0
                self.component['part'] = 1
                self.component['MWOE'] = None
                # round max should be a*r+b, but as we
                # dont know the parameters we use a
                # different termination mechanism
                self.component['terminate'] = False
            # Glossary of messages:
            #       [-1] : empty message
            #       ['search', int_ix] : a search message with the element's index
            #       ['convergecast', int_ix, int_min] : a convergecast message with
            #                                           both an index and the min
            #       ['elect a new leader']...
            #       [...]
            #       [...] 2 more pend
            if self.leader:
                # If leader and first round, search!
                if self.rounds == 1:
                    # Compute your own min outgoing edge please
                    potential_MWOEs = [(weights[k],k) for k in out_keys if k not in self.component['members']]
                    if len(potential_MWOEs) > 0:
                        MWOE, MWOE_ix = zip(*potential_MWOEs)
                        MWOE_ix = MWOE_ix[np.argmin(MWOE)]
                        MWOE = min(MWOE)
                    msg = 'search'
                    self.answer = {k:[msg, ix] for k in out_keys}
                    self.cache = {
                        'MWOE': [MWOE, MWOE_ix], 
                        'unseen_neighbors':[k for k in out_keys if k in self.component['members']],
                    }
                    self.rounds += 1
                    return False
                # Else the leader is an active member of the level 
                elif self.component['part'] == 1:
                    if self.component['part'] == 1:
                        for k,m in messages.items():
                            if m != [-1]:
                                if m[0] == 'convergecast':
                                    if self.cache['MWOE'][0]>m[2]:
                                        self.cache['MWOE'] = [m[2], m[1]]
                                    self.cache['unseen_neighbors'].pop(self.cache['unseen_neighbors'].index(m[1]))
                        if len(self.cache['unseen_neighbors']) == 0:
                            self.component['part'] == 2:
                            self.answer = {k:['elect new leader', self.cache['MWOE'][1], self.cache['MWOE'][0]] if k in self.component['members'] else k:[-1] for k in out_keys}
                            del self.answer[self.ix]
                            if len(self.component['members'])>1:
                                return False
                if self.component['part'] == 1:
                    self.rounds += 1
                    self.answer = {k:[-1] for k in out_keys}
                    return False

            # Compute the neighbors from our component, and default fill 
            # the message for those that are not as null
            neighbors_in_component = [k for k in out_keys if k in self.component['members']]
            for k in out_keys:
                if k not in neighbors_in_component:
                    self.answer[k] = [-1] 

            # List the neighbors that sent "search" and "convergecast"
            search_requesters = []
            convergecast_requesters = []
            new_leader_requests = []
            not_electing_leader = True
            for k,v in messages.items():
                if v != [-1]:
                    if v[0] in ['private leader choosing','the new leader is']:
                        not_eleting_leader = False
                        break
                    elif v[0]=='search':
                        search_requesters.append(v[-1:])
                    elif v[0]=='convergecast':
                        convergecast_requesters.append(v[1:])
                    elif v[0]=='elect a new leader':
                        new_leader_requests.append(v[1:])                           
            
            if not_eleting_leader:

                # If there is some search active, propagate it
                # to inactive nodes of the component
                if len(search_requesters) >= 1 and len(new_leader_requests)==0:
                    for k in neighbors_in_component:
                        if messages[k] == [-1]:
                            self.answer[k] = ['search', self.ix]

                # If we recieved convergecast requests,
                # or we have no new neighbors in out
                # component to forward a search message
                # to, it is required to compute our MWOE
                if ((len(convergecast_requesters)>0 or  
                    (len(search_requesters)==len(neighbors_in_component)))
                    and len(new_leader_requests)==0):
                    # Compute the MWOE
                    potential_MWOEs = [(weights[k],k) for k in out_keys if k not in self.component['members']]
                    if len(potential_MWOEs) > 0:
                        MWOE, MWOE_ix = zip(*potential_MWOEs)
                        MWOE_ix = MWOE_ix[np.argmin(MWOE)]
                        MWOE = min(MWOE)
                        MWOE_found = True
                    else:
                        MWOE_found = False
                    indexes, values = zip(*convergecast_requesters)
                    min_ix =  indexes[np.argmin(values)]
                    min_value = min(values)
                    if MWOE_found:
                        if MWOE < min_value:
                            min_value = MWOE
                            min_ix = self.ix
                    for k in neighbors_in_component:
                        if k not in convergecast_requesters:
                            self.answer[k] = ['convergecast', min_value, min_ix]
                
                if len(new_leader_requests)>0 and (self.ix != new_leader_requests[0][0]):
                    # Broadcast the info
                    for k in neighbors_in_component:
                        if k in new_leader_requests:
                            self.answer[k] = [-1]
                        else:
                            self.answer[k] = ['elect a new leader', *new_leader_requests[0]]
                elif len(new_leader_requests)>0 or (self.leader):
                    # Get the UID of the P on the other side of the edge
                    UIDs = [P.u for P in kwargs['Simulation'].States]
                    ixj = np.argmax(np.where(kwargs['Simulation'].graph.am[self.ix,:]==new_leader_requests[0][1], 1, 0))
                    if UIDs[ixj] > self.u:
                        new_leader = UIDs[ixsj]
                    else:
                        new_leader = self.u
                    # Compute the new component
                    msg = ['private leader choosing', new_leader, self.component['members']]
                    self.answer = {k:msg if k==ixj else k:[-1] for k in out_keys}

            else:
                self.answer = {}
                if 'private leader choosing' in [v[0] for v in messages.values()]:
                    msg = 'private leader choosing'
                else:
                    msg = 'the new leader is'
                new_leader, new_component_members = (
                    [v for v in messages.values() if v[0]=='private leader choosing'][1:]
                )
                self.component['leader'] = new_leader 
                self.component['new_members'] = list(set(new_component_members + self.component['members']))
                if new_leader != self.u:
                    self.leader = False
                for k in out_keys:
                    if k in self.component['members'] and messages[k]==[-1]:
                        self.answer[k] = [msg, new_leader, self.component['new_members']]
                    else:
                        self.answer[k] = [-1]

            # Keep the show going...
            self.rounds += 1

            # Increase the "inactive  rounds" counter
            if len([v for v in self.answer.values() if v != [-1]])==0:
                if len([v for v in messages.values() if v != [-1]])==0:
                    self.inactive_rounds += 1

            # Should we move to the next level? if so, mark it.
            if self.inactive_rounds > 2**self.level:
                self.level += 1
                self.rounds = 1

            # Halt the Simulation if the MST has been built
            N = len(kwargs['Simulation'].States)
            if len(list(set(self.component['members'])))==N:
                return True
            return False












