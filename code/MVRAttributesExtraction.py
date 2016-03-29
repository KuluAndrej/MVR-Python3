import configparser

def attributes_extraction():
    """
    Extract MVR options specified in config.ini
    Inputs:
     -

     Outputs:
     config  - data structure storing MVR attributes

    """

    # retrieve attributes of MVR necessary for a future work
    ATTRIBUTES_FILENAME = "config.ini"
    config = configparser.ConfigParser()
    config.read(ATTRIBUTES_FILENAME)
    return config

