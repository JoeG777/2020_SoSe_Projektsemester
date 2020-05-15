import data_pipeline.exception.exceptions as exceptions
from data_pipeline.exception.exceptions import ConfigException


def check_keys_in_request(req_json, expected_keys):
    """
    Given the valid schema of a http-Post-requests, this function extracts all keys from the users request
    'req_json' and compares them to the given schema-keys. Only if both lists contain the same
    keys, true will be returned.
    :param req_json: post-request-object.
    :raise InvalidConfigException if the given object is null.
    :return True if the ecepted keys match the given keys in the request.
    """

    expected_keys = {'value_name', 'measurement', 'frame_width', 'freq', 'register', 'time', 'from', 'to', 'threshold'}

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
        raise ConfigException('Request empty', 900)

    appendix = set(get_keys(req_json))

    return appendix == expected_keys
