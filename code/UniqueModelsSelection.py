from numpy import unique

def unique_models_selection(population):
    """
    Selects a subset of unique models from the population
    Inputs:
     population     - list of superpositions (models)

    Outputs:
     population     - list of unique superpositions (models)
    """


    population = list(set(population))

    return population