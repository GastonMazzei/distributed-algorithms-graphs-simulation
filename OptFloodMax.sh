#!/bin/sh

# Script to produce an exhaustive simulation showing the behaviour
# of the algorithm "FloodMax" for electing a leader in an Erdos-Renyi graph
python3 exhaustive_simulation/OptFloodMax/OptFloodMax_main.py
python3 exhaustive_simulation/OptFloodMax/plotting_optfloodmax.py
