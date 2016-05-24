def config_validation(config):
    config_flag_type_of_processing = config["flag_type_of_processing"]
    config_time_series_processing = config["time_series_processing"]

    if not config_flag_type_of_processing["flag"] in ['fit_data', 'time_series_processing']:
        raise NameError("flag is not in the ['fit_data', 'time_series_processing']")
