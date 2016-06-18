"""
Main file of the MVR project.

Author: Kulunchakov Andrei, MIPT
"""

import code.DataLoader as DataLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataFitting as DataFitting
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.ObserverTheBestFunction as ObserverTheBestFunction
import code.SaveData as SaveData
import code.SavePopulationToFile as SavePopulationToFile
import CutSegmentStoreToFile
import time
import matplotlib.pyplot as plt

# get a data structure with the MVR attributes
config          = MVRAttributesExtraction.attributes_extraction()
type_of_fitting = config["flag_type_of_processing"]["flag"]
print(type_of_fitting)

if type_of_fitting == "fit_data":

    data_to_fit = DataLoader.retrieve_data(config)
    start = time.time()
    population, measurements = DataFitting.data_fitting(data_to_fit, config)
    print(time.time() - start, population[0].MSE)
    plt.plot(measurements)
    plt.show()
    ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)

elif type_of_fitting == "time_series_processing":
    labels_ts_to_retrieve = config["time_series_processing"]["labels"].split(', ')

    for ind_label, label in enumerate(labels_ts_to_retrieve):
        print('now process the label ', label)
        whole_ts_to_fit = DataLoader.retrieve_ts(config,label)
        list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))
        print(len(list_ts_to_fit))

        for (ind, ts_to_fit) in enumerate(list_ts_to_fit):
            print('...part of the ', label, ' ts number ', str(ind))
            ts_to_fit           = DataPreprocesser.data_preprocesser(ts_to_fit)
            best_fitting_models = DataFitting.data_fitting(ts_to_fit, config)

            SavePopulationToFile.save_population_to_file(best_fitting_models, config, label, ind + 1)
elif type_of_fitting == "fit_and_collect":

    labels = ['chest_volume', 'heart_rate', 'oxygen_concentration']
    for label in labels:
        CutSegmentStoreToFile.data_cutter_loader(label)
        data_to_fit = DataLoader.retrieve_data(config)

        for iteration in range(int(config['fit_and_collect']['number_fittings'])):
            print('... iteration number', iteration)
            population  = DataFitting.data_fitting(data_to_fit, config)

            SavePopulationToFile.save_population_to_file(population, config, label, iteration + 51)




# after your program ends
#pr.print_stats(sort="calls")