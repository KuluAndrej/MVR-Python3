import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.model_processing.FitModelToData as FitModelToData
from code.model_processing.StringToModel import strings_to_population
from numpy import zeros, array, isnan
from numpy.linalg import norm

def check(pattern, replacement, dict_tokens_info, config, do_plot=True, verbose=False):
    """
    Once the replacement is fit for one realization of random parameters of pattern, we launch
    multistart procedure on this set. Namely, we get several new realization of this set and check
    similarity for each realization

    Author: Kulunchakov Andrei

    """
    if verbose:
        print_intro(pattern, replacement)

    # If the pattern is a constant function, we do not permit our replacement function to have terminals
    if pattern.number_of_terminals == 0 and replacement.number_of_terminals > 0:
        return False


    is_mse_permissible = zeros(int(config["rules_creation"]["iterations_to_check_fitness"]))
    errors             = zeros(int(config["rules_creation"]["iterations_to_check_fitness"]))
    threshold          = eval(config["rules_creation"]["threshold"])


    for i in range(int(config["rules_creation"]["iterations_to_check_fitness"])):
        if hasattr(replacement, 'optimal_params'):
            delattr(replacement, 'optimal_params')
        if hasattr(pattern, 'optimal_params'):
            delattr(pattern, 'optimal_params')

        attempts = 0
        while attempts < 1000:
            SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)
            data_to_fit = CreateDataToFit.create(pattern, config)
            if max(abs(data_to_fit[:,0])) < eval(config["rules_creation"]["maximum_value"]):
                break
            attempts += 1
        if attempts == 1000:
            print("Did not succeed in creating data with finite values.")
            return (False,None)

        fitted_values = FitModelToData.fit(replacement, data_to_fit, dict_tokens_info, config, do_plot)
        if any(isnan(fitted_values)):
            return (False,None)

        is_mse_permissible[i] = check_fitness(data_to_fit[:,0], fitted_values, config)
        errors[i] = norm(data_to_fit[:,0] - fitted_values)

    is_fitted = sum(is_mse_permissible) > is_mse_permissible.shape[0] * (1 - float(config["rules_creation"]["fraction_of_misfittings"]))
    if verbose:
        print(is_mse_permissible,'\n', errors, sep='')
        if is_fitted:
            print(replacement, "is fittable to the ", pattern)
        else:
            print(replacement, "is NOT fittable to the ", pattern)

    return (is_fitted, is_mse_permissible)


def check_fitness(data_to_fit, fitted_values,config):
    maximum_l0 = float(config["rules_creation"]["maximum_l0"])
    differences = array(abs(data_to_fit - fitted_values))
    return not any(differences > maximum_l0)

def print_intro(pattern, replacement):
    print(replacement, "is being fitted to", pattern)
