import numpy as np
from numpy import  sum, isnan, inf,  nan, transpose, errstate
import os
import matplotlib.pyplot as plt

def observer_the_best_function(population, data_to_fit):
    """
    Draw on the same plot initial and predicted values
    Inputs:
     population     - set of the best approximating functions for 'data_to_fit'
     data_to_fit    - initial values to be approximated


    Author: Kulunchakov Andrei, MIPT
    """
    if (data_to_fit.shape[1] > 2):
        return

    independent_var = data_to_fit[:,1:]
    independent_var = transpose(independent_var)
    dependent_var = data_to_fit[:,0]

    model = population[0]
    dependent_var_estimation = []
    if hasattr(model, "optimal_params"):
        # insert found parameters into the def_statement
        model.def_statement_param = lambda row: model.def_statement(row, *model.optimal_params)

        if not isnan(sum(model.optimal_params)):
            try:
                dependent_var_estimation = model.def_statement_param(independent_var)
            except:
                dependent_var_estimation = [nan for row in independent_var]
            setattr(model, "MSE", norm(dependent_var - dependent_var_estimation))
        else:
            setattr(model, "MSE", nan)
    else:
        try:
            dependent_var_estimation = model.def_statement(independent_var)
        except RuntimeWarning:
            dependent_var_estimation = [nan for row in independent_var]
        setattr(model, "MSE", norm(dependent_var - dependent_var_estimation))

    plt.plot(data_to_fit[:,1], data_to_fit[:,0], 'r--', t, t**2, 'b--', t, t**3, 'g^')
    plt.show()

    return data_to_fit
