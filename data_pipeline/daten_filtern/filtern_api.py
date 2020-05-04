from flask import *
from filtern_config import filtern_config
import filtern_engine

app = Flask(__name__)

@app.route('/')
def default():
    '''

    '''
    return '<h1>Endpoints</h1><p>/filtern - filter data</p><p>/log - Get the logs</p>'




@app.route('/filtern')
def filtern():
    '''
    Name in documentation: 'filtern'
    '''
    config = filtern_config["filter_options"][filtern_config["selected_value"]]

    data_pipeline.daten_filtern.filtern_engine.filtern(config)

    return render_template('index.html')


@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    '''
    return 'logs'