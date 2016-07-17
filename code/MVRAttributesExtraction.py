import configparser
import code.ValidateConfig as ValidateConfig

def extract_config(root =''):
    """
    Extract MVR options specified in config.ini
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    Author: Kulunchakov Andrei
    """

    # retrieve attributes of MVR necessary for a future work
    ATTRIBUTES_FILENAME = "config.ini"
    config = configparser.ConfigParser()

    config.read(root + ATTRIBUTES_FILENAME)

    return config

