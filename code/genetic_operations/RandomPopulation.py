from code.modules.random_model_generator import random_model_generation
import code.model_processing.StringToModel as StringToModel
from random import randint

def random_population(number_of_variables, config, is_initial_load):
    """
    Perform a generation of random superpositions.
    Inputs:
     number_of_variables,
     config.model_generation.random_models_number       - required size of a random population
     config.model_generation.random_models_complexity  - maximum possible structural complexity of a randomly generated
        model to generate appropriate random model
     is_initial_load                                   - before the evolution starts we load 1000 random models to population

    Outputs:
     population             - random population

    Author: Kulunchakov Andrei, MIPT
    """
    number_of_models = int(config["model_generation"]["random_models_number"])
    maximum_required_size = int(config["model_generation"]["random_models_complexity"])
    required_size = randint(2,maximum_required_size)
    if is_initial_load:
        number_of_models = int(config["init_rand_models"]["number_of_init_random_models"])
        required_size = int(config["init_rand_models"]["size_init_random_models"])

    list_of_new_handles = random_model_generation(number_of_variables, required_size, number_of_models, randint(1,100000)).split('$')
    list_of_new_handles = list_of_new_handles[:-1]

    # convert new strings to a population and append it to the existed one
    listOfNewModels = StringToModel.strings_to_population(list_of_new_handles)
    list(map(lambda model: setattr(model, 'where_from', "random"), listOfNewModels))

    return listOfNewModels