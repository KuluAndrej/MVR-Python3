import  code.model_processing.DefConstructor as DefConstructor
import  code.estimators_selectors.QualityEstimator as QualityEstimator
from scipy.optimize import  curve_fit
from numpy import nan, ones, inf, random, isnan
from scipy.optimize import OptimizeWarning
import time
def evaluator(population, data_to_fit, config):
    """
    Evaluate the optimal parameters for each model from the population
    Inputs:
     population                                         - list of Models to evaluate
     data_to_fit                                        - approximated data; necessary for the quality determination
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
            def_repr = DefConstructor.def_constructor(model)
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
                is_multistart = eval(config["model_generation"]["multistart"])
                bounds_included = eval(config["model_generation"]["bounds_included"])
                if is_multistart:
                    number_of_iterations = eval(config["model_generation"]["iterations_multistart"])
                else:
                    number_of_iterations = 1

                best_fit_params = []
                best_MSE = inf
                for i in range(number_of_iterations):
                    try:
                        #, model.curve_fit_init_params, model.curve_fit_bounds
                        if is_multistart:
                            model.curve_fit_init_params = 2 * random.rand(len(model.curve_fit_init_params)) - 1
                        if bounds_included:
                            popt, _ = curve_fit(model.def_statement, independent_var, dependent_var,\
                                            p0 = model.curve_fit_init_params, bounds=model.curve_fit_bounds, \
                                            ftol=0.01, xtol=0.01)
                        else:
                            try:
                                popt, _ = curve_fit(model.def_statement, independent_var, dependent_var,\
                                                p0 = model.curve_fit_init_params, \
                                                ftol=0.01, xtol=0.01)
                            except TypeError:
                                print(model)
                                raise

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
                    QualityEstimator.quality_estimator([model], data_to_fit, config)
                    if not isnan(model.MSE) and best_MSE > model.MSE:
                        best_MSE = model.MSE
                        best_fit_params = popt
                setattr(model, "optimal_params", best_fit_params)
                continue
            else:
                if not hasattr(model, "optimal_params"):
                    setattr(model, "optimal_params", ones(model.number_of_parameters))

        if model.number_of_parameters == 0:
            model.def_statement_param = model.def_statement

    return population


"""
def evaluator(population, data_to_fit, config):
    for model in population:
        evaluatorModel(model, data_to_fit, config)

    print("start_evaluating")
    st = time.time()

    num_args = len(population)
    #args = list(zip(population, itertools.repeat(data_to_fit, num_args), itertools.repeat(config, num_args)))
    #jobs = []
    pool = multiprocessing.Pool(2)

    # Open the urls in their own threads
    # and return the results
    results = pool.map(partial(evaluatorModel, data_to_fit=data_to_fit, config = config), population)

    #close the pool and wait for the work to finish
    pool.close()
    pool.join()

    for i in range(num_args):
        p = multiprocessing.Pool(target=evaluatorModel, args=args[i])
        jobs.append(p)
        p.start()

    #print(jobs[0])
    #print(time.time() - st)

    return population

def evaluatorModel(model, data_to_fit, config):

    Evaluate the optimal parameters for each model from the population
    Inputs:
     population                                         - list of Models to evaluate
     data_to_fit                                        - approximated data; necessary for the quality determination
     config.model_generation.is_parametric              - flag signifying if the parameters of superpositions will be tuned
     config.model_generation.maximum_param_number       - specifies maximum number of parameters
     config.model_generation.maximum_complexity         - specifies maximum structural complexity of a model
    Outputs:
     population         - estimated population

    Author: Kulunchakov Andrei, MIPT
    ""

    is_parametric = config["model_generation"]["is_parametric"]
    maximum_param_number = int(config["model_generation"]["maximum_param_number"])
    maximum_complexity = int(config["model_generation"]["maximum_complexity"])

    # split given data on dependent variables and independent one
    independent_var = data_to_fit[:,1:]
    independent_var = tuple(independent_var[:,column] for column in range(independent_var.shape[1]))
    #independent_var = (independent_var[:,0], independent_var[:,1])
    dependent_var = data_to_fit[:,0]

    if (not hasattr(model, "def_statement")):
        def_repr = DefConstructor.def_constructor(model)
        setattr(model, "def_statement", def_repr)
    if (model.number_of_parameters > maximum_param_number or len(model) > maximum_complexity):
        setattr(model, "is_deprecated", True)
        return model

    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        if (is_parametric == 'True' and (not hasattr(model, "optimal_params")) and model.number_of_parameters > 0):
            is_multistart = eval(config["model_generation"]["multistart"])
            bounds_included = eval(config["model_generation"]["bounds_included"])
            if is_multistart:
                number_of_iterations = eval(config["model_generation"]["iterations_multistart"])
            else:
                number_of_iterations = 1

            best_fit_params = []
            best_MSE = inf
            for i in range(number_of_iterations):
                try:
                    #, model.curve_fit_init_params, model.curve_fit_bounds
                    if is_multistart:
                        model.curve_fit_init_params = 2 * random.rand(len(model.curve_fit_init_params)) - 1
                    if bounds_included:
                        popt, _ = curve_fit(model.def_statement, independent_var, dependent_var,\
                                        p0 = model.curve_fit_init_params, bounds=model.curve_fit_bounds)
                    else:
                        try:
                            popt, _ = curve_fit(model.def_statement, independent_var, dependent_var,\
                                            p0 = model.curve_fit_init_params)
                        except:
                            print(model)
                            print(model.str_func)
                            raise
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
                QualityEstimator.quality_estimator([model], data_to_fit, config)
                if not isnan(model.MSE) and best_MSE > model.MSE:
                    best_MSE = model.MSE
                    best_fit_params = popt
            setattr(model, "optimal_params", best_fit_params)

            return model
        else:
            if not hasattr(model, "optimal_params"):
                setattr(model, "optimal_params", ones(model.number_of_parameters))

    if model.number_of_parameters == 0:
        model.def_statement_param = model.def_statement

    return model
"""
