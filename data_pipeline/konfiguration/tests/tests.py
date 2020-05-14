import unittest
import data_pipeline.konfiguration.src.config_validator as validator
from data_pipeline.konfiguration.src.bereinigungs_config import bereinigungs_config as be_con
import data_pipeline.konfiguration.src.config_API as api


class test_get_json_from_api(unittest.TestCase):

    def test_return_correct_json(self):

        expected_json = {
            'measurement': 'temperature_DWD',
            'value_name': 'temperature',
            'frame_width': 100,
            'freq': '60S',
            'register': 'historic',
            'time': {
                'from': '1579561622474ms',
                'to': '1580261128794ms'
            },
            'threshold': 3600
        }
        self.api = api.app.test_client()
        resp = self.api.get('/bereinigung_config')
        resp_json = resp.get_json()

        self.assertEqual(resp_json, expected_json)


class test_get_json(unittest.TestCase):

    def test_validator_matching_keys(self):

        expected_keys = ['measurement', 'value_name', 'frame_width', 'freq', 'register', 'time', 'from', 'to',
                         'threshold']
        json_request = {
            'measurement': 'temperature_DWD',
            'value_name': 'temperature',
            'frame_width': 100,
            'freq': '60S',
            'register': 'historic',
            'time': {
                'from': '1579561622474ms',
                'to': '1580261128794ms'
            },
            'threshold': 3600
        }

        self.assertTrue(validator.check_keys_in_request(json_request, expected_keys))
