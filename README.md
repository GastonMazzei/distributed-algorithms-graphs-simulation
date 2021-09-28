# distributed-algorithms-graphs-simulation
<b>Info:</b>

Simulation of synchronic distributed algorithms over weighted directed networks implemented in Python

<b>Basic usage:</b> 

`python3 Graph.py N f b`

where N is the number of nodes, f the Erdos Renyi probability, and b can be 0 or 1 to determine if it is undirected (1) or not (0).

To make the following picture the command was 

`python3 Graph.py 8 0.3 1`.

<img src="https://github.com/GastonMazzei/distributed-algorithms-graphs-simulation/blob/main/example.png" width=800>

<b>More info:</b> 

- <i>aux.py</i>: contains auxiliary functions



- <i>Graph.py</i>: contains the class definition of an Erdos Renyi graph implememnted with an adjacency matrix, which has the following outstanding methods:
  - Graph.make_undirected(): <i>a method to make it undirected.</i>
  - Graph.build_random_tree(): <i>a method to compute a tree using Breadth First Search beggining from a randomly selected node.</i>
  - Graph.view(): <i>a method to plot the built tree.</i>
