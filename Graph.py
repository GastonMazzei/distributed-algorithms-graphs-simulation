import sys,os

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from aux import show_graph, build_tree

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

    def make_undirected():
        pass
        
    def build_random_tree(self):
        self.i0 = np.random.randint(0,self.N)
        self.tree = [[] for _ in range(self.N)]
        build_tree_(self)

    def view(self):
        show_graph(self)

if __name__=='__main__':
    g = Graph(8,0.2)
    g.view()
