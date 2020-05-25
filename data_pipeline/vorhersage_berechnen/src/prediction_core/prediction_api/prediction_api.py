from data_pipeline.log_writer.log_writer import Logger

LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "uipserver.ddns.net"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Vorhersage berechnen"

logger = Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT,
                LOGGER_COMPONENT)

import json
from flask import *
import data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine.training_engine as training_engine
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_engine.prediction_engine as prediction_engine
from data_pipeline.exception.exceptions import *
import traceback
import requests

app = Flask(__name__)

http_status_codes = {
    "HTTPOK": 200,
    "HTTPBadRequest": 400,
    "HTTPInternalServerError": 500,
    "ConfigException": 900,
    "DBException": 901,
    "PersistorException": 902
}
CLASSIFICATION_INIT_URL = "http://localhost:5000/classify"


@app.route('/')
def default():
    """
    Not featured in the documentation.
    Just returns information about the API.
    """
    logger.info("Received request on default endpoint. Returning default answer.")
    return '<h1>Endpoints</h1><p>/train - Train a model</p>' \
           '<p>/predict - Make a prediction</p><p>/log - Get the logs</p>'


@app.route('/train', methods=['POST'])
def train():
    """
    Name in documentation: 'trainieren'
    This method is used to apply the trained models and create new predictions.
    :return: a Flask response containg one of the following status codes
    400 - Bad Request - e.g. if the request body is not a JSON
    500 - Internal Server Error - in any error cases not described here
    900 - Config Error - if the message body contains an invalid config
    901 - DBException - if there are problems with the database connection
    902 - PersistorException - if there are problems with persisting the new models
    """
    logger.info("Received request on train endpoint. Starting training procedure...")
    status_code = 200
    if request.is_json:
        try:
            training_engine.train(request.get_json())
            logger.info("Training was successful. Returning " + str(http_status_codes.get("HTTPOK")))
        except ConfigException as e:
            print(e.with_traceback())
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("ConfigException")
            logger.error("Returning " + str(status_code))
        except DBException as e:
            print(e.with_traceback())
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("DBException")
            logger.error("Returning " + str(status_code))
        except PersistorException as e:
            print(e.with_traceback())
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("PersistorException")
            logger.error("Returning " + str(status_code))
        except Exception as e:
            print(e.with_traceback())
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught (unknown). StackTrace: " + stack_trace)
            logger.error("Returning " + str(http_status_codes.get("HTTPInternalServerError")))
            status_code = http_status_codes.get("HTTPInternalServerError")
    else:
        logger.info("Request is not JSON. Returning " + str(http_status_codes.get("HTTPBadRequest")) + ".")
        status_code = http_status_codes.get("HTTPBadRequest")

    return Response(status=status_code)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Name in documentation: 'vorhersagen'
    This method is used to apply the trained models and create new predictions.
    :return: a Flask response containg one of the following status codes
    400 - Bad Request - e.g. if the request body is not a JSON
    500 - Internal Server Error - in any error cases not described here
    900 - Config Error - if the message body contains an invalid config
    901 - DBException - if there are problems with the database connection
    902 - PersistorException - if there are problems with the persisted models
    """
    logger.info("Received request on predict endpoint. Starting prediction procedure...")
    status_code = 200
    if request.is_json:
        try:
            prediction_engine.calculate_prediction(request.get_json())
            logger.info("New prediction created successfully. Returning " + str(http_status_codes.get("HTTPOK")))
        except ConfigException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("ConfigException")
            logger.error("Returning " + str(status_code))
        except DBException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("DBException")
            logger.error("Returning " + str(status_code))
        except PersistorException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            status_code = http_status_codes.get("PersistorException")
            logger.error("Returning " + str(status_code))
        except Exception as e:
            print(e.with_traceback())
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught (unknown). StackTrace: " + stack_trace)
            logger.error("Returning " + str(http_status_codes.get("HTTPInternalServerError")))
            status_code = http_status_codes.get("HTTPInternalServerError")
    else:
        logger.info("Request is not JSON. Returning " + str(http_status_codes.get("HTTPBadRequest")))
        status_code = http_status_codes.get("HTTPBadRequest")

    return Response(status=status_code)


def send_classification_request(classification_config):
    """
    Name in documentation: 'sende_klassifizierungsanfrage'
    """
    requests.post(CLASSIFICATION_INIT_URL, json=classification_config)
    return "Success!"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)