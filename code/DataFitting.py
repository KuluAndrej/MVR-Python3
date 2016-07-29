import code.genetic_operations.MutationPopulation as MutationPopulation
import code.model_processing.Parametrizer as Parametrizer
import code.estimators_selectors.QualityEstimator as QualityEstimator
import code.genetic_operations.RandomPopulation as RandomPopulation
import code.estimators_selectors.SelectBestModels as SelectBestModels
import code.estimators_selectors.Evaluator as Evaluator
import code.input_output.InitModelsLoader as InitModelsLoader
import code.genetic_operations.CrossoverPopulation as CrossoverPopulation
import code.input_output.ConstructScipyOptimizeAttributes as ConstructScipyOptimizeAttributes
import code.rule_simplification.RuleSimplifier as RuleSimplifier
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.structures.Population as Population
import code.input_output.CreateBigRandomInitPopulation as CreateBigRandomInitPopulation

from numpy import zeros

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
    print("Start data fitting\nNote that the first iteration takes a bit longer than the others")

    # some useful constants for stagnation recognition
    lowest_possible_rate = eval(config["stagnation"]["lowest_possible_rate"])
    window_size          = eval(config["stagnation"]["window_size"])
    init_iteration       = eval(config["stagnation"]["init_iteration"])
    # measurements stands for plotting the dynamics of MSE
    measurements = zeros(int(config["accuracy_requirement"]["max_number_cycle_count"]) + 1)


    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)
    number_of_variables = data_to_fit.shape[-1] - 1


    if eval(config["init_rand_models"]["do_init_random_generation"]):
        CreateBigRandomInitPopulation.create_big_random_init_population(config)

    population = InitModelsLoader.retrieve_init_models(config, source_of_launching="DataFitting")
    for i in range(int(config["accuracy_requirement"]["max_number_cycle_count"])):
        print_intro(config, i)
        if i > 0:
            measurements[i] = population[0].MSE

        if i > init_iteration and (measurements[max(i - window_size,0)] - measurements[i])/measurements[i] < lowest_possible_rate:
            print("break on iteration #", i, "because of stagnation")
            break

        population.append(CrossoverPopulation.crossover_population(population, config))
        population.append(MutationPopulation.mutate_population(population, number_of_variables, config))
        population.append(RandomPopulation.random_population(number_of_variables, config, False))
        population.unique_models_selection()

        population = RuleSimplifier.rule_simplify(population)
        # NOTE THAT IT CAN RUIN YOUR CLASSIFICATION MACHINE
        # STAY CAREFUL
        population.unique_models_selection()


        ConstructScipyOptimizeAttributes.construct_info_population(population,dict_tokens_info)
        population = Parametrizer.parametrize_population(population)
        population = Evaluator.evaluator(population, data_to_fit, config)
        population = QualityEstimator.quality_estimator(population, data_to_fit, config)


        population = SelectBestModels.select_best_models(population, config)
        print_results(population, config, i)

    print(population[0:3], sep = '\n')
    if config["flag_type_of_processing"]["flag"] == 'fit_data':
        return population, measurements
    else:
        return population

def print_intro(config, number_of_iteration):
    if config["flag_type_of_processing"]["flag"] == 'fit_data':
            print("iteration on fitting #", number_of_iteration, sep='')


def print_results(population, config, number_of_iteration):
    if config["flag_type_of_processing"]["flag"] == 'fit_data':
        print(len(population), " models are selected")
        print("best yet generated model", population[0].MSE)
        for ind in range(3):
            print(population[ind], "has MSE", population[ind].MSE)
            if hasattr(population[ind],'optimal_params'):
                print(population[ind].optimal_params)
        print("")
        return

    if config["flag_type_of_processing"]["flag"] == 'fit_data' and \
                    population[0].MSE < float(config["accuracy_requirement"]["required_accuracy"]):
        print("break on cycle #", number_of_iteration)
        return