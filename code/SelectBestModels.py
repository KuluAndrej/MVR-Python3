from code.structures.Population import Population
from code.Decorators import handicraft_timer


def select_best_models(population, config):
    """
    Selects best models from the population
    Inputs:
     population             - list of superpositions (models)
     config.model_generation.best_models_number  - required number of the best selected models
     config.model_generation.type_selection      - specifies the criterion used for model selection
    Outputs:
     population     - list of best superpositions (models)
    """


    number_of_best_models = int(config["model_generation"]["best_models_number"])
    type_of_selection = config["model_generation"]["type_selection"]
    population.sort(type_of_selection)


    population = population[:min(number_of_best_models, len(population))]

    return population