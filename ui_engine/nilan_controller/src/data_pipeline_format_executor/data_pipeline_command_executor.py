import requests
import data_pipeline.log_writer.log_writer as logger
import data_pipeline.exception.exceptions as exc
import json

logger = logger.Logger()


def drop_post_request(url, payload):
    return requests.post(url, json=json.dumps(payload))


def build_request_data_pipeline_cmd(json):
    try:
        return drop_post_request("http://localhost:5001" + "/pipeline_control_service ", json)
    except:
        logger.influx_logger.error('Unable to start forecast process.')
        raise exc.DataPipelineException('Unable to start forecast process.', 905)