import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.model_processing.FitModelToData as FitModelToData
from code.model_processing.StringToModel import strings_to_population
from numpy import zeros
from numpy.linalg import norm
def check(pattern, replacement, dict_tokens_info, config, do_plot=True, verbose = False):
    """
    Once the replacement is fit for one realization of random parameters of pattern, we launch
    multistart procedure on this set. Namely, we get several new realization of this set and check
    similarity for each realization

    Author: Kulunchakov Andrei

    """

    print(replacement, "is being fitted to", pattern)
    is_mse_permissible = zeros(int(config["rules_creation"]["iterations_of_fitting"]))
    errors = zeros(int(config["rules_creation"]["iterations_of_fitting"]))

    threshhold = eval(config["rules_creation"]["threshhold"])

    for i in range(int(config["rules_creation"]["iterations_of_fitting"])):
        if hasattr(replacement, 'optimal_params'):
            delattr(replacement, 'optimal_params')
        if hasattr(pattern, 'optimal_params'):
            delattr(pattern, 'optimal_params')

        new_pattern = SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)
        #setattr(pattern, 'init_params', [ 0.94604228, -0.59267325,  0.72588573])
        #new_pattern = pattern

        print(new_pattern.init_params)
        data_to_fit = CreateDataToFit.create(new_pattern, config)
        # note, that we get fitted values, not a model!
        fitted_replace = FitModelToData.fit(replacement, data_to_fit, dict_tokens_info, config, do_plot)
        print(replacement.optimal_params)

        is_mse_permissible[i] = norm(data_to_fit[:,0] - fitted_replace) < threshhold
        errors[i] = norm(data_to_fit[:,0] - fitted_replace)

    print(is_mse_permissible)
    print(errors)

    is_fitted = sum(is_mse_permissible) > is_mse_permissible.shape[0] * float(config["rules_creation"]["fraction_of_misfittings"])
    if verbose:
        if is_fitted:
            print(replacement, "is fittable to the ", pattern)
        else:
            print(replacement, "is NOT fittable to the ", pattern)


    return is_fitted

