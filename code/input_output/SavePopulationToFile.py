import os

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

    filename = construct_filename(config, filename, label, number_of_file)

    # save the population to the specified file
    file_to_store_ts  = open(filename, "w+")
    if isinstance(population, list):
        file_to_store_ts.write('\n'.join(population))
    else:
        file_to_store_ts.write("%s\n" % population)


def save_activity_population_to_file(populationX, populationY, populationZ,
                                     config, user_name, activity, number_of_file, filename = ''):
    """
    Save generated populations of models approximating on all 3 dimensions of data
    Inputs:
     populationX, populationY, populationZ
     config         - some settings specifying folders and extensions
     user_name      - id of person providing data
     activity       - type of activity, which person performs
     number_of_file - serial number of the file to which the population is being stored to

    Outputs:
     -

    Author: Kulunchakov Andrei, MIPT
    """

    filename = construct_filename(config, filename, None, number_of_file, user_name, activity)

    # save the population to the specified file
    file_to_store_ts  = open(filename, "w+")
    if isinstance(populationX, list):
        file_to_store_ts.write('\n'.join(populationX))
        file_to_store_ts.write('\n'.join(populationY))
        file_to_store_ts.write('\n'.join(populationZ))
    else:
        file_to_store_ts.write("%s\n" % populationX)
        file_to_store_ts.write("%s\n" % populationY)
        file_to_store_ts.write("%s\n" % populationZ)


def construct_filename(config, fname, label, number_of_file, user_name = None, activity = None):
    if config:
        type_of_fitting = config["flag_type_of_processing"]["flag"]

        # construct the filename where we store the models
        if type_of_fitting == "time_series_processing":
            filename = config["time_series_processing"]["where_to_store_models"]+label+"_"+str(number_of_file)+config["time_series_processing"]["extension"]
        elif type_of_fitting == "fit_and_collect":
            filename = config["fit_and_collect"]["where_to_store_models"]+label+"_"+str(number_of_file)+config["time_series_processing"]["extension"]
        elif type_of_fitting == "activity_prediction":
            if not os.path.exists(config["activity_prediction"]["directory_store"]+str(user_name)):
                os.makedirs(config["activity_prediction"]["directory_store"]+str(user_name))
            filename = config["activity_prediction"]["directory_store"]+str(user_name)+"/"+activity+'_'+\
                       str(number_of_file) + '.txt'
    else:
        filename = fname

    return filename

