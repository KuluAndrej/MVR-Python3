

def unique_models_selection(population, number_of_best_models):
    """
    Selects best models from the population
    Inputs:
     population             - list of superpositions (models)
     number_of_best_models  - required number of the best selected models
    Outputs:
     population     - list of best superpositions (models)
    """
    number_of_best_models = int(number_of_best_models)
    sorted(population, key=lambda model:model.MSE)
    population = population[:min(number_of_best_models, len(population))]

    return population