import code.model_processing.SetModelRandomParameters as SetModelRandomParameters
import code.rule_simplification.CreateDataToFit as CreateDataToFit
import code.DataFitting as DataFitting
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
import code.input_output.SaveRule as SaveRule
from code.structures.Population import Population
from configparser import ConfigParser
from numpy import nan, isnan, isinf


def creator(pattern, init_models_to_fit, dict_tokens_info, config):
    """
    Gets a 'model' and creates rules, where this model acts as the 'replacement' model.
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """
    print_intro(pattern)
    # prepare initial population

    SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)
    data_to_fit = CreateDataToFit.create(pattern, config)
    tuned_config = tune_config_for_replacement_fitting(config, pattern)

    if not check_correctness(data_to_fit):
        return

    proper_init_models = filter_init_models(init_models_to_fit, pattern)
    best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config,\
                                                       dict_tokens_info, proper_init_models)

    for replacement in best_found_replacements:
        if CheckReplacementForFitting.check(pattern, replacement, dict_tokens_info, config, do_plot=False, verbose=False)[0]:
            SaveRule.store(pattern, replacement, config, verbose=True)
            break

    clearUnnecessaryAttributes(init_models_to_fit)
    print("...processed")

def filter_init_models(init_models_to_fit, pattern):
    number_of_parameters = pattern.number_of_parameters
    proper_length = len(pattern)

    proper_models = []
    for model in init_models_to_fit:
        if len(model) < proper_length and model.number_of_terminals < number_of_parameters:
            if model.vars[0] <= pattern.vars[0] and model.vars[1] <= pattern.vars[1]:
                if model.vars[0] >= model.vars[1]:
                    proper_models.append(model)
    return Population(proper_models)

def clearUnnecessaryAttributes(init_models_to_fit):
    # To maintain correct flow of the program, we should remove all attributes, which
    # were set to initial population in Evaluator in DataFitting, namely "optimal_params"
    for model in init_models_to_fit:
        if hasattr(model, "optimal_params"):
            delattr(model, "optimal_params")


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
    tuned_config["model_generation"]["maximum_param_number"] = str(pattern.number_of_parameters)
    tuned_config["model_generation"]["size_init_random_models"] = str(3 * len(pattern) - 1)

    tuned_config["model_generation"]["number_of_init_random_models"] = str(1000)

    tuned_config["model_generation"]["type_selection"] = "MSE"


    return tuned_config

def print_intro(pattern):
    print("Start processing pattern: ", pattern)

def check_correctness(data_to_fit):
    if isnan(data_to_fit[0,0]) or isinf(data_to_fit[0,0]):
        print("Incorrect values:",data_to_fit[0,0], " are produced")
        return False

    return True