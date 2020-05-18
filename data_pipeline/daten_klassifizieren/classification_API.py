import data_pipeline.log_writer.log_writer as logger
LOGGER_DB_NAME = "logs"
LOGGER_MEASUREMENT = "logs"
LOGGER_HOST = "uipserver.ddns.net"
LOGGER_PORT = "8086"
LOGGER_COMPONENT = "Daten klassifizieren"
logger = logger.Logger(LOGGER_DB_NAME, LOGGER_MEASUREMENT, LOGGER_HOST, LOGGER_PORT, LOGGER_COMPONENT)

from flask import *
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import data_pipeline.daten_klassifizieren.classification_engine as classification
import data_pipeline.daten_klassifizieren.training_engine as training
import data_pipeline.exception.exceptions as ex
import traceback

app = Flask(__name__)

http_status_codes = {
    "HTTPOK": 200,
    "HTTPBadRequest": 400,
    "HTTPInternalServerError": 500,
    "ConfigException": 900,
    "DBException": 901,
    "PersistorException": 902,
    "FileException": 903,
    "SklearnException": 904
}

@app.route('/')
def default():
    """
    Not featured in the documentation.
    Just returns information about the API.
    """
    logger.info("Received request on default endpoint. Returning default answer.")
    return '<h1>Endpoints</h1><p>/train - Train a model</p><p>/classify - Classify data</p>'


@app.route('/classify', methods=['POST'])
def classify():
    """Name in documentation: 'classify'
    This method is used to apply the trained models and classify new data.
    :return: a Flask response contains one of the following status codes
    400 - Bad Request - e.g. if the request body is not a JSON
    500 - Internal Server Error - in any error cases not described here
    900 - Config Error - if the message body contains an invalid config
    901 - DBException - if there are problems with the database connection
    902 - PersistorException - if there are problems with the persisted models
    903 - FileException - if there are problems im model persistor with the files
    904 - SklearnException - if there are problems with Sklearn methods    """

    logger.info("Received request on classify endpoint. Starting classify procedure...")
    response = 200
    if request.is_json:
        try:
            extracted_config = request.get_json(force=True)
            classification.apply_classifier(extracted_config)
        except ex.ConfigException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("ConfigException")
            logger.error("Returning " + str(response))
        except ex.DBException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("DBException")
            logger.error("Returning " + str(response))
        except ex.PersistorException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("PersistorException")
            logger.error("Returning " + str(response))
        except ex.FileException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("FileException")
            logger.error("Returning " + str(response))
        except ex.SklearnException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("SklearnException")
            logger.error("Returning " + str(response))
    else:
        logger.info("Request is not JSON. Returning " + str(http_status_codes.get("HTTPBadRequest")))
        response = http_status_codes.get("HTTPBadRequest")

    status_code = Response(status=response)
    return status_code


@app.route('/train', methods=['POST'])
def train():
    """Name in documentation: 'train'
    This method is used to train models.
    :return: a Flask response contains one of the following status codes
    400 - Bad Request - e.g. if the request body is not a JSON
    500 - Internal Server Error - in any error cases not described here
    900 - Config Error - if the message body contains an invalid config
    901 - DBException - if there are problems with the database connection
    902 - PersistorException - if there are problems with persisting the new models
    903 - FileException - if there are problems im model persistor with the files"""

    logger.info("Received request on train endpoint. Starting training procedure...")
    response = 200
    if request.is_json:
        try:
            config = request.get_json(force=True)
            trainingsdata.enrich_data(config)
            logger.info("Enrich data was successful.")
            trainingsdata.mark_data(config)
            logger.info("Mark data was successful.")
            training.train_classifier(config)
            logger.info("Training was successful. Returning " + str(http_status_codes.get("HTTPOK")))
        except ex.ConfigException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("ConfigException")
            logger.error("Returning " + str(response))
        except ex.DBException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("DBException")
            logger.error("Returning " + str(response))
        except ex.PersistorException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("PersistorException")
            logger.error("Returning " + str(response))
        except ex.FileException as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught. StackTrace: " + stack_trace)
            response = http_status_codes.get("FileException")
            logger.error("Returning " + str(response))
        except Exception as e:
            exception_name = e.__class__.__name__
            stack_trace = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            logger.error(exception_name + " was caught (unknown). StackTrace: " + stack_trace)
            logger.error("Returning " + str(http_status_codes.get("HTTPInternalServerError")))
            response = http_status_codes.get("HTTPInternalServerError")

    status_code = Response(status=response)
    return status_code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
