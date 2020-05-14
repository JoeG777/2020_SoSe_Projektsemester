import data_pipeline.exception.exceptions as exe


def config_validation(filtern_config):
    """
    Validate the config. It is checked whether the values for "delete" are only "True" and "False"
    and whether the values for "Interpolation" are only "linear", "cubic", "spline" and "akima".
    Also checks if every curve and cycle is in the config.
    If this is not the case, an ConfigException is thrown.
    :param config_str: the Rootelement of the Config:
    """

    try:
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        timeframe = filtern_config['timeframe']
    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Can not read Filtern Config.", 900)


    expected_curve = ['room', 'condenser', 'evaporator', 'inlet', 'outlet', 'freshAirIntake']
    for curve in config:
        if curve in expected_curve:
            expected_curve.remove(curve)

        expected_cycle = ['warmwasseraufbereitung', 'ofennutzung','abtauzyklus', 'luefterstufen']
        for cycle in config[curve]:
            expected_delete_interpolation = ['delete' , 'Interpolation']

            for delete_interpolation in config[curve][cycle]:
                if delete_interpolation in expected_delete_interpolation:
                    expected_delete_interpolation.remove(delete_interpolation)

            if expected_delete_interpolation != []:
                raise exe.ConfigException("Filtern Config got no Interpolation or Delete.", 900)

            if cycle in expected_cycle:
                expected_cycle.remove(cycle)
            if config[curve][cycle]["delete"] != 'True' and config[curve][cycle]["delete"] != 'False':
                raise exe.ConfigException("Filtern Config Delete is not True or False.", 900)
            if config[curve][cycle]["Interpolation"] != 'linear' and config[curve][cycle]["Interpolation"] != 'cubic' and config[curve][cycle]["Interpolation"] != 'spline' and config[curve][cycle]["Interpolation"] != 'akima':
                raise exe.ConfigException("Filtern Config Interpolation is not linear, cubic, spline or akima.", 900)

        if expected_cycle != []:
            raise exe.ConfigException("Filtern Config missing a cycle.", 900)

    if expected_curve != []:
        raise exe.ConfigException("Filtern Config missing a curve.", 900)

