import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.DataFitting as DataFitting
import code.model_processing.FitModelToData as FitModelToData
from configparser import ConfigParser
from code.model_processing.StringToModel import strings_to_population
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
def creator(pattern, dict_tokens_info, config):
    """
    Gets a 'model' and creates rules, where this model acts as the 'replacement' model.
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """


    pattern = SetModelRandomParameters.random_parameters(pattern, dict_tokens_info, config)
    data_to_fit = CreateDataToFit.create(pattern, config)

    print(pattern, '\n', repr(pattern.init_params), sep = '')



    model_replacement = 'lnl_(X[0])'
    fitted_replace = FitModelToData.fit(strings_to_population([model_replacement]), data_to_fit, dict_tokens_info, config)


    tuned_config = ConfigParser().read_dict(config)
    tuned_config["model_generation"]["maximum_complexity"] = str(len(pattern) - 1)
    tuned_config["model_generation"]["size_init_random_models"] = str(len(pattern) - 1)
    tuned_config["model_generation"]["size_init_random_models"] = 1000

    for i in range(int(config["model_generation"]["iterations_of_fitting"])):
        best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config)

        for replacement in best_found_replacements:
            CheckReplacementForFitting.check(pattern, replacement, dict_tokens_info, config)

