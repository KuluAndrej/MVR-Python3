import code.MutationPopulation as MutationPopulation
import code.Parametrizer as Parametrizer
import code.QualityEstimator as QualityEstimator
import code.RandomPopulation as RandomPopulation
import code.SelectBestModels as SelectBestModels
import code.Evaluator as Evaluator
import code.InitModelsLoader as InitModelsLoader
import code.CrossoverPopulation as CrossoverPopulation

def data_fitting(data_to_fit, config):
    """
    Fit given data by superpositions of primitive functions

    Inputs:
     data_to_fit
     config   - parameters of MVR

    Outputs:
     population      - population of new superpositions produced by mutations
    """

    # automatically detect and extract the number of features from the given data

    number_of_variables = data_to_fit.shape[-1] - 1

    population  = InitModelsLoader.retrieve_init_models(config)
    population  = Parametrizer.parametrize_population(population)

    config_for_generation = config["model_generation"]
    config_for_accuracy   = config["accuracy_requirement"]

    for i in range(int(config_for_accuracy["max_number_cycle_count"])):
        #print("iteration# ", i)
        population.append(CrossoverPopulation.crossover_population(population, config_for_generation["crossing_number"]))
        population.append(MutationPopulation.mutate_population(population, config_for_generation["mutation_number"], number_of_variables))
        population.append(RandomPopulation.random_population(config_for_generation["random_models_number"], number_of_variables, int(config_for_generation["random_models_complexity"])))

        population.unique_models_selection()


        population = Parametrizer.parametrize_population(population)
        population = Evaluator.evaluator(population, data_to_fit, config_for_generation["is_parametric"])
        population = QualityEstimator.quality_estimator(population, data_to_fit)


        population = SelectBestModels.select_best_models(population, config_for_generation["best_models_number"], config_for_generation["type_selection"])

        """
        print(len(population), " models are selected")
        print("best yet generated model", population[0].MSE)
        print(population[0].handle)
        if hasattr(population[0], "optimal_params"):
            print(population[0].optimal_params)
        else:
            print("no params")

        print("")
        """
        if population[0].MSE <= int(config_for_accuracy["required_accuracy"]):
            break

    return population