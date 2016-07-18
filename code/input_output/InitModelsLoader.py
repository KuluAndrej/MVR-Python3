import os
from code.model_processing.StringToModel import strings_to_population
from code.structures.Population import Population
def retrieve_init_models(config):
    """
    Return data to fit from the folder specified in 'config'
    Inputs:
     config         - data structure storing MVR attributes

    Outputs:
     init_models    - handles of the initial models from the specified file (list of strings)
    """
    if config["flag_type_of_processing"]["flag"] == "rules_creation":
        DATA_LOCAL_PATH = config["rules_creation"]["rules_folder"]

        if config["rules_creation"]["regime"] == "create_patterns":
            DATA_LOCAL_PATH += config["rules_creation"]["init_replacements_filename"]
        elif config["rules_creation"]["regime"] == "create_replacements":
            DATA_LOCAL_PATH += config["rules_creation"]["init_patterns_filename"]
    else:
        DATA_LOCAL_PATH = config["data_extraction"]["init_models_filename"]

    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    # extract the initial models
    initial_models = []

    for line in open(DATA_FULL_PATH):
        line = line.strip()
        # ignore those lines which are py-comments and empty lines
        if not (line.startswith("#") or len(line) == 0):
            initial_models.append(line)

    initial_models = strings_to_population(initial_models)
    list(map(lambda model: setattr(model, 'where_from', "init"), initial_models))

    return Population(initial_models)