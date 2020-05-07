from flask import *
import data_pipeline.daten_klassifizieren.trainingsdata_editing_engine as trainingsdata
import data_pipeline.daten_klassifizieren.classification_engine as classification
import data_pipeline.daten_klassifizieren.training_engine as training

app = Flask(__name__)

# TODO: Fehlerhandling in der API?

@app.route('/classify', methods=['POST'])
def classify():
    response = 200
    try:
        config = request.get_json(force=True)
        print(type(config))
        if type(config) != dict:
            print("raise: ConfigError")
            response = 500

        #classification.apply_classifier(config)
    except Exception:
        response = 500

    status_code = Response(status=response)
    return status_code


@app.route('/train', methods=['POST', 'GET'])
def train():
    response = 200
    try:
        config = request.get_json(force=True)
        print(type(config))
        if type(config) != dict:
            print("raise: ConfigError")
            response = 500

        print(config)
        # TODO: Welche Fehler können auftreten? Modellierung sagt gar keine ?!
        #trainingsdata.expand_data(config)
        #trainingsdata.mark_data(config)
        #training.train_classifier(config)
    except Exception:
        response = 500

    status_code = Response(status=response)
    return status_code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
