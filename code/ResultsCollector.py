import datetime

def collect(population, config, measurements, regime):
    """

    :param population: resulted population (set of best generated models)
    :param config:     config-file
    :param measurements:    array of MSE of the best model on each iteration

    Author: Andrei Kulunchakov
    """
    results_dir = config["data_extraction"]["results_dir"]
    data = datetime.datetime.now().strftime("%B %d, %Y")
    print(results_dir + data)
    check_dir_existence(results_dir + data)

    with open(results_dir + data + "/" +regime, 'a+') as file:
        file.write("\n")
        file.write(repr(population))
        file.write("\n")
        file.write(repr(measurements))



def check_dir_existence(data):
    import os
    if not os.path.exists(data):
        print("create dir")
        os.makedirs(data)