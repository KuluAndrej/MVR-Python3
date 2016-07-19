import code.genetic_operations.RandomPopulation as RandomPopulation
import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import os

def create_big_random_init_population(config):
    if not config:
        config = MVRAttributesExtraction.extract_config()
    init_models = set(RandomPopulation.random_population(1, config, True))

    while True:
        previous_size = len(init_models)
        init_models = init_models.union(RandomPopulation.random_population(1, config, True))
        new_size = len(init_models)

        if (new_size - previous_size) / previous_size < .1:
            break

    DATA_LOCAL_PATH = config["data_extraction"]["init_models_filename"]


    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH
    file = open(DATA_FULL_PATH, 'w')
    desired_numb_rows = 300
    for ind, item in enumerate(init_models):
        if desired_numb_rows > ind:
            file.write("%s\n" % item)