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
import re

def rule_simplify(population):

    fopen = open('log.txt','w')
    for ind, model in enumerate(population):
        handle = model.handle
        handle = re.sub(r'X\[(\d+)\]', r'x\1', handle)
        backup_handle = handle
        handle = model_reconstruct(handle)
        handle = simplify_by_rules(handle)
            # here we fix some freaky bug
        # only the God knows the reasons of it
        while handle.find('x1') != -1:
            ind = handle.find('x1')
            handle = handle[0:ind] + 'bump_(x0)' + handle[ind+2:]

        # NOTE THAT IT CAN RUIN YOUR CLASSIFICATION MACHINE
        # STAY CAREFUL
        handle = model_reconstruct(handle)
        new_handle = handle
        handle = re.sub(r'x(\d+)', r'X[\1]', handle)

        population[ind].handle = handle
        if len(backup_handle) > len(new_handle):
            #print(backup_handle, '-->\n', new_handle)
            #print(model_reconstruct(backup_handle))
            print(backup_handle,file = fopen)

            setattr(population[ind], "backup_handle", backup_handle)

    return population