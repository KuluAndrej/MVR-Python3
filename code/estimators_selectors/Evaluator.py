from code.DefConstructor import def_constructor
from scipy.optimize import  curve_fit
from numpy import nan, ones
from scipy.optimize import OptimizeWarning
import numpy as np

def evaluator(population, data_to_fit, dict_tokens_info, config):
    """
    Evaluate the optimal parameters for each model from the population
    Inputs:
     population                                         - list of Models to evaluate
     data_to_fit                                        - approximated data; necessary for the quality determination
     dict_tokens_info                                   - info about parameters of tokens used in optimization
     config.model_generation.is_parametric              - flag signifying if the parameters of superpositions will be tuned
     config.model_generation.maximum_param_number       - specifies maximum number of parameters
     config.model_generation.maximum_complexity         - specifies maximum structural complexity of a model
    Outputs:
     population         - estimated population

    Author: Kulunchakov Andrei, MIPT
    """

    is_parametric = config["model_generation"]["is_parametric"]
    maximum_param_number = int(config["model_generation"]["maximum_param_number"])
    maximum_complexity = int(config["model_generation"]["maximum_complexity"])

    # split given data on dependent variables and independent one
    independent_var = data_to_fit[:,1:]
    independent_var = tuple(independent_var[:,column] for column in range(independent_var.shape[1]))
    #independent_var = (independent_var[:,0], independent_var[:,1])
    dependent_var = data_to_fit[:,0]


    for model in population:
        if (not hasattr(model, "def_statement")):
            def_repr = def_constructor(model)
            setattr(model, "def_statement", def_repr)
        if (model.number_of_parameters > maximum_param_number or len(model) > maximum_complexity):
            setattr(model, "is_deprecated", True)
            continue

        import warnings

        def fxn():
            warnings.warn("deprecated", DeprecationWarning)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fxn()
            if (is_parametric == 'True' and (not hasattr(model, "optimal_params")) and model.number_of_parameters > 0):
                try:
                    #, model.curve_fit_init_params, model.curve_fit_bounds
                    popt, _ = curve_fit(model.def_statement, independent_var, dependent_var,\
                                        p0 = model.curve_fit_init_params, bounds=model.curve_fit_bounds)
                except RuntimeError:
                    popt = [nan for i in range(model.number_of_parameters)]
                except RuntimeWarning:
                    popt = [nan for i in range(model.number_of_parameters)]
                except OptimizeWarning:
                    popt = [nan for i in range(model.number_of_parameters)]
                except ZeroDivisionError:
                    popt = [nan for i in range(model.number_of_parameters)]
                except ValueError:
                    popt = [nan for i in range(model.number_of_parameters)]
                except IndexError:
                    if hasattr(model, "backup_handle"):
                        print("problem with simplification:")
                        print(model.backup_handle,'-->',model.handle)
                    else:
                        print("problem NOT with simplification")
                        print(model)
                    raise
                setattr(model, "optimal_params", popt)
                continue
            else:
                if not hasattr(model, "optimal_params"):
                    setattr(model, "optimal_params", ones(model.number_of_parameters))

        if model.number_of_parameters == 0:
            model.def_statement_param = model.def_statement

    return population