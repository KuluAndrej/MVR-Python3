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
import code.model_processing.DefConstructor as DefConstructor
import code.model_processing.Parametrizer as Parametrizer
import re
import code.ResultsCollector as ResultsCollector
from code.structures.Population import Population

def rule_simplify(population, config):
    rules_filename = construct_filename(config)

    for ind, model in enumerate(population):
        backup_handle = model.handle
        handle = simplify_by_rules(model_reconstruct(backup_handle), rules_filename)
        handle = model_reconstruct(handle)

        new_handle = handle

        population[ind].handle = handle

        if len(backup_handle) > len(new_handle):
            #print(backup_handle, '-->\n', new_handle)
            #print(model_reconstruct(backup_handle))
            setattr(population[ind], "backup_handle", backup_handle)
            population[ind].renew_tokens()
            population[ind] = Parametrizer.parametrize_model(population[ind], reparametrize = True)
            population[ind] = DefConstructor.add_def_statements_attributes(population[ind])
            ResultsCollector.collect([backup_handle, population[ind]], config, None, "fit models to options", use_simplification=True)

    return population

def construct_filename(config):
    if config["flag_type_of_processing"]["flag"] == "rules_creation":
        return config["rules_creation"]["rules_folder"] + config["rules_creation"]["rules_filename"]
    else:
        return config["rules_creation"]["rules_used_in_fitting"]
