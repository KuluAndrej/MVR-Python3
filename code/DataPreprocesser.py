from code.modules.crosser import crossing
import code.StringToModel as StringToModel
import numpy as np
from sklearn import preprocessing

def data_preprocesser(data_to_process):
    """
    We scale given data, delete outfilers.
    Inputs:
     data_to_process

    Outputs:
     data_processed
    """
    #data_to_process = preprocessing.scale(data_to_process,axis = 1)
    data_to_process = data_to_process - np.mean(data_to_process, axis = 0)
    data_to_process = np.divide(data_to_process, np.max(data_to_process, axis=0))

    return data_to_process