import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.model_processing.FitModelToData as FitModelToData
from code.model_processing.StringToModel import strings_to_population
from numpy import zeros
from numpy.linalg import norm
def check(pattern, replacement, dict_tokens_info, config):
    """
    Once the replacement is fit for one realization of random parameters of pattern, we launch
    multistart procedure on this set. Namely, we get several new realization of this set and check
    similarity for each realization

    Author: Kulunchakov Andrei

    """

    is_mse_permissible = zeros(int(config["rules_creation"]["iterations_of_fitting"]))
    threshhold = eval(config["rules_creation"]["threshhold"])

    for i in range(int(config["rules_creation"]["iterations_of_fitting"])):

        new_pattern = SetModelRandomParameters.random_parameters(pattern, dict_tokens_info, config)
        data_to_fit = CreateDataToFit.create(new_pattern, config)

        # note, that we get fitted values, not a model!
        fitted_replace = FitModelToData.fit(replacement, data_to_fit, dict_tokens_info, config)
        is_mse_permissible[i] = norm(data_to_fit[:,0] - fitted_replace) < threshhold

    return sum(is_mse_permissible) < is_mse_permissible.shape[0] * float(config["rules_creation"]["fraction_of_misfittings"])

