import data_pipeline.exception.exceptions as exe
import re


def config_validation(filtern_config):
    """
    Name in documentation: 'config_validation'
    Validate the config. It is checked whether the values for "delete" are only "True" and "False"
    and whether the values for "Interpolation" are only "linear", "cubic", "spline" and "akima".
    Also checks if every curve and cycle is in the config.
    If this is not the case, an ConfigException is thrown.
    :raises: ConfigExeption: For incorrect Config.
    :raises: InvalidConfigKeyException: For wrong keys in Config.
    :raises: InvalidConfigValueException: For wrong Values in Config.
    :raises: IncompleteConfigException: For missing anything in Config.
    :param filtern_config: The filtern_config:
    """


    try:
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        timeframe = filtern_config['timeframe']
    except:
        raise exe.InvalidConfigKeyException("Can not read Filtern Config.", 900)


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
                raise exe.InvalidConfigKeyException("Filtern Config got no Interpolation or Delete.", 900)

            if cycle in expected_cycle:
                expected_cycle.remove(cycle)
            if config[curve][cycle]["delete"] != 'True' and config[curve][cycle]["delete"] != 'False':
                raise exe.InvalidConfigValueException("Filtern Config Delete is not True or False.", 900)
            if config[curve][cycle]["Interpolation"] != 'linear' and config[curve][cycle]["Interpolation"] != 'cubic' and config[curve][cycle]["Interpolation"] != 'spline' and config[curve][cycle]["Interpolation"] != 'akima':
                raise exe.InvalidConfigValueException("Filtern Config Interpolation is not linear, cubic, spline or akima.", 900)

        if expected_cycle != []:
            raise exe.IncompleteConfigException("Filtern Config missing a cycle.", 900)

    if expected_curve != []:
        raise exe.IncompleteConfigException("Filtern Config missing a curve.", 900)

    for time in timeframe:
        if not re.search(r"[0-9][0-9][0-9][0-9][-][0-1][0-9][-][0-3][0-9][ ][0-2][0-9][:][0-6][0-9][:][0-6][0-9][.][0-9][0-9][0-9][ ][U][T][C]" , time):
            raise exe.ConfigException("Filtern Config Timeframe Format is not correct.", 900)


