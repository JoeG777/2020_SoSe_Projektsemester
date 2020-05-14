from flask import *
import data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine.training_engine as training_engine
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_engine.prediction_engine as prediction_engine
from data_pipeline.log_writer.log_writer import Logger
from data_pipeline.exception.exceptions import *
import sys

app = Flask(__name__)

http_status_codes = {
    "HTTPBadRequest": 400,
    "HTTPInternalServerError": 500,
    "ConfigException": 900,
    "DBException": 901,
    "PersistorException": 902
}

LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "localhost"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Vorhersage berechnen"

logger = Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT,
                LOGGER_COMPONENT)

@app.route('/')
def default():
    """
    Not featured in the documentation.
    Just returns information about the API.
    """
    logger.info("Received request on default endpoint. Returning default answer.")
    return '<h1>Endpoints</h1><p>/train - Train a model</p><p>/predict - Make a prediction</p><p>/log - Get the logs</p>'


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
        except ConfigException as e:
            exception_name = type(e).__name__
            logger.error(exception_name + " was caught.\n StackTrace: " + str(e.__traceback__))
            logger.error("Returning " + str(http_status_codes.get(exception_name)))
            status_code = http_status_codes.get(exception_name)
        except DBException as e:
            logger.error(type(e).__name__ + " was caught.\n StackTrace: " + str(e.__traceback__))
            status_code = http_status_codes.get("DBException")
        except PersistorException as e:
            logger.error(type(e).__name__ + " was caught.\n StackTrace: " + str(e.__traceback__))
            status_code = http_status_codes.get("PersistorException")
        except Exception as e:
            logger.error(type(e).__name__ + " was caught.\n StackTrace: " + str(e.__traceback__))
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

    status_code = 200
    if request.is_json:
        try:
            print("-----predicting----")
            prediction_engine.calculate_prediction(request.get_json())
        except ConfigException as e:
            print(e.with_traceback())
            status_code = http_status_codes.get("ConfigException")
        except DBException as e:
            print(e.with_traceback())
            status_code = http_status_codes.get("DBException")
        except PersistorException as e:
            print(e.with_traceback())
            status_code = http_status_codes.get("PersistorException")
        except Exception as e:
            print(e.with_traceback())
            status_code = http_status_codes.get("HTTPInternalServerError")
    else:
        logger.info("Request is not JSON. Returning 400 - Bad Request.")
        status_code = http_status_codes.get("HTTPBadRequest")

    return Response(status=status_code)


@app.route('/log')
def get_logs():
    """
    Name in documentation: 'get_logs'

    """
    return 'logs'


def send_classification_request(documentation):
    """
    Name in documentation: 'sende_klassifizierungsanfrage'
    """