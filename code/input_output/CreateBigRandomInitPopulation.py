import code.genetic_operations.RandomPopulation as RandomPopulation
import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import os

def create_big_random_init_population(config, number_of_vars = 1):

    print_intro()
    if not config:
        config = MVRAttributesExtraction.extract_config()

    init_models = set(RandomPopulation.random_population(number_of_vars, config, True))

    while True:
        previous_size = len(init_models)
        init_models = init_models.union(RandomPopulation.random_population(number_of_vars, config, True))
        new_size = len(init_models)
        # we stop generation, when our set already contains the majority of newly generated models
        if (new_size - previous_size) / previous_size < .1:
            break

    DATA_FULL_PATH = construct_data_path(config)

    file = open(DATA_FULL_PATH, 'w')
    desired_numb_rows = int(config["init_rand_models"]["preferable_number_models"])
    for ind, item in enumerate(init_models):
        if desired_numb_rows > ind:
            if len(item) >= 2:
                file.write("%s\n" % item)

def construct_data_path(config):

    if config["init_rand_models"]["purpose"] == "rules_creation":
        DATA_LOCAL_PATH =  config["rules_creation"]["rules_folder"]
        if config["rules_creation"]["regime"] == "create_replacements":
            DATA_LOCAL_PATH += config["rules_creation"]["init_patterns_filename"]
        elif config["rules_creation"]["regime"] == "create_patterns":
            DATA_LOCAL_PATH += config["rules_creation"]["init_replacements_filename"]
    else:
        DATA_LOCAL_PATH = config["data_extraction"]["init_models_filename"]
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    print(DATA_FULL_PATH)
    return DATA_FULL_PATH

def print_intro():
    print("Start creation of initial models")

