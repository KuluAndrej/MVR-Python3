"""
Retrieve final population for specified segment of time series
Draw on the same plot initial and predicted values for the top model in the population

Author: Kulunchakov Andrei, MIPT
"""


import code.DataLoader as DataLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.QualityEstimator as QualityEstimator
import code.Evaluator as Evaluator
import code.Parametrizer as Parametrizer
import code.ReadTokensInfoForOptimization as ReadTokensInfoForOptimization
import code.ConstructScipyOptimizeAttributes as ConstructScipyOptimizeAttributes
from code.StringToModel import strings_to_population
from numpy import empty, insert
from code.structures.Population import Population
import matplotlib.pyplot as plt
import re


def validate_final_model(label, index_to_observe):
    def get_population_from_file(filename):

        files_path = 'populations/collected_models21/'


        lines_file_content = []
        last_non_empty_str = -1

        with open(files_path + filename, 'r') as f_in:
            lines_file_content = (line.rstrip() for line in f_in) # All lines including the blank ones
            non_empty_strings_inds = [ind for ind,line in enumerate(lines_file_content) if line]
            last_non_empty_str = non_empty_strings_inds[-1]

        lines_file_content = open(files_path + filename, 'r').readlines()[0:last_non_empty_str+1]
        population = empty(len(lines_file_content) // 2, dtype = object)

        """for ind, entity in enumerate(lines_file_content):
            model_name = entity.split(' ')[-1]
            population[ind] = re.sub(r'X\[(\d+)\]', r'x\1', model_name.strip())"""
        for ind, entity in enumerate(lines_file_content):
            if ind % 2 == 0:
                model_name = entity.split(' ')[-1]
                population[ind // 2] = model_name.strip()

        return population

    print("label =", label)
    config          = MVRAttributesExtraction.attributes_extraction()
    whole_ts_to_fit = DataLoader.retrieve_ts(config, label)
    list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))
    data_to_fit     = DataPreprocesser.data_preprocesser(list_ts_to_fit[index_to_observe - 1])

    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    models_names         = get_population_from_file(label + '_' + str(index_to_observe) + '.txt')
    initial_models       = strings_to_population(models_names)

    for i in range(len(initial_models) // 2):
        plt.figure()
        print(i, "model = ", initial_models[i])
        model = Parametrizer.parametrizing(initial_models[i].handle).first
        model = re.sub(r'w(\d+)',r'w[\1]', model)
        model = re.sub(r'X\[(\d+)\]',r'x', model)
        print("model = ", model, sep='')

        untrained_population = Population(initial_models[i:i+1])
        ConstructScipyOptimizeAttributes.construct_info_population(untrained_population,dict_tokens_info)

        population  = Parametrizer.parametrize_population(untrained_population)

        population = Evaluator.evaluator(population, data_to_fit, dict_tokens_info, config)
        population = QualityEstimator.quality_estimator(population, data_to_fit, config)

        print("w = np.", repr(insert(initial_models[i].optimal_params, [0,], [0,])),sep='')


        ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)

import sys
#validate_final_model(label, index_segment + 1)

if len(sys.argv) > 1 and sys.argv[1] == 'specific_segment':
    validate_final_model(sys.argv[2], int(sys.argv[3]))
else:

    labels = ['open_apple', 'heart_rate']
    number_of_segments = 50

    for index_segment in range(number_of_segments):
        for ind_label, label in enumerate(labels):
            print(label, index_segment)
            plt.figure(index_segment + ind_label * number_of_segments)
            validate_final_model(label, index_segment + 1)

