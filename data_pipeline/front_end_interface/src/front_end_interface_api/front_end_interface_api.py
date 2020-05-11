from flask import *
import data_pipeline.front_end_interface.src.nilan_control_service as ncs
import data_pipeline.front_end_interface.src.pipeline_control_service as pcs
import data_pipeline.exception.exceptions as exc
import data_pipeline.log_writer.log_writer as logger

app = Flask(__name__)

@app.route('/nilan_control_service')
def nilan_control_service():

    response = None

    try:
        json_validation()

        nilan_json = {
            "startdatum": request.get('start_datum'),
            "enddatum": request.get('end_datum'),
            "vorhersage": request.get('vorhersage'),
            "raumtemperatur": request.get('raumtemperatur'),
            "luefterstufe_zuluft": request.get('luefterstufe_zuluft'),
            "luefterstufe_abluft": request.get('luefterstufe_abluft'),
            "betriebsmodus": request.get('betriebsmodus')
        }

        ncs.write_to_nilan(nilan_json)

        response = 200

    except exc.DataPipelineException as dpxc:
        response = dpxc.args[1]

    except exc.IncompleteConfigException as icxc:
        response = dpxc.args[1]

    return Response(status=response)

@app.route('/pipeline_control_service')
def pipeline_control_service():

def json_validation():

    if int(request.headers.get('Content-Length')) == 0:
        logger.influx_logger.error('Config-JSON empty')
        raise exc.IncompleteConfigException('Config-JSON empty.', 900)

    try:
        request.get_json()['start_datum']
        request.get_json()['end_datum']
        request.get_json()['vorhersage']
        request.get_json()['raumtemperatur']
        request.get_json()['luefterstufe_zuluft']
        request.get_json()['luefterstufe_abluft']
        request.get_json()['betriebsmodus']

    except:
        logger.influx_logger.error('Incomplete Config-JSON')
        raise exc.IncompleteConfigException('Incomplete Config-JSON.', 900)
