"""
Gets list of rules stored in specified file
All rules are converted to models

Author: Kulunchakov Andrei, MIPT
"""
from code.structures.Model import Model

def retrieve(filename = "data/rules.txt"):
    lines = open(filename, 'r').readlines()
    patterns = []
    replacements = []

    for line in lines:
        patterns.append(Model(line.split()[0]))
        replacements.append(Model(line.split()[1]))

    return patterns, replacements
