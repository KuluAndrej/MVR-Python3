from code.modules.parametrizer import parametrizing

def parametrize_population(population):
    """
    Return a list of parametred handles made from ones listed in 'handles_list'
    Inputs:
     population         - list of superpositions (instances of the class Model)

    Outputs:
     param_handles_list - list of parametred superposition handles

    """

    # extract handles of the superpositions from the population and parametrize them
    # launch only for those of models, which have no set sufficient attributes


    parametrizing_outputs = [parametrizing(model.handle) if not hasattr(model, 'param_handle') else (model.param_handle, model.number_of_parameters) for model in population]

    # process the outputs of parametrizing
    param_handles_list = [StringIntPairObject.first if not type(StringIntPairObject)==type(()) else StringIntPairObject[0] for StringIntPairObject in parametrizing_outputs]
    numbers_of_parameters = [StringIntPairObject.second if not type(StringIntPairObject)==type(()) else StringIntPairObject[1] for StringIntPairObject in parametrizing_outputs]

    # insert parametred handles into the class instances
    list(map(lambda ind: setattr(population[ind], 'param_handle', param_handles_list[ind]), range(len(population))))
    list(map(lambda ind: setattr(population[ind], 'number_of_parameters', numbers_of_parameters[ind]), range(len(population))))

    return population

