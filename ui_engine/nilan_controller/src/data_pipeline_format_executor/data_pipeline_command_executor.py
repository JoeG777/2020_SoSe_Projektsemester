import requests
import data_pipeline.log_writer.log_writer as logger
import data_pipeline.exception.exceptions as exc
import json

logger = logger.Logger("logs", "logs", "uipserver.ddns.net", 8086,"Nilan Controller")


def build_request_data_pipeline_cmd(nilan_json):
    '''
    Name in documentation: 'build_request_data_pipeline_cmd'
    Triggers the front_end_interface to start the prediction process with the given json-File
    :param: nilan_json: user-settings
    :return: request to front-end-interface
    '''

    try:
        return requests.post("http://localhost:5001" + "/pipeline_control_service", {}, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
    except:
        logger.influx_logger.error('Unable to start forecast process.')
        raise exc.DataPipelineException('Unable to start forecast process.', 905)