import openpyxl
import pandas as pd
import os

def retrieve_data(DATAPATH = "/data/"):
    """
    Read information about primitive functions and initial models
    Inputs:
     DATAPATH - path to the folder with data

     Outputs:
     primitive_info  - dataframe containing info about primitive functions:
         name        - string representation of a function
         outputs     - number of outputs
         arguments   - number of arguments
         parameteres - number of parameters

    initial_models   - list of handles of initial functions
    """

    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    data_dir = parent_dir + DATAPATH

    primitive_info = pd.read_excel(data_dir + "demo.reg.xlsx")
    initial_models = []

    for line in open(data_dir + "demo.mdl.txt"):
        line = line.strip()
        if not (line.startswith("#") or len(line) == 0):
            initial_models.append(line)
    return (primitive_info, initial_models)