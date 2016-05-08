from numpy import  sum, isnan, nan, transpose, errstate
from numpy.linalg import norm
import warnings

def quality_estimator(population, data_to_fit):
    """
    Estimates the errors of approximation for models in the population
    Inputs:
     population     - list of superpositions (models)
     data_to_fit    - data which were approximated
    Outputs:
     populations    - list of estimated superpositions (models)

    """
    independent_var = data_to_fit[:,1:]
    independent_var = transpose(independent_var)
    dependent_var = data_to_fit[:,0]



    # now estimate the error of approximation for each model
    with warnings.catch_warnings(record=True) as w:
         # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        for model in population:

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

    return population

