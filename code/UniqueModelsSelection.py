from numpy import unique
from code.structures.Population import Population
def unique_models_selection(population):
    """
    Selects a subset of unique models from the population
    Inputs:
     population     - list of superpositions (models)

    Outputs:
     population     - list of unique superpositions (models)
    """


    population = Population(list(set(population)))

    return population