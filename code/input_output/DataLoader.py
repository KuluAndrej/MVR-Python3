import numpy as np
import os, re
import code.data_processing.DataPreprocesser as DataPreprocesser

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
    data_to_fit = DataPreprocesser.data_preprocesser(data_to_fit)

    print('data.shape = ', data_to_fit.shape)
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


def retrieve_activity_data(config,user,activity):
    DATA_LOCAL_DIR = config["activity_prediction"]["directory"] + user + '/'
    files = os.listdir(DATA_LOCAL_DIR)
    activity_files = list(filter(lambda x: x.startswith(activity), files))
    activity_files = sorted(activity_files, key=natural_keys)
    array_of_data = []

    for file in activity_files:
        A = np.loadtxt("ts_processing/human_activity/0/"+file, delimiter=',')
        for i in range(A.shape[1]):
            mn = min(A[:,i])
            mx = max(A[:,i])
            A[:,i] = (2 * A[:,i] - (mn + mx)) / (max(A[:,i]) - min(A[:,i]))
        array_of_data.append(A)

    return array_of_data

def atoi(text):
    return int(text) if text.isdigit() else text
def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

