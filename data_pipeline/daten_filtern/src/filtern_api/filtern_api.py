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
        #filtern_config = request.get_json()["filtern_config"]
        config_validation('filtern_config')
        #config = filtern_config["filter_options"][filtern_config["selected_value"]]
        #print(config)
    #        config_validation(config)
        filtern_config = request.get_json()['filtern_config']
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        print(config)
        filtern_engine.filter(config)
        response = 200

    except exe.IncompleteConfigException:
        print("???????????")
        #logger.influx_logger.error("Config is wrong.")
        #raise ConfigException("Filtern Config is wrong.", 900)
        print(response)
        response = exe.IncompleteConfigException.args[1]
        print(response)
    finally:
        return Response(status=response)



@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    '''
    return 'logs'

def config_validation(config):
    """

    :param config:
    :return:
    """

    if int(request.headers.get('Content-Length')) == 0:
        #logger.influx_logger.error('Config-JSON empty')
        print("!!!!!!!!!!!")
        raise exe.IncompleteConfigException("Filtern Config is empty.", 900)



    try:
        temp = request.get_json()[config]
        print(temp)
    except:
        #logger.influx_logger.error("Config is wrong.")
        raise exe.IncompleteConfigException("Filtern Config is wrong.", 900)


"""
    counter_curve = 0
    counter_cycle = 0
    for curve in config:
        counter_curve = counter_curve + 1
        for cycle in config[curve]:
            counter_cycle += 1

    if counter_cycle != 6 or counter_curve != 24:
        raise ConfigException("Filtern Config is wrong.", 900)
        """

if __name__ == '__main__':
    app.run(host='localhost', port='8000')