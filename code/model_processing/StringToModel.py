from code.structures.Model import Model
def strings_to_population(handles):
    """
    Get a list of superposition handles and return a list of instances of Model-class
    Inputs:
     handles        - list of superposition handles

    Outputs:
     populations    - list of instances of Model-class built from handles

    """
    population = list(map(Model, handles))

    return population

