import code.StringToModel as StringToModel
import numpy as np

def select_best_models(population, number_of_best_models):
    """
    Select best models from the population
    Inputs:
     population             - list of superpositions (models)
     number_of_best_models  - required number of the best selected models
    Outputs:
     population     - list of best superpositions (models)
    """
    errors = [model.MSE for model in population]


    # convert new strings to a population and append it to the existed one
    population.extend( StringToModel.strings_to_population(new_generated_superpositions) )
    return population