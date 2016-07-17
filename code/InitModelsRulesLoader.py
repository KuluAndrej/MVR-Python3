"""
Function for extracting models from a file specified by 'config'.
The successive rules creation are based on these models.
There are utilized either as the replacement models for the future rules or pattern models.
The type of the utilization is specified by 'regime'.

Author: Kulunchakov Andrei
"""

def loader(config):
    filename_root = config['rules_creation']['rules_folder']
    regime   = config['rules_creation']['regime']

    if regime == 'create_replacements':
        filename = filename_root + config['rules_creation']['init_patterns_filename']
    elif regime == 'create_patterns':
        filename = filename_root + config['rules_creation']['init_replacements_filename']
    else:
        raise("regime of rules creation is not set")

    models = open(filename, 'r').readlines()
    models = list(map(lambda x: x.strip(), models))

    return models