import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.DataFitting as DataFitting
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
import code.input_output.SaveRule as SaveRule

from configparser import ConfigParser
def creator(pattern, dict_tokens_info, config):
    """
    Gets a 'model' and creates rules, where this model acts as the 'replacement' model.
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """
    print_intro(pattern)

    SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)

    data_to_fit = CreateDataToFit.create(pattern, config)
    tuned_config = tune_config_for_replacement_fitting(config, pattern)

    for i in range(int(config["rules_creation"]["iterations_of_fitting"])):
        best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config)

        for replacement in best_found_replacements:
            if CheckReplacementForFitting.check(pattern, replacement, dict_tokens_info, config, do_plot=False, verbose=True):
                    SaveRule.store(pattern, replacement, config)

    print("...processed")

def tune_config_for_replacement_fitting(config, pattern):
    # copy 'config' file and change some attributes for correct work of replacements creation
    # Inputs:
    #   config      - config file to copy
    #   length      - length of pattern to which we fit replacements
    # Outputs:
    #   tuned_config

    tuned_config = ConfigParser()
    tuned_config.read_dict(config)
    tuned_config["model_generation"]["maximum_complexity"] = str(len(pattern)- 1)
    tuned_config["model_generation"]["maximum_param_number"] = str(pattern.number_of_parameters - 1)
    tuned_config["model_generation"]["size_init_random_models"] = str(3 * len(pattern) - 1)

    tuned_config["model_generation"]["number_of_init_random_models"] = str(1000)

    tuned_config["model_generation"]["type_selection"] = "MSE"


    return tuned_config

def print_intro(pattern):
    print("Start processing pattern: ", pattern)
