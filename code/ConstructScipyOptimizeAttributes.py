from code.modules.extract_model_tokens_encodings import extract_tokens
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
from functools import reduce
from re import sub, compile

def construct_info(model,dict_tokens_info):
    """
    Construct arrays which will be passed to scipy.optimize.curve_fit. These arrays contain
    necessary information about initial parameters for parameters and its domains.

    Inputs:
    model                   - model which parameters are to be optimized
    tokens_info             - dictionary with tokens names as keys and the following values:
     initial_values         - initial values for optimized parameters
     bounds                 - specified set of values of parameters, where optimization occurs

    Outputs:
     p0         - scipy.optimize.curve_fit attribute: Initial guess for the parameters.
     bounds     - scipy.optimize.curve_fit attribute: Lower and upper bounds on the parameters

    Author: Kulunchakov Andrei, MIPT
    """
    # function detect is 'string' represents a variable
    def is_var(string):
        pattern = compile("x[0-9]*")
        return pattern.match(string)

    handle = sub(r'X\[(\d+)\]', r'x\1', model.handle)
    tokens_names = extract_tokens(handle).split('&')

    preproc_init_values = [dict_tokens_info[token][0] for token in tokens_names if not is_var(token)]
    preproc_left_bounds  = [dict_tokens_info[token][1][0] for token in tokens_names if not is_var(token)]
    preproc_right_bounds = [dict_tokens_info[token][1][1] for token in tokens_names if not is_var(token)]

    p0 = []
    bounds = [[],[]]

    concatenator = lambda x, y: x+y
    if preproc_init_values:
        p0 = reduce(concatenator, preproc_init_values)
        # now we initialize bounds as a list,
        # then it will be converted to a 2-tuple of array_like

        bounds[0] = reduce(concatenator, preproc_left_bounds)
        bounds[1] = reduce(concatenator, preproc_right_bounds)

        bounds = (bounds[0], bounds[1])

    return (p0, bounds)


def construct_info_population(population,dict_tokens_info):
    for model in population:
        if not hasattr(model,'curve_fit_init_params'):
            p0, bounds = construct_info(model,dict_tokens_info)
            setattr(model, "curve_fit_init_params", p0)
            setattr(model, "curve_fit_bounds", bounds)
