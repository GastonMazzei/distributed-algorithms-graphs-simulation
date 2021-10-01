#!/bin/sh

# Script to produce an exhaustive simulation showing the behaviour
# of the algorithm "BellmanFord" for electing a shortest path in an Erdos-Renyi graph
rm exhaustive_simulation/BellmanFord/results-bellmanford.pkl
python3 exhaustive_simulation/BellmanFord/BellmanFord_main.py
python3 exhaustive_simulation/BellmanFord/plotting_bellmanford.py
