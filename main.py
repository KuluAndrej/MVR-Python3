"""
Main file of the MVR project.

Author: Kulunchakov Andrei, MIPT
"""

import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataLoader as DataLoader
import code.DataFitting as DataFitting
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.SavePopulationToFile as SavePopulationToFile
import CutSegmentStoreToFile
import time
import matplotlib.pyplot as plt

# get a data structure with the MVR attributes
config          = MVRAttributesExtraction.attributes_extraction()
type_of_fitting = config["flag_type_of_processing"]["flag"]
print(type_of_fitting)

if type_of_fitting == "fit_data":
    label = 'heart_rate'
    index_to_observe = 1

    CutSegmentStoreToFile.data_cutter_loader(label, index_to_observe)
    data_to_fit = DataLoader.retrieve_data(config)

    start = time.time()
    population, measurements = DataFitting.data_fitting(data_to_fit, config)
    print(time.time() - start, population[0].MSE)
    plt.plot(measurements)
    plt.show()
    ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)
    print(population[0].optimal_params)

elif type_of_fitting == "time_series_processing":
    labels_ts_to_retrieve = config["time_series_processing"]["labels"].split(', ')
    start_label_ind = 0
    start_index     = 0
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
            ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)
            SavePopulationToFile.save_population_to_file(population, config, label, iteration + 1)
# after your program ends
# pr.print_stats(sort="calls")
