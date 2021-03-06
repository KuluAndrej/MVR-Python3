import os
import code.structures.Model as Model
def store(pattern, replacement, config, verbose=False):
    """

    Author: Kulunchakov Andrei
    """

    filename_folder = config["rules_creation"]["rules_folder"]
    filename = filename_folder + config["rules_creation"]["rules_filename"]

    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + filename

    with open(DATA_FULL_PATH, "a") as file:
        file.write(pattern.handle + " " + replacement.handle + '\n')

    if verbose:
        print("wrote the rule", pattern, "->", replacement)
