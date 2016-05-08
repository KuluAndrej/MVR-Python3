from code.modules.random_model_generator import random_model_generation
import code.StringToModel as StringToModel
from code.structures.Population import Population
def random_population(number_of_models, number_of_variables, required_size):
    """
    Perform a generation of random superpositions.
    Inputs:
     number_of_models       - required size of a random population
     number_of_variables,
     required_size          - parameters of a random model required by random_model_generation
        to generate appropriate random model

    Outputs:
     population             - random population
    """
    number_of_models = int(number_of_models)
    # superpositions generated by crossings
    new_generated_superpositions = []
    list_of_new_handles = [random_model_generation(number_of_variables, required_size) for i in range(number_of_models)]


    # convert new strings to a population and append it to the existed one
    populationNew = StringToModel.strings_to_population(list_of_new_handles)
    list(map(lambda model: setattr(model, 'where_from', "random"), populationNew))

    return Population(populationNew)