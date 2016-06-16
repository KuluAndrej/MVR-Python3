import code.MutationPopulation as MutationPopulation
import code.Parametrizer as Parametrizer
import code.QualityEstimator as QualityEstimator
import code.RandomPopulation as RandomPopulation
import code.SelectBestModels as SelectBestModels
import code.Evaluator as Evaluator
import code.InitModelsLoader as InitModelsLoader
import code.CrossoverPopulation as CrossoverPopulation
import code.SaveData as SaveData
from numpy import array
def data_fitting(data_to_fit, config):
    """
    Fit given data by superpositions of primitive functions

    Inputs:
     data_to_fit
     config   - parameters of MVR

    Outputs:
     population      - population of new superpositions produced by mutations

    Author: Kulunchakov Andrei, MIPT
    """

    # automatically detect and extract the number of features from the given data
    number_of_variables = data_to_fit.shape[-1] - 1

    population  = InitModelsLoader.retrieve_init_models(config)
    population  = Parametrizer.parametrize_population(population)


    for i in range(int(config["accuracy_requirement"]["max_number_cycle_count"])):
        if config["flag_type_of_processing"]["flag"] == 'fit_data':
            print("iteration on fitting# ", i)
        population.append(CrossoverPopulation.crossover_population(population, config))
        population.append(MutationPopulation.mutate_population(population, number_of_variables, config))
        population.append(RandomPopulation.random_population(number_of_variables, config))
        population.unique_models_selection()


        population = Parametrizer.parametrize_population(population)
        population = Evaluator.evaluator(population, data_to_fit, config)
        population = QualityEstimator.quality_estimator(population, data_to_fit)



        population = SelectBestModels.select_best_models(population, config)

        """
        print(len(population), " models are selected")
        print("best yet generated model", population[0].MSE)
        for ind, model in enumerate(population):
            if ind < 7:
                print(model, "has MSE", model.MSE)

        print("")
        """
    """
    print("best generated model has MSE = ", population[0].MSE)
    print("optimal parameters = ", population[0].optimal_params)
    """
    return population