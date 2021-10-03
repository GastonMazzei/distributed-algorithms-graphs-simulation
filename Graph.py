import sys,os

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from aux import show_graph_, build_tree_

if False:
    SEED = 1234
    np.random.seed(SEED)



class Graph():
    def __init__(self, N=3, p=0.1, weighted=True):
        self.N = N
        self.p = p
        self.am = ( 
            (np.ones((N,N))-np.identity(N)) * 
            np.where(np.random.rand(N**2)>(1-p),1,0).reshape(N,N)
        ) 
        if weighted:
            self.am *= np.random.choice(range(1,2*N**2), N**2, replace=False).reshape((N,N))
        self.am = self.am.astype('uint8')
        self.i0 = None
        self.tree = None
        self.tree_status = False
        self.tree_depth = 0
        self.is_tree_adjacency = False
        self.undirected = False

    def make_undirected(self):
        self.am = ((self.am.astype('int') + self.am.T.astype('int'))/2).astype('uint8')
        self.undirected = True

    def build_random_tree(self, starting_point=False):
        if starting_point!=False:
            self.i0 = starting_point
        else:
            self.i0 = np.random.randint(0,self.N)
        self.tree = {_:{'parent':[],'children':[]} for _ in range(self.N)}
        build_tree_(self)
        self.tree_status = True

    def view(self):
        try:
            show_graph_(self,2)
        except:
            try:
                show_graph_(self,0)
            except:
                try:
                    show_graph_(self,1)
                except:
                    show_graph_(self,3)

if __name__=='__main__':
    try:
        g = Graph(int(sys.argv[1]),float(sys.argv[2]))
        if sys.argv[3]=='1':
            g.make_undirected()
    except:
        g = Graph(4,0.5)
    g.build_random_tree()
    g.view()
