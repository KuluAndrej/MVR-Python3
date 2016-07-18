import code.estimators_selectors.CalculatorModelValues as CalculatorModelValues
from numpy import  sum, isnan, inf,  nan, transpose
import warnings
from numpy.linalg import norm as norm

def quality_estimator(population, data_to_fit, config):
    """
    Estimates the errors of approximation for models in the population
    Inputs:
     population     - list of superpositions (models)
     data_to_fit    - data which were approximated
     config
    Outputs:
     populations    - list of estimated superpositions (models)

    Author: Kulunchakov Andrei, MIPT
    """
    independent_var = data_to_fit[:,1:]
    independent_var = transpose(independent_var)
    dependent_var = data_to_fit[:,0]



    # now estimate the error of approximation for each model
    with warnings.catch_warnings(record=True) as w:
         # Cause all warnings to always be triggered.
        warnings.simplefilter("always")
        for model in population:

            if (hasattr(model, "is_deprecated")):
                setattr(model, "MSE", inf)
                continue

            dependent_var_estimation = CalculatorModelValues.calculate_model_values(model,independent_var)
            setattr(model, "MSE", norm(dependent_var - dependent_var_estimation))

    for model in population:
        if isnan(model.MSE):
            model.MSE = inf

        if config["model_generation"]["type_selection"] == "Penalize_params":
            if hasattr(model, "optimal_params"):
                setattr(model,"Penalized_error", model.MSE + float(config["model_generation"]["parameters_penalty"]) * norm(model.optimal_params))
            else:
                setattr(model,"Penalized_error", model.MSE)
    return population

