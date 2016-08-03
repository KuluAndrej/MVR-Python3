import code.estimators_selectors.CalculatorModelValues as CalculatorModelValues
import numpy as np

def create(model, config):
    """
    Gets a 'model' and specified characteristics of independent variables from 'config'.
    Creates data, which will be fitted by other models.=
    Inputs:
     model   - provides a calculation of the dependent variable
     config

    Outputs:
     data_to_fit - independent variables described in 'config' + calculated dependent variable

    Author: Kulunchakov Andrei
    """

    grid_limits = eval(config["rules_creation"]["range_independent_var"])
    grid = np.linspace(grid_limits[0], grid_limits[1],
                       int(config["rules_creation"]["number_of_samples"]))
    grid = grid.reshape(-1,1)


    dependent_var = CalculatorModelValues.calculate_model_values(model, grid.T)
    if type(dependent_var)==type(1) or type(dependent_var)==type(1.0) or not dependent_var.shape:
        dependent_var = dependent_var * np.ones(grid.shape)

    dependent_var = dependent_var.reshape(-1,1)

    return np.hstack((dependent_var, grid))