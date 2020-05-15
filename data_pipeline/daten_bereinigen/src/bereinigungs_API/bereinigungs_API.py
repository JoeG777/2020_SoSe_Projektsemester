from flask import *
from data_pipeline.daten_bereinigen.src.bereinigungs_engine import bereinigungs_engine as cleaning_eng
import data_pipeline.exception.exceptions as exceptions
import data_pipeline.konfiguration.src.config_validator as validator

from data_pipeline.log_writer.log_writer import Logger

app = Flask(__name__)

logger = Logger("logs", "cleaning_logs", "uipserver.ddns.net", 8086, "Cleaning_API")
expected_keys = set(['sensor_data',
                  'from_db', 'to_db', 'from_measurement', 'to_measurement', 'value_name', 'register',
                  'frame_width', 'freq', 'threshold', 'time',  'to', 'from',
                  'historic_weatherdata',
                  'from_db', 'to_db', 'from_measurement', 'to_measurement', 'value_name', 'register',
                  'frame_width', 'freq', 'threshold', 'time',  'to', 'from',
                  'forecast_weatherdata',
                  'from_db', 'to_db', 'from_measurement', 'to_measurement', 'value_name', 'register',
                  'frame_width', 'freq', 'threshold', 'time', 'to', 'from'])

#expected_keys = set(
#    ['frame_width', 'freq', 'value_name', 'to_measurement', 'to_db', 'sensor_data', 'historic_weatherdata', 'threshold',
#     'forecast_weatherdata', 'register', 'from_measurement', 'time', 'from_db'])


def check_if_request_empty():
    """ Checks if the incoming http-post-request comes with an empty body.
    :raise InvalidConfigException if the body is empty.
    :return request-object.
    """
    if int(request.headers.get('Content-Length')) == 0:
        raise exceptions.NoDataException('Message must not be empty', 900)
    return request.get_json(force=True)


@app.route('/datenbereinigung', methods=['POST'])
def cleaning():
    """
    Name in documentation: datenbereinigung()
    API callable via http-post-request when existing data needs to be cleaned. While executing every occurring
    error/warning will be logged into the log-database specified in db_connector.
    :return JSON-respond with status code 200 if call was successful and 900 otherwise.
     """

    response = {'statuscode': 200}

    try:

        incoming_req = check_if_request_empty()
        if validator.check_keys_in_request(incoming_req, expected_keys):

            start_process_with_config_params(incoming_req, 'sensor_data')
            start_process_with_config_params(incoming_req, 'historic_weatherdata')
            start_process_with_config_params(incoming_req, 'forecast_weatherdata')

        else:
            raise exceptions.InvalidConfigKeyException('Received invalid keys', 900)

    except exceptions.InvalidConfigKeyException as ice:
        response['statuscode'] = 900
        logger.error(ice.args[0])

    except exceptions.InconsistentConfigException as ice:
        response['statuscode'] = 900
        logger.error(ice.args[0])

    except exceptions.NoDataException as nde:
        response['statuscode'] = 900
        logger.error(nde.args[0])

    except exceptions.FormatException as fe:
        response['statuscode'] = 900
        logger.error(fe.args[0])

    except exceptions.ImputationDictionaryException as ide:
        response['statuscode'] = 900
        logger.error(ide.args[0])

    except exceptions.DBException as dbe:
        response['statuscode'] = 901
        logger.error(dbe.args[0])

    except Exception as e:
        response['statuscode'] = 500
        logger.error(e.args[0])

    finally:
        logger.info('bereinigungsprozess beendet mit statuscode: ' + str(response['statuscode']))
        return make_response(jsonify({'statuscode': response['statuscode']}))


def start_process_with_config_params(incoming_req, process_type):
    sensor_data = incoming_req[process_type]
    from_db = sensor_data['from_db']
    to_db = sensor_data['to_db']
    from_measurement = sensor_data['from_measurement']
    to_measurement = sensor_data['to_measurement']
    value_name = sensor_data['value_name']
    register = sensor_data['register']
    frame_width = sensor_data['frame_width']
    freq = sensor_data['freq']
    threshold = sensor_data['threshold']
    time = sensor_data['time']

    cleaning_eng.fast_and_furious(from_db, to_db, from_measurement, to_measurement, value_name, register,
                                  frame_width, freq, threshold, time)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
