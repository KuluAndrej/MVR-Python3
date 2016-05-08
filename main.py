import cProfile


import code.CrossoverPopulation as CrossoverPopulation
import code.DataLoader as DataLoader
import code.Evaluator as Evaluator
import code.InitModelsLoader as InitModelsLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.MutationPopulation as MutationPopulation
import code.Parametrizer as Parametrizer
import code.QualityEstimator as QualityEstimator
import code.RandomPopulation as RandomPopulation
import code.SelectBestModels as SelectBestModels
import code.StringToModel as StringToModel
import code.UniqueModelsSelection as UniqueModelsSelection
import  code.DataPreprocesser as DataPreprocesser

pr = cProfile.Profile()
pr.enable()
# get a data structure with the MVR attributes
config = MVRAttributesExtraction.attributes_extraction()


data_to_fit = DataLoader.retrieve_data(config)
data_to_fit = DataPreprocesser.data_preprocesser(data_to_fit)
print(data_to_fit.shape)
# automatically detect and extract the number of features from the given data
number_of_variables = data_to_fit.shape[1] - 1

population  = InitModelsLoader.retrieve_init_models(config)

population  = Parametrizer.parametrize_population(population)

config_for_generation = config["model_generation"]
config_for_accuracy   = config["accuracy_requirement"]
for i in range(int(config_for_accuracy["max_number_cycle_count"])):
    print("iteration# ", i)
    populationCross  = CrossoverPopulation.crossover_population(population, config_for_generation["crossing_number"])
    populationMutate = MutationPopulation.mutate_population(populationCross, config_for_generation["mutation_number"], number_of_variables)
    populationRandom = RandomPopulation.random_population(config_for_generation["random_models_number"], number_of_variables, 10)

    population = population + populationCross
    population = population + populationMutate
    population = population + populationRandom

    population = UniqueModelsSelection.unique_models_selection(population)


    population = Parametrizer.parametrize_population(population)
    population = Evaluator.evaluator(population, data_to_fit)
    population = QualityEstimator.quality_estimator(population, data_to_fit)
    population = SelectBestModels.select_best_models(population, config_for_generation["best_models_number"])

    print(len(population), " models are selected")
    print("best yet generated model", population[0].MSE)
    print(population[0].handle)
    if hasattr(population[0], "optimal_params"):
        print(population[0].optimal_params)
    else:
        print("no params")

    print("")

    if population[0].MSE <= int(config_for_accuracy["required_accuracy"]):
        break


pr.disable()
# after your program ends
#pr.print_stats(sort="calls")