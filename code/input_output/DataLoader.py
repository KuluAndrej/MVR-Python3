import numpy as np
import os

def retrieve_data(config):
    """
    Return data to fit from the folder specified in 'config'
    Inputs:
     config         - data structure storing MVR attributes

     Outputs:
     data_to_fit    - data from the specified file


    initial_models   - list of handles of initial functions

    Author: Kulunchakov Andrei, MIPT
    """
    DATA_LOCAL_PATH = config["data_extraction"]["dataset_filename"]
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    # retrieve the data to fit from the specified file
    data_to_fit = np.loadtxt(DATA_FULL_PATH, delimiter = ',')


    print('data = ', data_to_fit.shape)
    return data_to_fit

def retrieve_ts(config,label):
    """
    Return time series data to fit from the folder specified in 'config'
    Inputs:
     config         - data structure storing MVR attributes
     label          - label of time series to retrieve

    Outputs:
     data_to_fit    - data from the specified file


    initial_models   - list of handles of initial functions
    """
    DATA_LOCAL_PATH = config["time_series_processing"]["root_path"]
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    parent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))

    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH + label + config["time_series_processing"]["extension"]
    # retrieve the data to fit from the specified file
    data_to_fit = np.loadtxt(DATA_FULL_PATH, delimiter = ',')
    data_to_fit = np.vstack((data_to_fit, np.linspace(-1,1, len(data_to_fit)))).T

    return data_to_fit

