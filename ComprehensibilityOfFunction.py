import code.model_processing.DefConstructor as DefConstructor
import code.rule_simplification.CheckReplacementForFitting as CheckReplacementForFitting
from code.structures.Population import Population
from code.structures.Model import Model
import code.model_processing.Parametrizer as Parametrizer
import code.input_output.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
from configparser import ConfigParser
import matplotlib.pyplot as plt
import numpy as np
import time

grid_of_multistart_parameter = np.arange(1,5)
measurements = np.zeros(grid_of_multistart_parameter.shape)


def measure_cimprehensibility(model):
    start = time.time()
    config           = MVRAttributesExtraction.extract_config()
    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    population = Population([Model(pattern), Model(replacement)])
    population = Parametrizer.parametrize_population(population)

    DefConstructor.add_def_statements_attributes(population)
    print('pattern =', population[0], "replacement =", population[1])

    for ind, param in enumerate(grid_of_multistart_parameter):
        print(param)
        tuned_config = ConfigParser()
        tuned_config.read_dict(config)
        tuned_config["model_generation"]["iterations_multistart"] = str(param)
        tuned_config["rules_creation"]["iterations_to_check_fitness"] = str(10000)


        b, checks = CheckReplacementForFitting.check(population[0], population[1], dict_tokens_info, tuned_config, False, False)
        print(checks.shape)
        measurements[ind] = np.mean(checks)

    print(measurements)
    #plt.plot(grid_of_multistart_parameter, measurements)
    #plt.show()
    print(time.time() - start)

measure_cimprehensibility('hypot_(normal_(X[0]),neg_(X[1]))')