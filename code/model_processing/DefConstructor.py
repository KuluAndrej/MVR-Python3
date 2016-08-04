from code.primitives.Primitives import *

from code.structures.Population import Population
from code.structures.Model import Model

def def_constructor(model):
    """
    Constructs a python def definition for 'model'.
    Inputs:
     model                  - structure storing a superposition of primitive functions and
        an information related with it

    Outputs:
     def_statement          - python def statement for 'model'
    """
    base_string = "lambda X"
    list_of_parameters = [ ",w" + str(i + 1) for i in range(model.number_of_parameters)]
    parameters_string = ''.join(list_of_parameters)
    base_string += parameters_string
    base_string += ": "
    base_string += model.param_handle
    setattr(model, 'str_func', base_string)
    def_statement = eval(base_string)

    return def_statement

def add_def_statements_attributes(population):
    if isinstance(population,Model):
        setattr(population, "def_statement", def_constructor(population))
        return population
    elif isinstance(population,Population):
        for model in population:
            setattr(model, "def_statement", def_constructor(model))
