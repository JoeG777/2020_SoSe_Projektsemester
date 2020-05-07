from flask import *
from data_pipeline.daten_filtern.src.filtern_engine import filtern_engine
from influxdb import InfluxDBClient
from data_pipeline.daten_filtern.src.filtern_config.filtern_config import filtern_config
from data_pipeline.exception.exceptions import ConfigException

app = Flask(__name__)

@app.route('/filtern')
def filter():
    '''
    Name in documentation: 'filtern'
    Start the filtern engine.
    '''

    response = None
    try:

        config = filtern_config["filter_options"][filtern_config["selected_value"]]

        filtern_engine.filtern(config)

        response = 200

    except ConfigException:
        response = ConfigException.args[1]
    finally:
        return Response(status=response)



@app.route('/log')
def get_logs():
    '''
    Name in documentation: 'get_logs'
    '''
    return 'logs'

if __name__ == '__main__':
    app.run(host='localhost', port='8000')