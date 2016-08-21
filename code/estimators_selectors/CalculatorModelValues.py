from numpy import  sum, isnan, ones,  nan, random
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
                    dependent_var_estimation = nan * ones(independent_var.shape[1])
                if not hasattr(dependent_var_estimation, "size") or dependent_var_estimation.size == 1:
                    dependent_var_estimation = dependent_var_estimation * ones(independent_var.shape[1])

                return dependent_var_estimation
            else:
                return nan * ones(independent_var.shape[1])
        elif hasattr(model, "init_params"):
            # insert found parameters into the def_statement
            #model.init_params = 2 * random.rand(model.init_params.shape[0]) - 1
            #print(model.init_params)
            model.def_statement_param = lambda row: model.def_statement(row, *model.init_params)

            if not isnan(sum(model.init_params)):
                try:
                    dependent_var_estimation = model.def_statement_param(independent_var)
                except:
                    dependent_var_estimation = nan * ones(independent_var.shape[1])
                return dependent_var_estimation
            else:
                return nan * ones(independent_var.shape[1])

        else:
            try:

                dependent_var_estimation = model.def_statement(independent_var)
            except RuntimeWarning:
                dependent_var_estimation = nan * ones(independent_var.shape[1])
            except TypeError:
                dependent_var_estimation = nan * ones(independent_var.shape[1])

            return dependent_var_estimation

