from flask import *
from data_pipeline.daten_filtern.src.filtern_engine import filtern_engine
from data_pipeline.daten_filtern.src.filtern_validator import filtern_validator
import data_pipeline.exception.exceptions as exe
import traceback

from data_pipeline.log_writer.log_writer import Logger
LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "localhost"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Daten filtern"

logger = Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT,
                LOGGER_COMPONENT)

app = Flask(__name__)

@app.route('/')
def default():
    """
    Not featured in the documentation.
    Just returns information about the API.
    """
    logger.info("Received request on default endpoint. Returning default answer.")
    return '<h1>Endpoints</h1><p>/filtern - Filter classified Data</p>' \
           '<p>/log - Get the logs</p>'

@app.route('/filtern', methods =['POST'])
def filter():
    '''
    Name in documentation: "filtern()"
    Validates the supplied config and then starts the filter engine. The received config is transferred to this
    :return: statuscode
    '''
    logger.info("Received request on filter data. Starting ...")
    response = None
    try:
        filtern_config = request.get_json()['filtern_config']
        filtern_validator.config_validation(filtern_config)
        logger.info("Config validated")
        timeframe = filtern_config['timeframe']
        config = filtern_config["filter_options"][filtern_config["selected_value"]]
        filtern_engine.filter(config, timeframe)
        response = 200
        logger.info("Filter data was successful. Returning" + str(response))

    except exe.IncompleteConfigException as e:
        exception_name = e.__class__.__name__
        stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
        response = e.args[1]
        logger.error("Returning " + str(response))
    except exe.DBException as e:
        exception_name = e.__class__.__name__
        stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
        response = e.args[1]
        logger.error("Returning " + str(response))
    except exe.InvalidConfigValueException as e:
        exception_name = e.__class__.__name__
        stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
        response = e.args[1]
        logger.error("Returning " + str(response))
    except exe.InvalidConfigKeyException as e:
        exception_name = e.__class__.__name__
        stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
        response = e.args[1]
        logger.error("Returning " + str(response))
    except exe.ConfigException as e:
        exception_name = e.__class__.__name__
        stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
        logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
        response = e.args[1]
        logger.error("Returning " + str(response))
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