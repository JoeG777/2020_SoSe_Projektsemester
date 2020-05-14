from flask import *
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import data_pipeline.daten_klassifizieren.classification_engine as classification
import data_pipeline.daten_klassifizieren.training_engine as training
import data_pipeline.exception.exceptions as ex


app = Flask(__name__)

# TODO: Fehlerhandling in der API?


@app.route('/classify', methods=['POST'])
def classify():
    response = 200
    try:
        extracted_config = request.get_json()
        classification.apply_classifier(extracted_config)
    except ex.ConfigException:
        response = 900
    except ex.DBException:
        response = 901
    except ex.PersistorException:
        response = 902
    """except ex.FileException:
        response = 900
    """

    status_code = Response(status=response)
    return status_code


@app.route('/train', methods=['POST'])
def train():
    response = 200
    try:
        config = request.get_json()

        trainingsdata.enrich_data(config)
        trainingsdata.mark_data(config)
        training.train_classifier(config)
    except ex.ConfigException:
        response = 900
    except ex.DBException:
        response = 901
    except ex.PersistorException:
        response = 902
    """except ex.FileException:
        response = 900
    """

    status_code = Response(status=response)
    return status_code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
