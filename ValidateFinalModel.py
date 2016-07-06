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

        files_path = 'populations/collected_models18/'

        lines_file_content = open(files_path + filename, 'r').readlines()
        population = empty(len(lines_file_content), dtype = object)

        for ind, entity in enumerate(lines_file_content):
            population[ind] = entity.split(' ')[-1].strip()
        return [model for model in population]


    config          = MVRAttributesExtraction.attributes_extraction()
    whole_ts_to_fit = DataLoader.retrieve_ts(config, label)
    list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))
    data_to_fit     = DataPreprocesser.data_preprocesser(list_ts_to_fit[index_to_observe - 1])

    dict_tokens_info = ReadTokensInfoForOptimization.read_info_tokens_for_optimization(config)

    models_names         = get_population_from_file(label + '_' + str(index_to_observe) + '.txt')
    initial_models       = strings_to_population(models_names)
    print("model = ", initial_models[0])
    model = Parametrizer.parametrizing(initial_models[0].handle).first
    model = re.sub(r'w(\d+)',r'w[\1]', model)
    model = re.sub(r'X\[(\d+)\]',r'x', model)
    print("model = ", model, sep='')

    untrained_population = Population(initial_models[0:1])

    ConstructScipyOptimizeAttributes.construct_info_population(untrained_population,dict_tokens_info)

    population  = Parametrizer.parametrize_population(untrained_population)

    population = Evaluator.evaluator(population, data_to_fit, dict_tokens_info, config)
    population = QualityEstimator.quality_estimator(population, data_to_fit, config)

    print("w = np.", repr(insert(initial_models[0].optimal_params, [0,], [0,])),sep='')


    ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)

import sys

labels = ['open_apple', 'heart_rate']
number_of_segments = 50

for index_segment in range(number_of_segments):
    for ind_label, label in enumerate(labels):
        print(label, index_segment)
        plt.figure(index_segment + ind_label * number_of_segments)
        validate_final_model(label, index_segment + 1)

