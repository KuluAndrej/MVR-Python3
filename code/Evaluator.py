from code.DefConstructor import def_constructor
from scipy.optimize import  curve_fit
from numpy import nan, ones
from scipy.optimize import OptimizeWarning


def evaluator(population, data_to_fit, config):
    """
    Evaluate the optimal parameters for each model from the population
    Inputs:
     population                                         - list of Models to evaluate
     data_to_fit                                        - approximated data; necessary for the quality determination
     config.model_generation.is_parametric              - flag signifying if the parameters of superpositions will be tuned
     config.model_generation.maximum_param_number       - specifies maximum number of parameters
    Outputs:
     population         - estimated population
    """

    is_parametric = config["model_generation"]["is_parametric"]
    maximum_param_number = int(config["model_generation"]["maximum_param_number"])

    # split given data on dependent variables and independent one
    independent_var = data_to_fit[:,1:]
    independent_var = tuple(independent_var[:,column] for column in range(independent_var.shape[1]))
    #independent_var = (independent_var[:,0], independent_var[:,1])
    dependent_var = data_to_fit[:,0]


    for model in population:
        if (not hasattr(model, "def_statement")):
            def_repr = def_constructor(model)
            setattr(model, "def_statement", def_repr)
        if (model.number_of_parameters > maximum_param_number):
            setattr(model, "is_deprecated", True)
            continue

        import warnings

        def fxn():
            warnings.warn("deprecated", DeprecationWarning)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            fxn()
            if (is_parametric == 'True' and not hasattr(model, "optimal_params") and model.number_of_parameters > 0):
                try:
                    popt, _ = curve_fit(model.def_statement, independent_var, dependent_var)
                except RuntimeError:
                    popt = [nan for i in range(model.number_of_parameters)]
                except RuntimeWarning:
                    popt = [nan for i in range(model.number_of_parameters)]
                except OptimizeWarning:
                    popt = [nan for i in range(model.number_of_parameters)]
                setattr(model, "optimal_params", popt)
                continue
            else:
                setattr(model, "optimal_params", ones(model.number_of_parameters))

        if model.number_of_parameters == 0:
            model.def_statement_param = model.def_statement

    return population