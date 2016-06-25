"""
Retrieve final population for specified segment of time series
Draw on the same plot initial and predicted values for the top model in the population

Author: Kulunchakov Andrei, MIPT
"""


import code.DataLoader as DataLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.QualityEstimator as QualityEstimator
import code.Evaluator as Evaluator
import code.Parametrizer as Parametrizer
from code.StringToModel import strings_to_population
import time
import matplotlib.pyplot as plt
import code.CalculatorModelValues as CalculatorModelValues
from numpy import  sum, isnan, inf,  nan, transpose, errstate
import os, re
import matplotlib.pyplot as plt
from numpy import empty
from code.structures.Population import Population

def get_population_from_file(filename):

    files_path = 'populations/collected_models6/'
    print(files_path + filename)
    lines_file_content = open(files_path + filename, 'r').readlines()
    population = empty(len(lines_file_content), dtype = object)

    for ind, entity in enumerate(lines_file_content):
        population[ind] = entity.split(' ')[-1].strip()
    return [model for model in population]

label = 'chest_volume'
index_to_observe = 2
config          = MVRAttributesExtraction.attributes_extraction()
whole_ts_to_fit = DataLoader.retrieve_ts(config, label)
list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))
data_to_fit     = DataPreprocesser.data_preprocesser(list_ts_to_fit[index_to_observe - 1])

independent_var = data_to_fit[:,1:]
independent_var = transpose(independent_var)
dependent_var   = data_to_fit[:,0]

models_names         = get_population_from_file(label + '_' + str(index_to_observe) + '.txt')
initial_models       = strings_to_population(models_names)
untrained_population = Population(initial_models[0:1])

population  = Parametrizer.parametrize_population(untrained_population)
population = Evaluator.evaluator(population, data_to_fit, config)
population = QualityEstimator.quality_estimator(population, data_to_fit)

print(population)

if hasattr(population[0], 'optimal_params'):
    print(population[0].optimal_params)

ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)
