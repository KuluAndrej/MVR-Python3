"""
Extract arbitrary segment in the specified time series and store it to the file
specified in 'config'

Author: Kulunchakov Andrei, MIPT
"""

import code.DataLoader as DataLoader
import code.MVRAttributesExtraction as MVRAttributesExtraction
import code.DataPreprocesser as DataPreprocesser
import code.SegmentatorTS as SegmentatorTS
import code.SaveData as SaveData

def data_cutter_loader(label, number_of_segment):
    """
    Extract arbitrary segment in the specified time series and store it to the file
    specified in 'config'

    Inputs:
     label              - label of the time series, which we'll cut from
     number_of_segment  - index of retrieved segment

    Outputs:
     init_models    - handles of the initial models from the specified file (list of strings)
    Author: Kulunchakov Andrei, MIPT
    """
    # get a data structure with the MVR attributes
    config          = MVRAttributesExtraction.attributes_extraction()
    type_of_fitting = config["flag_type_of_processing"]["flag"]


    labels_ts_to_retrieve = [label]

    for ind_label, label in enumerate(labels_ts_to_retrieve):
        print('now process the label ', label)
        whole_ts_to_fit = DataLoader.retrieve_ts(config,label)
        list_ts_to_fit  = SegmentatorTS.segmentate_ts(whole_ts_to_fit, int(config["time_series_processing"]["number_of_segments"]))


        data = DataPreprocesser.data_preprocesser(list_ts_to_fit[number_of_segment])
        print(data.shape)
        filename = '/data/data_to_fit.txt'

        SaveData.save_data(data, filename)
