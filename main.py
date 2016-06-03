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

# get a data structure with the MVR attributes
config          = MVRAttributesExtraction.attributes_extraction()
type_of_fitting = config["flag_type_of_processing"]["flag"]

if type_of_fitting == "fit_data":

    data_to_fit = DataLoader.retrieve_data(config)
    population  = DataFitting.data_fitting(data_to_fit, config)

    print(population)

    #ObserverTheBestFunction.observer_the_best_function(population, data_to_fit)

elif type_of_fitting == "time_series_processing":
    # last one = 340
    starting_segment = 0
    starting_label_index = 42
    labels_ts_to_retrieve = config["time_series_processing"]["labels"].split(', ')

    for ind_label, label in enumerate(labels_ts_to_retrieve):
        print('now process the label ', label)
        whole_ts_to_fit = DataLoader.retrieve_ts(config,label)
        list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))
        print(len(list_ts_to_fit))

        for (ind, ts_to_fit) in enumerate(list_ts_to_fit):
            if ind_label < starting_label_index or ind < starting_segment:
                continue
            print('...part of the ', label, ' ts number ', str(ind))
            ts_to_fit = DataPreprocesser.data_preprocesser(ts_to_fit)

            best_fitting_models = DataFitting.data_fitting(ts_to_fit, config)
            file_to_store_ts    = open(config["time_series_processing"]["where_to_store_models"]+label+"_"+str(ind+1)+config["time_series_processing"]["extension"], "w+")
            file_to_store_ts .write("%s\n" % best_fitting_models)




# after your program ends
#pr.print_stats(sort="calls")