#!/bin/sh

# Script to produce an exhaustive simulation showing the behaviour
# of the algorithm "SynchGHS" for building a MST in an Erdos-Renyi 
# undirected weighted graph
rm exhaustive_simulation/SynchGHS/results-synchghs.pkl
python3 exhaustive_simulation/SynchGHS/SynchGHS_main.py
python3 exhaustive_simulation/SynchGHS/plotting_synchghs.py
