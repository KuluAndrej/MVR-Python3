import code.modules.parametrizer as parametrizer
import code.StringToModel as StringToModel
import numpy as np


def crossover_population(population, data_to_fit):
    """
    Evaluate the quality of each model from the population
    Inputs:
     population         - list of Models to evaluate
     data_to_fit        - approximated data; necessary for the quality determination

    Outputs:
     population         - estimated population
    """

    # parametrize each superposition

