from flask import *
import data_pipeline.vorhersage_berechnen.src.prediction_core.training_engine.training_engine as training_engine
import data_pipeline.vorhersage_berechnen.src.prediction_core.prediction_engine.prediction_engine as prediction_engine
from data_pipeline.exception.exceptions import *


app = Flask(__name__)

http_status_codes = {
    "HTTPBadRequest": 400,
    "HTTPInternalServerError": 500,
    "ConfigException": 900,
    "DBException": 901,
    "PersistorException": 902
}

@app.route('/')
def default():
    """
    Not featured in the documentation.
    Just returns information about the API.
    """
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
    print("Starting training-----")
    print(request)
    status_code = 200
    if request.is_json:
        try:
            training_engine.train(request.get_json())
        except ConfigException as e:
            status_code = http_status_codes.get("ConfigException")
        except DBException as e:
            status_code = http_status_codes.get("DBException")
        except PersistorException as e:
            status_code = http_status_codes.get("PersistorException")
        except Exception as e:
            print(e.with_traceback())
            status_code = http_status_codes.get("HTTPInternalServerError")
    else:
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