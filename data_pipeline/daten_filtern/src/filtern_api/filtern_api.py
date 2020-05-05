from flask import *
from data_pipeline.daten_filtern.src.filtern_engine.filtern_engine import filtern_engine

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
    Start the filtern engine.
    '''

    filtern_engine.filtern()

    return render_template('index.html')


@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    '''
    return 'logs'