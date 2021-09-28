import sys,os

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

DEBUG = False

def show_graph_(Graph, layout_n=3):

    if Graph.tree_status:
        f, ax = plt.subplots(1,2,figsize=(12,6))
    else:
        f, ax = plt.subplots(1,1,figsize=(7,7))
    
    # Get the adjcancency matrix from the Graph Class
    A = Graph.am

    # Create DiGraph from A
    G = nx.from_numpy_matrix(A, create_using=nx.DiGraph)

    # Use some layout to handle positioning of graph
    LAYOUT = [nx.spring_layout,
            nx.spectral_layout,
            nx.shell_layout,
            nx.planar_layout,
            ][layout_n]
    layout = LAYOUT(G)

    # Use a list for node_sizes
    #sizes = [1000,400,200]

    # Use a list for node colours
    #color_map = ['g', 'b', 'r']

    # Draw the graph using the layout - with_labels=True if you want node labels.
    if Graph.tree_status:
        nx.draw(G, layout, with_labels=True, ax=ax[0])
        #, node_size=sizes, node_color=color_map)
        # Get weights of each edge and assign to labels
        labels = nx.get_edge_attributes(G, "weight")
        # Draw edge labels using layout and list of labels
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels, ax=ax[0])
        ax[0].set_title(f'Erdos renyi graph with\nN={Graph.N}, p={Graph.p}, undirected={Graph.undirected}')
    else:
        nx.draw(G, layout, with_labels=True, ax=ax)
        #, node_size=sizes, node_color=color_map)
        # Get weights of each edge and assign to labels
        labels = nx.get_edge_attributes(G, "weight")
        # Draw edge labels using layout and list of labels
        nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels, ax=ax)



    if Graph.tree_status:

        # Get the adjcancency matrix from the Graph's tree
        A = tree_to_adjcacency_matrix(Graph.tree)
        if DEBUG: print(f'A tree was made and it was this: {A}')
        # Create DiGraph from A
        G = nx.from_numpy_matrix(A, create_using=nx.DiGraph)

        # Use a list for node_sizes
        #sizes = [1000,400,200]

        # Use a list for node colours
        color_map = ['r' if _ != Graph.i0 else 'g' for _ in range(Graph.N)]
        for i in range(len(color_map)):
            if sum(A[i,:]+A[:,i])==0:
                color_map[i] = 'w'

        # Draw the graph using the layout - with_labels=True if you want node labels.
        nx.draw(G, layout, 
                    node_color=color_map,
                    ax=ax[1]
                    )
        ax[1].set_title(f'Associated Tree beggining in node {Graph.i0}')


    # Show plot
    plt.show()

def tree_to_adjcacency_matrix(tree):
    k = sorted(list(tree.keys()))
    N = len(k)
    A = np.zeros((N,N))
    for i in k:
        for j in tree[i]['children']:
            A[i,j] = 1
    return A

def build_tree_(Graph):
    ixs = np.asarray(range(Graph.N))
    marked = [False if _ != Graph.i0 else True for _ in range(Graph.N)]
    parent = {}
    children = {}
    current = [Graph.i0]
    current_children = []
    tot = 1
    depth = 0
    def flatten(t):
        return [item for sublist in t for item in sublist]
    while sum(marked)!=Graph.N and tot != 0:
        # Reinitialize counter of total news: it protects against disconnected nodes
        tot = 0
        dads = flatten(parent.values())
        for i in current:
            # Get the nodes that "i" points to
            connected_to = ixs[np.where(Graph.am[i,:]!=0,True,False)].tolist()
            # Exclude brothers, nephews and parents
            connected_to = [_ for _ in connected_to if _ not in current + current_children + dads]
            # For all the children:
            for c in connected_to:
                # Add them to the node's list of children
                children[i] = children.get(i,[]) + [c]
                # Add the node to the children's parent
                parent[c] = [i]
                # Mark the children as parsed
                marked[c] = True
                # Increase the counter by one
                tot += 1
            # Append the children connected to node "i" to the 
            # total list of childrens at this level of the tree
            current_children += connected_to.copy()
        # The current nodes are those previously defined as children
        current = current_children.copy()
        # The list of current children gets reinitialized
        current_children = []
        # Count depth
        depth += 1
    # Store the results in the object
    for i in range(Graph.N):
        Graph.tree[i]['parent'] = parent.get(i,[])
        Graph.tree[i]['children'] = children.get(i,[])
    # Store the tree's depth
    Graph.tree_depth = depth if sum(marked)==Graph.N else np.inf

















