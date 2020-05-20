import json
import data_pipeline.exception.exceptions as exc
from data_pipeline.front_end_interface.src.front_end_interface_api.front_end_interface_api import logger
import requests


def build_request_data_pipeline_cmd():
    '''
    Calls the 'start_process'-method in the pipeline controller, which starts the whole forecast process.
    :param parameters: Parameters from Usersettings in the Web-application
    '''

    try:
        print("test3")
        return requests.post("http://localhost:5000" + "/start_process", {}, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
    except:
        logger.influx_logger.error('Unable to start process')
        raise exc.RawDataException('Unable to start process', 905)

