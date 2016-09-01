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
#measurements = np.zeros(grid_of_multistart_parameter.shape)
measurements = np.zeros(50)

def draw_plot(pattern, replacement):
    config           = MVRAttributesExtraction.extract_config()
    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    population = Population([Model(pattern), Model(replacement)])
    population = Parametrizer.parametrize_population(population)

    DefConstructor.add_def_statements_attributes(population)

    #for ind, param in enumerate(grid_of_multistart_parameter):
    for ind in range(measurements.size):
        #print(param)

        param = 5

        tuned_config = ConfigParser()
        tuned_config.read_dict(config)
        tuned_config["model_generation"]["iterations_multistart"] = str(param)
        tuned_config["rules_creation"]["iterations_to_check_fitness"] = str(250)


        b, checks = CheckReplacementForFitting.check(population[0], population[1], dict_tokens_info, tuned_config, False, False)
        measurements[ind] = np.mean(checks)

    #print(measurements)
    #plt.plot(grid_of_multistart_parameter, measurements)
    #plt.show()
    #plt.hist(measurements)
    #plt.show()
    return measurements

pattern = 'lnl_(neg_(X[0]))'
replacement = 'lnl_(X[0])'
draw_plot(pattern,replacement)
"""
data_file = open("data/Rules_creation_files/received_rules.txt",'r').readlines()
out_file = open("data/Rules_creation_files/proc_rules.txt",'w')

for line in data_file:
    models = line.split()
    print("process rule", models)
    start = time.time()

    output = draw_plot(models[0], models[1])
    out_file.write(repr(models))
    out_file.write('\n')
    percentiles = []
    for i in np.arange(10,95,20):
        out_file.write("%.3f" % np.percentile(output, i))
        out_file.write(' ')
    out_file.write('\n')
    print(time.time() - start)

out_file.close()
data_file.close()
"""