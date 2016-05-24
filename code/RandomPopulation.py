from code.modules.random_model_generator import random_model_generation
import code.StringToModel as StringToModel
from code.structures.Population import Population
from random import randint

def random_population(number_of_models, number_of_variables, maximum_required_size):
    """
    Perform a generation of random superpositions.
    Inputs:
     number_of_models       - required size of a random population
     number_of_variables,
     maximum_required_size  - maximum possible structural complexity of a randomly generated model
        to generate appropriate random model

    Outputs:
     population             - random population
    """
    number_of_models = int(number_of_models)

    required_size = randint(4,maximum_required_size)
    list_of_new_handles = random_model_generation(number_of_variables, required_size, number_of_models, randint(1,100000)).split('$')
    list_of_new_handles = list_of_new_handles[:-1]

    # convert new strings to a population and append it to the existed one
    listOfNewModels = StringToModel.strings_to_population(list_of_new_handles)
    list(map(lambda model: setattr(model, 'where_from', "random"), listOfNewModels))

    return listOfNewModels