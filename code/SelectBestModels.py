from code.structures.Population import Population
from code.Decorators import handicraft_timer

@handicraft_timer
def select_best_models(population, number_of_best_models,type_of_selection):
    """
    Selects best models from the population
    Inputs:
     population             - list of superpositions (models)
     number_of_best_models  - required number of the best selected models
     type_of_selection      - specifies the criterion used for model selection
    Outputs:
     population     - list of best superpositions (models)
    """

    number_of_best_models = int(number_of_best_models)

    population.sort(type_of_selection)
    population = population[:min(number_of_best_models, len(population))]

    return population