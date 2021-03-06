import os
from code.model_processing.StringToModel import strings_to_population
from code.structures.Population import Population
import inspect

def retrieve_init_models(config, source_of_launching = None):
    """
    Return data to fit from the folder specified in 'config'
    Inputs:
     config                 - data structure storing MVR attributes
     source_of_launching    - name of the file, from which its launching
    Outputs:
     init_models    - handles of the initial models from the specified file (list of strings)
    """

    DATA_FULL_PATH = construct_the_filename_with_init_models(config, source_of_launching)
    # extract the initial models
    initial_models = []

    for line in open(DATA_FULL_PATH):
        line = line.strip()
        # ignore those lines which are py-comments and empty lines
        if not (line.startswith("#") or len(line) == 0):
            initial_models.append(line)

    initial_models = strings_to_population(initial_models)
    initial_models = [model for model in initial_models if len(model) <= int(config["model_generation"]["maximum_complexity"])]
    list(map(lambda model: setattr(model, 'where_from', "init"), initial_models))


    return Population(initial_models)


def construct_the_filename_with_init_models(config, source_of_launching):
    if inspect.stack()[2][3] == "data_fitting" or source_of_launching == "DataFitting":
        DATA_LOCAL_PATH = config["data_extraction"]["init_models_filename"]
    elif config["flag_type_of_processing"]["flag"] == "rules_creation":
        DATA_LOCAL_PATH = config["rules_creation"]["rules_folder"]
        if config["rules_creation"]["regime"] == "create_patterns":
            DATA_LOCAL_PATH += config["rules_creation"]["init_replacements_filename"]
        elif config["rules_creation"]["regime"] == "create_replacements":
            DATA_LOCAL_PATH += config["rules_creation"]["init_patterns_filename"]
    else:
        DATA_LOCAL_PATH = config["data_extraction"]["init_models_filename"]

    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    return parent_dir + DATA_LOCAL_PATH