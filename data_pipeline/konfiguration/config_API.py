from flask import *
import data_pipeline.exception.exceptions as exceptions
from data_pipeline.log_writer.log_writer import Logger
app = Flask(__name__)

logger = Logger()


def check_request(req_json):
    """
    Given the valid schema of a http-Post-requests, this function extracts all keys from the users request
    'req_json' and compares them to the given schema-keys. Only if both lists contain the same
    keys, true will be returned.
    :param req_json: post-request-object.
    :raise InvalidConfigException if the given object is null.
    :return True if the ecepted keys match the given keys in the request.
    """

    expected_keys = set(['frame_width', 'freq', 'register', 'time', 'from', 'to', 'threshold'])

    def get_keys(json_req):

        tmp = []

        def get_keys_rec(v_dict):
            for k, v in v_dict.items():
                if type(k) is dict:
                    tmp.append(k)
                    get_keys_rec(v)
                else:
                    tmp.append(k)

        for k, v in json_req.items():
            if type(v) is dict:
                tmp.append(k)
                get_keys_rec(v)
            else:
                tmp.append(k)

        return tmp

    if req_json is None:
        raise exceptions.InvalidConfigException('Request empty', 900)

    appendix = set(get_keys(req_json))

    return appendix == expected_keys


def check_if_request_empty():
    """ Checks if the incoming http-post-request comes with an empty body.
    :raise InvalidConfigException if the body is empty.
    :return request-object.
    """
    if int(request.headers.get('Content-Length')) == 0:
        raise exceptions.InvalidConfigException('Message must not be empty', 900)
    return request.get_json(force=True)


@app.route('/erhebung_config', methods=['POST'])
def erhebung_config():
    """
    Name in documentation: datenbereinigung()
    API callable via http-post-request when existing data needs to be cleaned. While executing every occurring
    error/warning will be logged into the log-database specified in db_connector.
    :return JSON-respond with status code 200 if call was successful and 900 otherwise.
     """

    response = {'statuscode': 200}

    try:

        pass

    except exceptions.InvalidConfigException as ice:
        response['statuscode'] = 900
        logger.influx_logger.error(ice.args[0])

    except exceptions.InconsistentConfigException as ice:
        response['statuscode'] = 900
        logger.influx_logger.error(ice.args[0])

    except exceptions.NoDataException as nde:
        response['statuscode'] = 900
        logger.influx_logger.error(nde.args[0])

    except exceptions.FormatException as fe:
        response['statuscode'] = 900
        logger.influx_logger.error(fe.args[0])

    except exceptions.ImputationDictionaryException as ide:
        response['statuscode'] = 900
        logger.influx_logger.error(ide.args[0])

    except exceptions.DBError as dbe:
        response['statuscode'] = 901
        logger.influx_logger.error(dbe.args[0])

    except Exception as e:
        response['statuscode'] = 500
        logger.influx_logger.error(e.args[0])

    finally:
        logger.influx_logger.info('bereinigungsprozess beendet mit statuscode' + str(response['statuscode']))
        return make_response(jsonify({'statuscode': response['statuscode']}))

@app.route('/bereinigung_config', methods=['POST'])
def bereinigung_config():
    pass

@app.route('/filterung_config', methods=['POST'])
def filterung_config():
    pass

@app.route('/klassifikation_config', methods=['POST'])
def klassifikation_config():
    pass

@app.route('/vorhersage_config', methods=['POST'])
def vorhersage_config():
    pass

@app.route('/frontend_interface_config', methods=['POST'])
def frontend_interface_config():
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
