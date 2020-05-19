import unittest
import data_pipeline.daten_bereinigen.src.bereinigungs_API.bereinigungs_API as api
import data_pipeline.exception.exceptions as excep
import data_pipeline.konfiguration.src.config_validator as validator

expected_keys = set(['measurement', 'value_name', 'frame_width', 'freq', 'register', 'time', 'from', 'to', 'threshold'])


class test_api(unittest.TestCase):

    def test_empty_request(self):
        self.app = api.app.test_client()
        resp = self.app.post('/datenbereinigung', json={})
        resp_json = resp.get_json()
        self.assertEqual(resp_json['statuscode'], 900)

    def test_wrong_request(self):
        self.app = api.app.test_client()
        resp = self.app.post('/datenbereinigung', json={'siktir': 'lan'})
        resp_json = resp.get_json()
        self.assertEqual(resp_json['statuscode'], 900)


class test_check_request(unittest.TestCase):

    def test_wrong_incoming_request(self):
        test_request_body = {
            'frame_weidth': 100,
            'teim': 100,
            'frohm': 'hallo'}
        self.assertFalse(validator.check_keys_in_request(test_request_body, expected_keys))

    def test_none_request(self):
        test_request_body = None
        self.assertRaises(excep.InvalidConfigKeyException, validator.check_keys_in_request, test_request_body, expected_keys)

    def test_correct_request(self):
        test_request_body = {
            'measurement': 'temperatur_DWD',
            'value_name': 'temperature',
            'frame_width': 100,
            'freq': '60S',
            'register': 'historic',
            'time': {
                'from': '1579561622474ms',
                'to': '1580261128794ms'
            },
            'threshold': 3600,
        }
        self.assertTrue(validator.check_keys_in_request(test_request_body, expected_keys))


if __name__ == '__main__':
    unittest.main()
