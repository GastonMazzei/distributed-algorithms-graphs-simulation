import sys,os

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from aux import show_graph_, build_tree_

SEED = 1234
np.random.seed(SEED)



class Graph():
    def __init__(self, N=3, p=0.1):
        self.N = N
        self.am = ( 
            (np.ones((N,N))-np.identity(N)) * 
            np.where(np.random.rand(N**2)>(1-p),1,0).reshape(N,N)
        ) * np.random.randint(1,max([N, 1000]),(N,N))
        self.am = self.am.astype('uint8')
        self.i0 = None
        self.tree = None
        self.tree_status = False
        self.tree_length = 0

    def make_undirected():
        pass

    def build_random_tree(self):
        self.i0 = np.random.randint(0,self.N)
        self.tree = {_:{'parent':[],'children':[]} for _ in range(self.N)}
        build_tree_(self)
        self.tree_status = True

    def view(self):
        try:
            show_graph_(self,3)
        except:
            try:
                show_graph_(self,2)
            except:
                try:
                    show_graph_(self,1)
                except:
                    show_graph_(self,0)

if __name__=='__main__':
    g = Graph(8,0.5)
    g.build_random_tree()
    g.view()
