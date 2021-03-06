"""
Main file of the MVR project.

Author: Kulunchakov Andrei, MIPT
"""
import code.input_output.MVRAttributesExtraction as MVRAttributesExtraction
import code.input_output.DataLoader as DataLoader
import code.DataFitting as DataFitting
import code.data_processing.DataPreprocesser as DataPreprocesser
import code.data_processing.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.input_output.SavePopulationToFile as SavePopulationToFile
import code.input_output.CutSegmentStoreToFile as CutSegmentStoreToFile
import code.input_output.CreateBigRandomInitPopulation as CreateBigRandomInitPopulation
import time
import matplotlib.pyplot as plt

import code.ResultsCollector as ResultsCollector
from code.primitives.Primitives import *
import code.genetic_operations.GenerateAllPossibleModels as GenerateAllPossibleModels

# get a data structure with the MVR attributes
config          = MVRAttributesExtraction.extract_config()
type_of_fitting = config["flag_type_of_processing"]["flag"]
print(type_of_fitting)


if type_of_fitting == "labeled_fit_data":
    label = 'heart_rate'
    index_to_observe = 27

    CutSegmentStoreToFile.data_cutter_loader(label, index_to_observe, config)
    data_to_fit = DataLoader.retrieve_data(config)

    data_to_fit = DataLoader.retrieve_data(config)
    start = time.time()
    population, measurements = DataFitting.data_fitting(data_to_fit, config, verbose = True)
    print(time.time() - start, population[0].MSE)
    plt.plot(measurements)
    plt.show()
    ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)
    print(repr(population[0].optimal_params))
    print()

if type_of_fitting == "fit_data":
    plot_verbose = False
    if plot_verbose:
        plt.axis([-1,1,-1,1])
        plt.ion()
        plt.show()
    data_to_fit = []
    activities = eval(config["activity_prediction"]["activities"])

    for activity in activities:
        data_to_fit_whole = DataLoader.retrieve_activity_data(config, "0", activity)
        for ind_file, data_to_fit_4_columns in enumerate(data_to_fit_whole):
            data_to_fit_pred_X = data_to_fit_4_columns[:,[1,0]]
            data_to_fit_pred_Y = data_to_fit_4_columns[:,[2,0]]
            data_to_fit_pred_Z = data_to_fit_4_columns[:,[3,0]]
            data_to_fit = data_to_fit_pred_X[:len(data_to_fit_pred_X)//2,:]
            break


    #CreateBigRandomInitPopulation.create_big_random_init_population(config)

    print(data_to_fit.shape)
    start = time.time()

    population, measurements = DataFitting.data_fitting(data_to_fit, config,
                                                        use_simplification = False, plot_verbose = False)

    print("time elapsed =", time.time() - start, ",\npopulation MSE =", population[0].MSE)
    if not plot_verbose:
        plt.plot(measurements)
        plt.show()
        ObserverTheBestFunction.draw_2d_plot(population, data_to_fit)
    print(repr(population[0].optimal_params))

elif type_of_fitting == "time_series_processing":
    labels_ts_to_retrieve = config["time_series_processing"]["labels"].split(', ')
    start_label_ind = 1
    start_index     = 62
    number_of_segments = int(config["time_series_processing"]["number_of_segments"])
#   for ind_segment in enumerate(list_ts_to_fit):, ts_to_fit)

    for ind_segment in range(number_of_segments):
        if ind_segment < start_index:
            continue
        for ind_label, label in enumerate(labels_ts_to_retrieve):
            if ind_segment == start_index and ind_label < start_label_ind:
                continue

            print('now process the label ', label, '#', ind_segment)

            whole_ts_to_fit = DataLoader.retrieve_ts(config, label)
            list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))

            ts_to_fit           = DataPreprocesser.data_preprocesser(list_ts_to_fit[ind_segment])
            best_fitting_models = DataFitting.data_fitting(ts_to_fit, config)
            #ObserverTheBestFunction.observer_the_best_function(best_fitting_models, ts_to_fit)
            SavePopulationToFile.save_population_to_file(best_fitting_models, config, label, ind_segment + 1)



elif type_of_fitting == "fit_and_collect":
    start_label_ind = 0
    start_index     = 0
    labels = ['heart_rate']
    for ind,label in enumerate(labels):
        if ind < start_label_ind:
            continue
        CutSegmentStoreToFile.data_cutter_loader(label)
        data_to_fit = DataLoader.retrieve_data(config)

        for iteration in range(int(config['fit_and_collect']['number_fittings'])):
            if ind == start_label_ind and iteration < start_index:
                continue
            print('... iteration number', iteration)
            population  = DataFitting.data_fitting(data_to_fit, config)
            ObserverTheBestFunction.observer_the_best_function(population, data_to_fit, config)
            SavePopulationToFile.save_population_to_file(population, config, label, iteration + 1)

elif type_of_fitting == "init_models_creation":
    config = MVRAttributesExtraction.extract_config()
    CreateBigRandomInitPopulation.create_big_random_init_population(config)
    #GenerateAllPossibleModels.generate('data/Rules_creation_files/init_patterns.txt',number_of_variables = 2)

elif type_of_fitting == "activity_prediction":
    activities = eval(config["activity_prediction"]["activities"])

    for activity in activities:
        data_to_fit_whole = DataLoader.retrieve_activity_data(config, "0", activity)
        for ind_file, data_to_fit_4_columns in enumerate(data_to_fit_whole):
            if activity == "jogging" and ind_file < 85:
                continue
            print("Process %s and file %d" % (activity, ind_file))
            data_to_fit_pred_X = data_to_fit_4_columns[:,[1,0]]
            data_to_fit_pred_Y = data_to_fit_4_columns[:,[2,0]]
            data_to_fit_pred_Z = data_to_fit_4_columns[:,[3,0]]

            best_fitting_models_X = DataFitting.data_fitting(data_to_fit_pred_X, config, plot_verbose=False)
            best_fitting_models_Y = DataFitting.data_fitting(data_to_fit_pred_Y, config, plot_verbose=False)
            best_fitting_models_Z = DataFitting.data_fitting(data_to_fit_pred_Z, config, plot_verbose=False)

            SavePopulationToFile.save_activity_population_to_file(best_fitting_models_X, best_fitting_models_Y,
                best_fitting_models_Z,config, user_name = 0, activity = activity, number_of_file=ind_file)
