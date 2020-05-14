from flask import *
from data_pipeline.daten_filtern.src.filtern_engine import filtern_engine
import data_pipeline.exception.exceptions as exe

app = Flask(__name__)

@app.route('/filtern', methods =['POST'])
def filter():
    '''
    Name in documentation: "filtern()"
    Validates the supplied config and then starts the filter engine. The received config is transferred to this
    :return: statuscode
    '''

    response = None
    try:
        config_validation('filtern_config')
        filtern_config = request.get_json()['filtern_config']
        timeframe = filtern_config['timeframe']
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        #filtern_engine.filter(config, timeframe)
        response = 200

    except exe.ConfigException as exConf:
        #logger.influx_logger.error("Config is wrong.")
        response = exConf.args[1]
    except exe.DBException as exDb:
        #logger.influx_logger.error("Database not available.")
        response = exDb.args[1]
    finally:
        return Response(status=response)

@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    Reads the resulting logs.
    '''
    return 'logs'


def config_validation(config_str):
    """
    Validate the config. It is checked whether the values for "delete" are only "True" and "False"
    and whether the values for "Interpolation" are only "linear", "cubic", "spline" and "akima".
    Also checks if every curve and cycle is in the config.
    If this is not the case, an ConfigException is thrown.
    :param config_str: the Rootelement of the Config:
    """

    if int(request.headers.get('Content-Length')) == 0:
        #logger.influx_logger.error('Config-JSON empty')
        raise exe.ConfigException("Filtern Config is empty.", 900)

    try:
        filtern_config = request.get_json()[config_str]
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        timeframe = filtern_config['timeframe']
    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Filtern Config is wrong.", 900)


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
                raise exe.ConfigException("Filtern Config is wrong.", 900)

            if cycle in expected_cycle:
                expected_cycle.remove(cycle)
            if config[curve][cycle]["delete"] != 'True' and config[curve][cycle]["delete"] != 'False':
                raise exe.ConfigException("Filtern Config is wrong.", 900)
            if config[curve][cycle]["Interpolation"] != 'linear' and config[curve][cycle]["Interpolation"] != 'cubic' and config[curve][cycle]["Interpolation"] != 'spline' and config[curve][cycle]["Interpolation"] != 'akima':
                raise exe.ConfigException("Filtern Config is wrong.", 900)

        if expected_cycle != []:
            raise exe.ConfigException("Filtern Config is wrong.", 900)

    if expected_curve != []:
        raise exe.ConfigException("Filtern Config is wrong.", 900)

    #["2020-01-10 00:00:00.000 UTC", "2020-01-20 12:0:00.000 UTC"],
    for time in timeframe:
        print(time)
        for char in time:
            print(char)




if __name__ == '__main__':
    app.run(host='localhost', port='8000')