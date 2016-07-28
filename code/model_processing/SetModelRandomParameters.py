from code.modules.extract_model_tokens_encodings import extract_tokens
import re
import numpy as np
def set_random_parameters(model, dict_tokens_info, config):
    """
    Given 'model', we are to create a set of random parameters. We get into account, that
    each parameter is from its own specified range. Its range is written in
    'config["tokens_info"]["info_for_curve_fit"]'

    """

    random_parameters = np.zeros(model.number_of_parameters)

    processed_handle= re.sub(r'X\[(\d+)\]', r'x\1', model.handle)
    tokens = extract_tokens(processed_handle).split('&')

    inf_replace = float(config["rules_creation"]["inf_replace"])
    cur_pos_in_random_parameters = 0
    for token in tokens:
        if is_var(token):
            continue
        bounds = dict_tokens_info[token][1]
        numb_token_params = len(bounds[0])
        # if the token is parametric
        if numb_token_params:
            for i in range(numb_token_params):
                left_bound  = bounds[0][i] if not np.isinf(bounds[0][i]) else inf_replace * np.sign(bounds[0][i])
                right_bound = bounds[1][i] if not np.isinf(bounds[1][i]) else inf_replace * np.sign(bounds[1][i])
                rand_param  = np.random.uniform(left_bound, right_bound)
                random_parameters[cur_pos_in_random_parameters + i] = rand_param
            cur_pos_in_random_parameters += numb_token_params

    setattr(model, "init_params", random_parameters)
    return model

def is_var(token):
    return re.match(r'x(\d+)', token)