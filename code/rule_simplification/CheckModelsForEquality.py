import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting


def check(first_model, second_model, dict_tokens_info, config):
    """
    Find if the first model is equivalent to the second

    Author: Kulunchakov Andrei
    """

    if CheckReplacementForFitting.check(first_model, second_model, dict_tokens_info, config, do_plot=False, verbose=True):
        # now we swap first_model and second_model to check if the first_model is also able to fit
        # the second_model with any set of parameters
        if CheckReplacementForFitting.check(second_model, first_model, dict_tokens_info, config, verbose=True):
            return True

    return False