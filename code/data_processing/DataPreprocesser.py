import numpy as np

def data_preprocesser(data_to_process):
    """
    We scale given data, delete outfilers.
    Inputs:
     data_to_process

    Outputs:
     data_processed

    Author: Kulunchakov Andrei, MIPT
    """
    #data_to_process = preprocessing.scale(data_to_process,axis = 1)


    data_to_process = data_to_process - np.mean(data_to_process, axis = 0)
    data_to_process = np.divide(data_to_process, np.max(np.abs(data_to_process), axis=0))

    return data_to_process