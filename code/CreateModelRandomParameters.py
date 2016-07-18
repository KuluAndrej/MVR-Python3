from code.modules.extract_model_tokens_encodings import extract_tokens
import re
import numpy as np
def random_parameters(model, dict_tokens_info, config):
    """
    Given 'model', we are to create a set of random parameters. We get into account, that
    each parameter is from its own specified range. Its range is written in
    'config["tokens_info"]["info_for_curve_fit"]'

    """

    random_parameters = np.zeros(model.number_of_parameters)

    processed_handle= re.sub(r'X\[(\d+)\]', r'x\1', model.handle)
    tokens = extract_tokens(processed_handle).split('&')

    inf_replace = config["rules_creation"]["inf_replace"]
    for token in tokens:
        if 