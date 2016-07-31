
def save_population_to_file(population, config, label, number_of_file, filename = ''):
    """
    Return data to fit from the folder specified in 'config'
    Inputs:
     population
     config         - some settings specifying folders and extensions
     label          - name/label of the file to which the population is being stored to
     number_of_file - serial number of the file to which the population is being stored to
     filename       - if set, we ignore 'config' and store models in to 'filename'

    Outputs:
     -

    Author: Kulunchakov Andrei, MIPT
    """

    filename = construct_filename(config, filename)

    # save the population to the specified file
    file_to_store_ts  = open(filename, "w+")
    if isinstance(population, list):
        file_to_store_ts .write('\n'.join(population))
    else:
        file_to_store_ts .write("%s\n" % population)



def construct_filename(config, fname):
    if config:
        type_of_fitting = config["flag_type_of_processing"]["flag"]

        # construct the filename where we store the models
        if type_of_fitting == "time_series_processing":
            filename = config["time_series_processing"]["where_to_store_models"]+label+"_"+str(number_of_file)+config["time_series_processing"]["extension"]
        elif type_of_fitting == "fit_and_collect":
            filename = config["fit_and_collect"]["where_to_store_models"]+label+"_"+str(number_of_file)+config["time_series_processing"]["extension"]
    else:
        filename = fname

    return filename

