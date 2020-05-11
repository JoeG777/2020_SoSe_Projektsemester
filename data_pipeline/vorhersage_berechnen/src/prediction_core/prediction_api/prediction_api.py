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


    """
    return '<h1>Endpoints</h1><p>/train - Train a model</p><p>/predict - Make a prediction</p><p>/log - Get the logs</p>'


@app.route('/train', methods=['POST'])
def train():
    """
    Name in documentation: 'trainieren'

    """
    status_code = 200
    if request.is_json:
        try:
            training_engine.train(request.get_json())
        except ConfigException:
            status_code = http_status_codes.get("ConfigException")
        except DBException:
            status_code = http_status_codes.get("DBException")
        except PersistorException:
            status_code = http_status_codes.get("PersistorException")
        except Exception:
            status_code = http_status_codes.get("HTTPInternalServerError")
    else:
        status_code = http_status_codes.get("HTTPBadRequest")

    return Response(status=status_code)


@app.route('/predict', methods=['POST'])
def predict():
    """
    Name in documentation: 'vorhersagen'

    """
    status_code = 200
    if request.is_json:
        try:
            prediction_engine.calculate_prediction(request.get_json())
        except ConfigException:
            status_code = http_status_codes.get("ConfigException")
        except DBException:
            status_code = http_status_codes.get("DBException")
        except PersistorException:
            status_code = http_status_codes.get("PersistorException")
        except Exception:
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