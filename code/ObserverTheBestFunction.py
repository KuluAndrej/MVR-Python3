import numpy as np
import code.CalculatorModelValues as CalculatorModelValues
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
    print(model.MSE)
    #if hasattr(model, 'optimal_params'):
    #print(model.optimal_params)
    dependent_var_estimation = CalculatorModelValues.calculate_model_values(model,independent_var)


    dependent_var            = dependent_var.reshape(1,-1)
    dependent_var_estimation = dependent_var_estimation.reshape(1,-1)

    plt.plot(independent_var[0], dependent_var[0], 'r--', independent_var[0], dependent_var_estimation[0], 'b')
    plt.show()