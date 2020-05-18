from flask import *
import data_pipeline.front_end_interface.src.nilan_control_service.nilan_control_service as ncs
import data_pipeline.front_end_interface.src.pipeline_control_service.pipeline_control_service as pcs
import data_pipeline.exception.exceptions as exc
import data_pipeline.log_writer.log_writer as logger

app = Flask(__name__)
logger = logger.Logger("logs", "logs", "uipserver.ddns.net", 8086,"Forntend-Interface")
response = None

@app.route('/nilan_control_service', methods=['POST'])
def nilan_control_service():
    '''
    Name in documentation: 'nilan_control_service()'
    Gets called when new Data has to be persisted.
    The passed Data gets validated and afterwards calls the write_to_nilan method on
    nilan_control_service.
    :return: statuscode
    '''
    try:
        json_validation()
        ncs.write_to_nilan(request.args)

        response = 200

    except exc.DataPipelineException as dpxc:
        response = dpxc.args[1]

    except exc.IncompleteConfigException as icxc:
        response = icxc.args[1]

    return Response(status=response)

@app.route('/pipeline_control_service', methods=['POST'])
def pipeline_control_service():
    '''
    Name in Documentation: 'pipeline_control_service'
    Gets called when new Data has to be passed to the pipeline controller.
    The passed Data gets validated and afterwards triggers the process in pipeline_control_service
    :return: statuscode
    '''
    try:
        json_validation()
        pcs.start_process(request.args)

        response = 200

    except exc.DataPipelineException as dpxc:
        response = dpxc.args[1]

    except exc.IncompleteConfigException as icxc:
        response = icxc.args[1]

    return Response(status=response)

def json_validation():

    '''
    Gets called in the beginning of either 'pipeline_control_service' or 'nilan_control_service' to proof wether the passed config data
    is complete or not.
    :param index: Depending on the passed index, the config gets checked for another tag. Either 'forecastURL' or 'historischURL'.
    '''
    if int(request.headers.get('Content-Length')) == 0:
        logger.influx_logger.error('Config-JSON empty')
        raise exc.IncompleteConfigException('Config-JSON empty.', 900)

    parameter_names = ["start_datum", "end_datum", "vorhersage", "raumtemperatur", "luefterstufe_zuluft", "luefterstufe_abluft", "betriebsmodus"]

    for i in range(len(parameter_names)):

        try:
            request.get_json()[parameter_names[i]]

        except:
            logger.influx_logger.error('Incomplete Config-JSON')
            raise exc.IncompleteConfigException('Incomplete Config-JSON.', 900)
