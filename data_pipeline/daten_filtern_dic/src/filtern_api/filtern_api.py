from flask import *
from data_pipeline.daten_filtern_dic.src.filtern_engine import filtern_engine
from data_pipeline.daten_filtern_dic.src.filtern_validator import filtern_validator
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
        filtern_config = request.get_json()['filtern_config']
        filtern_validator.config_validation(filtern_config)
        timeframe = filtern_config['timeframe']
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        filtern_engine.filter(config, timeframe)
        response = 200

    except exe.IncompleteConfigException as exIncConf:
        #logger.influx_logger.error("Config is wrong.")
        response = exIncConf.args[1]
    except exe.DBException as exDb:
        #logger.influx_logger.error("Database not available.")
        response = exDb.args[1]
    except exe.InvalidConfigValueException as exInval:
        #logger.influx_logger.error("Config is wrong.")
        response = exInval.args[1]
    except exe.InvalidConfigKeyException as exInvalkey:
        #logger.influx_logger.error("Config is wrong.")
        response = exInvalkey.args[1]
    except exe.ConfigException as exConf:
        #logger.influx_logger.error("Config is wrong.")
        response = exConf.args[1]
    finally:
        return Response(status=response)

@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    Reads the resulting logs.
    '''
    return 'logs'

if __name__ == '__main__':
    app.run(host='localhost', port='8000')