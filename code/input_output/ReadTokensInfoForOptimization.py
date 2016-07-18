import numpy as np
def read_info_tokens_for_optimization(config):
    """
    Read info about tokens from specified file.
    This info is necessary for correct work of scipy.optimize.curve_fit.
    It includes initial values for optimized parameters and ranges, where optimal values
    will be found.

    Inputs:
     config.tokens_info.info_for_curve_fit  - list of Models to evaluate
    Outputs:
    tokens_info             - dictionary with tokens names as keys and the following values:
     initial_values         - initial values for optimized parameters
     bounds                 - specified set of values of parameters, where optimization occurs

    Author: Kulunchakov Andrei, MIPT
    """

    file_with_info = open(config["tokens_info"]["info_for_curve_fit"], 'r')

    lines = file_with_info.readlines()

    def parse_line(line):
        token_name,init_value,bounds = line.split(" ")
        return (token_name,init_value,bounds)

    # ignore the header
    # parse remained lines
    token_name_array  = []
    init_values_array = []
    bounds_array      = []
    for line_ind in np.arange(1,len(lines)):
        token_name,init_value,bounds = parse_line(lines[line_ind])
        token_name_array.append(token_name)
        init_values_array.append(eval(init_value))
        bounds_array.append(eval(bounds))

    tokens_info = {token : (init_values, bounds) \
                   for token, init_values, bounds in zip(token_name_array,init_values_array,bounds_array)}
    return tokens_info