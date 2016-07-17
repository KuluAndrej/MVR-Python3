import numpy as np

def creator(model, config):
    """
    Gets a 'model' and creates rules, where this model acts as the 'replacement' model.
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """

    grid_limits = eval(config["rules_creation"]["range_independent_var"])
    grid = np.linspace(grid_limits[0], grid_limits[1],
                       int(config["rules_creation"]["number_of_samples"]))

