#!/bin/sh

# Script to produce an exhaustive simulation showing the behaviour
# of the algorithm "SynchBFS" for electing a leader in an Erdos-Renyi graph
rm exhaustive_simulation/SynchBFS/results-synchbfs.pkl
python3 exhaustive_simulation/SynchBFS/SynchBFS_main.py
python3 exhaustive_simulation/SynchBFS/plotting_synchbfs.py
