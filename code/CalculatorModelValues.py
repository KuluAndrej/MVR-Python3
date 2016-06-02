from numpy import  sum, isnan, inf,  nan, transpose
from numpy.linalg import norm
import warnings

def calculate_model_values(model, independent_var):
    """
    Calculate values of the 'model' on independent variables presented in 'independent_var'
    Inputs:
     model
     independent_var    - data having independent variables
    Outputs:
     values

    Author: Kulunchakov Andrei, MIPT
    """
    independent_var = data_to_fit[:,1:]
    independent_var = transpose(independent_var)
    dependent_var = data_to_fit[:,0]



    # now estimate the error of approximation for each model
    with warnings.catch_warnings(record=True) as w:
         # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        if hasattr(model, "optimal_params"):
            # insert found parameters into the def_statement
            model.def_statement_param = lambda row: model.def_statement(row, *model.optimal_params)

            if not isnan(sum(model.optimal_params)):
                try:
                    dependent_var_estimation = model.def_statement_param(independent_var)
                except:
                    dependent_var_estimation = [nan for row in independent_var]
                return dependent_var_estimation
            else:
                return nan * np.ones(dependent_var.shape)
        else:
            try:
                dependent_var_estimation = model.def_statement(independent_var)
            except RuntimeWarning:
                dependent_var_estimation = [nan for row in independent_var]

            return dependent_var_estimation



    return population

