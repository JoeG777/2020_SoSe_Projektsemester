from flask import Flask

app = Flask(__name__)


@app.route('/')
def default():
    """


    """
    return '<h1>Endpoints</h1><p>/train - Train a model</p><p>/predict - Make a prediction</p><p>/log - Get the logs</p>'


@app.route('/train')
def train():
    """
    Name in documentation: 'trainieren'

    """
    return 'train'


@app.route('/predict')
def predict():
    """
    Name in documentation: 'vorhersagen'

    """
    return 'predict'


@app.route('/log')
def get_logs():
    """
    Name in documentation: 'get_logs'

    """
    return 'logs'


def send_classification_request():
    """
    Name in documentation: 'sende_klassifizierungsanfrage'
    """