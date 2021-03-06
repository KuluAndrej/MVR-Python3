import code.estimators_selectors.Evaluator as Evaluator
import code.model_processing.Parametrizer as Parametrizer
import code.input_output.ConstructScipyOptimizeAttributes as ConstructScipyOptimizeAttributes
import code.estimators_selectors.CalculatorModelValues as CalculatorModelValues
import matplotlib.pyplot as plt
import  code.model_processing.DefConstructor as DefConstructor
import code.estimators_selectors.QualityEstimator as QualityEstimator
import code.ObserverTheBestFunction as ObserverTheBestFunction

from numpy import zeros

def fit(model, data_to_fit, dict_tokens_info, config, do_plot = True):
    """
    Fit model parameters to fit the data
    Inputs:
     model
     data_to_fit

    Outputs:
     model      - input model with set fitted parameters

    Author: Kulunchakov Andrei
    """
    population = [model]
    ConstructScipyOptimizeAttributes.construct_info_population(population,dict_tokens_info)
    population = Parametrizer.parametrize_population(population)
    DefConstructor.add_def_statements_attributes(population)
    population = Evaluator.evaluator(population, data_to_fit, config)
    population = QualityEstimator.quality_estimator(population, data_to_fit, config)

    fitted = CalculatorModelValues.calculate_model_values(population[0], data_to_fit[:,1:].T)

    if do_plot:
        try:
            ObserverTheBestFunction.observer_the_best_function(population,data_to_fit)

            return fitted

        except:

            plt.plot(data_to_fit[:,1], data_to_fit[:,0], 'b', data_to_fit[:,1], zeros(data_to_fit[:,0].shape), 'g')
            plt.show()

            return zeros(data_to_fit[:,0].shape)

    return fitted

