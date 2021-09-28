#!/bin/sh

# Script to produce an exhaustive simulation showing the behaviour
# of the algorithm "FloodMax" for electing a leader in an Erdos-Renyi graph
python3 exhaustive_simulation/FloodMax/FloodMax_main.py
python3 exhaustive_simulation/FloodMax/plotting_floodmax.py
