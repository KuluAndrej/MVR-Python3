from code.modules.parametrizer import parametrizing
from code.structures.Population import Population
from code.structures.Model import Model
import re

def parametrize_population(population):
    """
    Return a list of parametred handles made from ones listed in 'handles_list'
    Inputs:
     population         - list of superpositions (instances of the class Model)

    Outputs:
     param_handles_list - list of parametred superposition handles

    Author: Kulunchakov Andrei, MIPT
    """

    # extract handles of the superpositions from the population and parametrize them
    # launch only for those of models, which have no set sufficient attributes
    for ind, _ in enumerate(population):
        population[ind] = parametrize_model(population[ind])

    return population

def parametrize_model(model):
    if not hasattr(model, 'param_handle'):
        parametrizing_outputs = parametrizing(model.handle)
    else:
        parametrizing_outputs = (model.param_handle, model.number_of_parameters)

    # process the outputs of parametrizing
    if not type(parametrizing_outputs)==type(()):
        param_handles_list = parametrizing_outputs.first
    else:
        param_handles_list = parametrizing_outputs[0]
    if not type(parametrizing_outputs)==type(()):
        numbers_of_parameters = parametrizing_outputs.second
    else:
        numbers_of_parameters = parametrizing_outputs[1]

    # insert parametred handles into the class instances

    setattr(model, 'param_handle', param_handles_list)
    setattr(model, 'number_of_parameters', numbers_of_parameters)
    setattr(model, 'number_of_tokens', find_number_of_tokens(model.handle))

    return model

# Function parsing superposition handle and finding number of tokens which it consists of
def find_number_of_tokens(handle):
    # here we use the property of primitive functions: they end with special symbol '_'
    number_of_primitive_function = len([char for char in list(handle) if char == '_'])
    number_of_variables = len(re.compile('X\[\d+\]').findall(handle))
    return number_of_primitive_function + number_of_variables