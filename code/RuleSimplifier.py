"""
Get the handle of a superposition and transform it in concise form such that the values
of the function do not change.
This procedure is performed for all models from a population


Note that for correct work of the rule simplification, we should transform a handle in
the way that subtrees of commutative nodes are ordered
Author: Kulunchakov Andrei, MIPT
"""
from code.modules.model_simplifier_by_rules import simplify_by_rules
from code.modules.model_reconstructer import model_reconstruct
from code.structures import Model
import re

def rule_simplify(population):

    for ind, model in enumerate(population):
        handle = model.handle
        print(handle)
        handle = re.sub(r'X\[(\d+)\]', r'x\1', handle)

        handle = model_reconstruct(handle)
        print('reconstruct terminated', handle)
        handle = simplify_by_rules(handle)
        print('simplify_by_rules terminated')

        handle = re.sub(r'x(\d+)', r'X[\1]', handle)
        population[ind] = Model.Model(handle)

    return population