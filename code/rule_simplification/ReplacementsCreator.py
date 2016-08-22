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

    # prepare initial population
    SetModelRandomParameters.set_random_parameters(pattern, dict_tokens_info, config)
    data_to_fit = CreateDataToFit.create(pattern, config)
    tuned_config = tune_config_for_replacement_fitting(config, pattern)

    if not check_correctness(data_to_fit):
        return

    proper_init_models = filter_init_models(init_models_to_fit, pattern)
    best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config,\
                                                       dict_tokens_info, proper_init_models)
    for iter in range(3):
        best_found_replacements = DataFitting.data_fitting(data_to_fit, tuned_config,\
                                                       dict_tokens_info, best_found_replacements, verbose = False)
        best_found_replacements = best_found_replacements[0:max(2,len(best_found_replacements)//2)]

    best_found_replacements = select_the_top_models(best_found_replacements)
    best_found_replacements.sort(type_of_selection='len_param')

    for replacement in best_found_replacements[0:3]:
        if CheckReplacementForFitting.check(pattern, replacement, dict_tokens_info, tune_config_for_replacement_checking(config), do_plot=False, verbose=False)[0]:
            SaveRule.store(pattern, replacement, config, verbose=True)
            clearUnnecessaryAttributes(init_models_to_fit)
            clearUnnecessaryAttributes(best_found_replacements)
            return True

    clearUnnecessaryAttributes(init_models_to_fit)
    clearUnnecessaryAttributes(best_found_replacements)
    return False

def select_the_top_models(best_found_replacements):
    bestMSE = best_found_replacements[0].MSE
    percent_deviation_acceptable = 0.1
    boundForMSE = bestMSE * (1 + percent_deviation_acceptable)
    current_index = 0
    while current_index < len(best_found_replacements) and best_found_replacements[current_index].MSE <= boundForMSE:
        current_index += 1

    return best_found_replacements[0:current_index]

def filter_init_models(init_models_to_fit, pattern):
    number_of_parameters = pattern.number_of_parameters
    proper_length = len(pattern)

    proper_models = []
    for model in init_models_to_fit:
        if len(model) < proper_length and model.number_of_parameters <= number_of_parameters:
            if model.vars[0] <= pattern.vars[0] and model.vars[1] <= pattern.vars[1]:
                if model.vars[0] >= model.vars[1]:
                    proper_models.append(model)

    return Population(proper_models)

def clearUnnecessaryAttributes(init_models_to_fit):
    # To maintain correct flow of the program, we should remove all attributes, which
    # were set to initial population in Evaluator in DataFitting, namely "optimal_params"
    for ind in range(len(init_models_to_fit)):
        if hasattr(init_models_to_fit[ind], "optimal_params"):
            delattr(init_models_to_fit[ind], "optimal_params")
        if hasattr(init_models_to_fit[ind], "MSE"):
            delattr(init_models_to_fit[ind], "MSE")
    return init_models_to_fit

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

def tune_config_for_replacement_checking(config):
    # copy 'config' file and change some attributes for correct work of checking creation
    # we increase the number of iterations of parameters evaluation procedure
    # Inputs:
    #   config      - config file to copy
    # Outputs:
    #   tuned_config

    tuned_config = ConfigParser()
    tuned_config.read_dict(config)
    tuned_config["model_generation"]["iterations_multistart"] = str(20)

    return tuned_config


def check_correctness(data_to_fit):
    if isnan(data_to_fit[0,0]) or isinf(data_to_fit[0,0]):
        print("Incorrect values:",data_to_fit[0,0], " are produced")
        return False

    return True