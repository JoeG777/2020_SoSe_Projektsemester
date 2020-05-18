import json
import data_pipeline.exception.exceptions as exc
import data_pipeline.log_writer.log_writer as log_writer
import requests

logger = log_writer.Logger()


def build_request_data_pipeline_cmd(front_end_json):
    '''
    Calls the 'start_process'-method in the pipeline controller, which starts the whole forecast process.
    :param parameters: Parameters from Usersettings in the Web-application
    '''

    try:
        return requests.post("http://localhost:5000" + "/start_process ", json=json.dumps(json))
    except:
        logger.influx_logger.error('Unable to start process')
        raise exc.RawDataException('Unable to start process', 905)

