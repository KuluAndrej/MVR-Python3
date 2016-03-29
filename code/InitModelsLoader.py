import pandas as pd
import numpy as np
import os

def retrieve_data(config):
    """
    Read data to fit from the folder specified in 'config'
    Inputs:
     config  - data structure storing MVR attributes

     Outputs:


    initial_models   - list of handles of initial functions
    """
    DATA_LOCAL_PATH = config["data_extraction"]["dataset_filename"]
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    # retrieve the data to fit from the specified file
    data_to_fit = np.loadtxt(DATA_FULL_PATH)
    return data_to_fit
    
    primitive_info = pd.read_excel(data_dir + "demo.reg.xlsx")
    initial_models = []

    for line in open(data_dir + "demo.mdl.txt"):
        line = line.strip()
        if not (line.startswith("#") or len(line) == 0):
            initial_models.append(line)
    return (primitive_info, initial_models)