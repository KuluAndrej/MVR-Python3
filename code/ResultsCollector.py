import datetime, inspect

def collect(results, config, measurements, regime):
    """

    :param results:   information to store
    :param config:    config-file
    :param measurements:    array of MSE of the best model on each iteration
    :param regime:    type of results collected

    Author: Andrei Kulunchakov
    """
    results_dir = config["data_extraction"]["results_dir"]
    data = datetime.datetime.now().strftime("%B %d, %Y")
    filename = results_dir + data + "/" +regime + str(2)
    check_dir_existence(results_dir + data)
    if type(results) == type(0):
        file = open(filename, 'a+')
        file.write("\nLaunch =" + str(results))
        file.write("\n")
        file.close()
        return


    if len(inspect.stack()) > 1 and len(inspect.stack()[1]) > 3 and inspect.stack()[1][3] == "rule_simplify":
        file = open(filename, 'a+')
        file.write("\nRule applied: ")
        file.write(repr(results[0]))
        file.write(" --> ")
        file.write(repr(results[1]))
        file.close()
        return


    file = open(filename, 'a+')
    file.write("\n")
    file.write(repr(results))
    file.write("\n")
    file.write(repr(measurements))
    file.close()


def check_dir_existence(data):
    import os
    if not os.path.exists(data):
        os.makedirs(data)