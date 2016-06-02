import numpy as np
import os

def save_data(data, filename):
    """
    Return data to fit from the folder specified in 'config'
    Inputs:
     data           - data to be stored
     filename       - name of the file to store 'data'

    Outputs:
     -

    Author: Kulunchakov Andrei, MIPT
    """
    DATA_LOCAL_PATH = filename
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    DATA_FULL_PATH = parent_dir + DATA_LOCAL_PATH

    # save the data to fit from the specified file
    np.savetxt(DATA_FULL_PATH, data, fmt='%.4f', delimiter=',', newline='\n')
