import requests
import data_pipeline.log_writer.log_writer as logger
import data_pipeline.exception.exceptions as exc
import json

logger = logger.Logger("logs", "logs", "uipserver.ddns.net", 8086,"Nilan Controller")


def build_request_modbus_cmd(nilan_json):
    '''
    Name in documentation: 'build_request_modbus_cmd'
    Triggers the front_end_interface to save the user-settings into InfluxDB
    :param: nilan_json: user-settings
    :return: request to front-end-interface
    '''

    try:
        return requests.post("http://localhost:5001" + "/nilan_control_service", json=nilan_json, headers={'Content-type': 'application/json'})

    except:
        logger.influx_logger.error('Unable to save new parameters.')
        raise exc.RawDataException('Unable to save new parameters.', 905)