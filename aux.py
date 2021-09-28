import sys,os

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def show_graph(Graph):

    # Get the adjcancency matrix from the Graph Class
    A = Graph.am

    # Create DiGraph from A
    G = nx.from_numpy_matrix(A, create_using=nx.DiGraph)

    # Use some layout to handle positioning of graph
    LAYOUT = [nx.spring_layout,
            nx.spectral_layout,
            nx.planar_layout,
            nx.shell_layout,
            ][2]
    layout = LAYOUT(G)

    # Use a list for node_sizes
    #sizes = [1000,400,200]

    # Use a list for node colours
    #color_map = ['g', 'b', 'r']

    # Draw the graph using the layout - with_labels=True if you want node labels.
    nx.draw(G, layout, with_labels=True)#, node_size=sizes, node_color=color_map)

    # Get weights of each edge and assign to labels
    labels = nx.get_edge_attributes(G, "weight")

    # Draw edge labels using layout and list of labels
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)

    # Show plot
    plt.show()