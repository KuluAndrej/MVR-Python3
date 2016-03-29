import modules.parametrizer as parametrizer

def parametrize_population(handles_list):
    """
    Return a list of parametred handles made from ones listed in 'handles_list'
    Inputs:
     handles_list         - list of unparametred superposition handles

    Outputs:
     param_handles_list   - list of parametred superposition handles

    """
    param_handles_list = list(map(parametrizer.parametrizing, handles_list))
    return param_handles_list

