import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.DataFitting as DataFitting
from configparser import ConfigParser
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
import code.input_output.SaveRule as SaveRule
def creator(pattern, dict_tokens_info, config):
    """
    Gets a 'model' and creates rules, where this model acts as the 'replacement' model.
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """

    print("Start processing pattern: ", pattern)
    SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)


    data_to_fit = CreateDataToFit.create(pattern, config)


    tuned_config = ConfigParser()
    tuned_config.read_dict(config)
    tuned_config["model_generation"]["maximum_complexity"] = str(len(pattern) - 1)
    tuned_config["model_generation"]["size_init_random_models"] = str(3 * len(pattern) - 1)
    tuned_config["model_generation"]["number_of_init_random_models"] = str(1000)
    tuned_config["model_generation"]["type_selection"] = "MSE"

    for i in range(int(config["rules_creation"]["iterations_of_fitting"])):
        best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config)
        print(best_found_replacements[0:3], sep = '\n')
        for replacement in best_found_replacements:
            if CheckReplacementForFitting.check(pattern, replacement, dict_tokens_info, config):
                print("Replacement is fittable to the pattern")

                # now we swap pattern and replacement to check if the pattern is also able to fit the replacement
                # with any set of parameters
                if CheckReplacementForFitting.check(replacement, pattern, dict_tokens_info, config):
                    print("Pattern is fittable to the replacement")
                    SaveRule.store(pattern, replacement, config)

    print("...processed")