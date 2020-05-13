from flask import *
from data_pipeline.daten_filtern.src.filtern_engine import filtern_engine
#from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config
import data_pipeline.exception.exceptions as exe

app = Flask(__name__)

@app.route('/filtern', methods =['POST'])
def filter():
    '''
    Name in documentation: 'filtern'
    Start the filtern engine.
    '''

    response = None

    try:
        config_validation('filtern_config')
        filtern_config = request.get_json()['filtern_config']
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        filtern_engine.filter(config)
        response = 200

    except exe.ConfigException as exConf:
        #logger.influx_logger.error("Config is wrong.")
        response = exConf.args[1]
    finally:
        return Response(status=response)



@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    '''
    return 'logs'


def config_validation(config_str):
    """

    :param config:
    :return:
    """

    if int(request.headers.get('Content-Length')) == 0:
        #logger.influx_logger.error('Config-JSON empty')
        raise exe.ConfigException("Filtern Config is empty.", 900)

    try:
        filtern_config = request.get_json()[config_str]
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.ConfigException("Filtern Config is wrong.", 900)



    counter_curve = 0
    counter_cycle = 0
    for curve in config:
        counter_curve += 1
        for cycle in config[curve]:
            counter_cycle += 1
            if config[curve][cycle]["delete"] != 'True' and config[curve][cycle]["delete"] != 'False':
                raise exe.ConfigException("Filtern Config is wrong.", 900)
            if config[curve][cycle]["Interpolation"] != 'linear' and config[curve][cycle]["Interpolation"] != 'cubic' and config[curve][cycle]["Interpolation"] != 'spline' and config[curve][cycle]["Interpolation"] != 'akima':
                raise exe.ConfigException("Filtern Config is wrong.", 900)


    if counter_curve != 6 or counter_cycle != 24:
        raise exe.ConfigException("Filtern Config is wrong.", 900)


if __name__ == '__main__':
    app.run(host='localhost', port='8000')